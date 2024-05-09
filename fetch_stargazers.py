import requests
import json
import os
import time
import datetime
import logging
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'latitude-dev'
REPO_NAME = 'latitude'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Content-Type': 'application/json'
}

if TOKEN is None:
    logging.critical("GITHUB_TOKEN is not set. Please set the environment variable and retry.")
    exit(1)

session = requests.Session()
retries = Retry(total=5, 
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=frozenset(['GET', 'POST']))
session.mount('https://', HTTPAdapter(max_retries=retries))

def run_graphql_query(query, variables=None):
    """Execute a GraphQL query with error handling for rate limits."""
    url = 'https://api.github.com/graphql'
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = session.post(url, headers=HEADERS, json={'query': query, 'variables': variables})
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)

            response_data = response.json()
            if 'data' in response_data:
                return response_data['data']
            elif 'errors' in response_data:
                error_messages = [error['message'] for error in response_data['errors']]
                logging.error(f"🚨 GraphQL errors: {error_messages}")

                if any('rate limit exceeded' in message.lower() for message in error_messages):  # Adjusted to catch more general rate limit errors
                    retry_count += 1
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        wait_until_reset = max(0, int(reset_time) - int(time.time()) + 10)  # Extra 10 seconds buffer
                        readable_reset_time = datetime.datetime.fromtimestamp(int(reset_time)).strftime('%Y-%m-%d %H:%M:%S')
                        logging.warning(f"⏳ Rate limit exceeded. Waiting until {readable_reset_time} to retry...")
                        time.sleep(wait_until_reset)
                        continue
                    else:
                        logging.error("🚨 'X-RateLimit-Reset' header is missing from the response.")
        except HTTPError as http_err:
            logging.error(f"🚨 HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"🚨 Other error occurred: {err}")

        retry_count += 1  # Increment retry count for any type of failure not just rate limit

    logging.error("🚨 Reached maximum retry limit without successful data retrieval.")
    return None

def get_stargazers(repo_owner, repo_name):
    """Fetch up to 10 stargazers for a given GitHub repository, along with the total count."""
    query = """
    query ($repoOwner: String!, $repoName: String!, $cursor: String, $limit: Int!) {
      repository(owner: $repoOwner, name: $repoName) {
        stargazers(first: $limit, after: $cursor) {
          totalCount
          edges {
            node {
              login
            }
            cursor
          }
          pageInfo {
            hasNextPage
          }
        }
      }
    }
    """
    stargazers = []
    cursor = None
    batch_size = 100  # Reduce batch size to limit total fetch size
    total_count = 0

    while True:
        variables = {'repoOwner': repo_owner, 'repoName': repo_name, 'cursor': cursor, 'limit': batch_size}
        data = run_graphql_query(query, variables)
        if not data or 'repository' not in data:
            break
        page = data['repository']['stargazers']
        if total_count == 0:  # Ensure total_count is fetched only once
            total_count = page['totalCount']
        stargazers.extend([edge['node']['login'] for edge in page['edges']])
        if len(stargazers) >= 5:  # Stop once we have 5 stargazers
            break
        if not page['pageInfo']['hasNextPage']:
            break
        cursor = page['edges'][-1]['cursor']

    return stargazers[:5], total_count
    # return stargazers, total_count

def run_paginated_query(query, variables, item_key):
    """Run paginated GraphQL queries to fetch all items in a paginated structure."""
    items = []
    while True:
        data = run_graphql_query(query, variables)
        if not data or item_key not in data['user']:
            break
        page = data['user'][item_key]
        items.extend([item['node'] for item in page['edges']])
        if not page['pageInfo']['hasNextPage']:
            break
        variables['cursor'] = page['edges'][-1]['cursor']
    return items

def get_user_details(username):
    """Fetch user details including following, organizations, starred repos, and additional user info using GraphQL."""
    # Check the count of starred repositories first
    starred_count_query = """
    query ($username: String!) {
      user(login: $username) {
        starredRepositories {
          totalCount
        }
      }
    }
    """
    starred_count_data = run_graphql_query(starred_count_query, {'username': username})
    starred_repos_count = starred_count_data['user']['starredRepositories']['totalCount'] if starred_count_data and 'user' in starred_count_data and 'starredRepositories' in starred_count_data['user'] else 0

    # If the count of starred repositories exceeds 5000, skip this user
    if starred_repos_count > 5000:
        logging.info(f"Skipping {username} with {starred_repos_count} starred repositories.")
        return None
    # Following query
    following_query = """
    query ($username: String!, $cursor: String) {
      user(login: $username) {
        following(first: 100, after: $cursor) {
          edges {
            node {
              login
            }
            cursor
          }
          pageInfo {
            hasNextPage
          }
        }
      }
    }
    """
    following = run_paginated_query(following_query, {'username': username, 'cursor': None}, 'following')

    # Starred repositories query
    starred_repos_query = """
    query ($username: String!, $cursor: String) {
      user(login: $username) {
        starredRepositories(first: 100, after: $cursor) {
          edges {
            node {
              nameWithOwner
              stargazers {
                totalCount
              }
            }
            cursor
          }
          pageInfo {
            hasNextPage
          }
        }
      }
    }
    """
    starred_repositories = run_paginated_query(starred_repos_query, {'username': username, 'cursor': None}, 'starredRepositories')
    starred_repositories = [repo for repo in starred_repositories if repo['stargazers']['totalCount'] > 500]

    # Organizations query with pagination
    organizations_query = """
    query ($username: String!, $cursor: String) {
      user(login: $username) {
        organizations(first: 100, after: $cursor) {
          nodes {
            login
          }
          pageInfo {
            hasNextPage
            endCursor
          }
        }
      }
    }
    """
    organizations = []
    cursor = None
    while True:
        org_data = run_graphql_query(organizations_query, {'username': username, 'cursor': cursor})
        if not org_data or 'user' not in org_data or 'organizations' not in org_data['user']:
            break
        page = org_data['user']['organizations']
        organizations.extend([org['login'] for org in page['nodes']])
        if not page['pageInfo']['hasNextPage']:
            break
        cursor = page['pageInfo']['endCursor']

    # Public repositories count query
    public_repos_query = """
    query ($username: String!) {
      user(login: $username) {
        repositories(privacy: PUBLIC, first: 1) {
          totalCount
        }
      }
    }
    """
    public_repos_data = run_graphql_query(public_repos_query, {'username': username})
    public_repos_count = public_repos_data['user']['repositories']['totalCount'] if public_repos_data and 'user' in public_repos_data and 'repositories' in public_repos_data['user'] else 0

    # Basic user info query
    basic_info_query = """
    query ($username: String!) {
      user(login: $username) {
        login
        email
        location
        createdAt
        updatedAt
        followers {
          totalCount
        }
        company
      }
    }
    """
    
    basic_info_variables = {'username': username}
    basic_info_data = run_graphql_query(basic_info_query, basic_info_variables)
    if basic_info_data and 'user' in basic_info_data:
        user_info = basic_info_data['user']
        return {
            'username': user_info['login'],
            'email': user_info.get('email', 'N/A'),
            'location': user_info.get('location', 'N/A'),
            'created_at': user_info['createdAt'],
            'updated_at': user_info['updatedAt'],
            'followers_count': user_info['followers']['totalCount'],
            'company': user_info.get('company', 'N/A'),
            'following_count': len(following),
            'following': ', '.join([person['login'] for person in following]),
            'organizations': ', '.join(organizations),
            'public_repos_count': public_repos_count,
            'starred_repos_count': len(starred_repositories),
            'starred_repos': ', '.join([repo['nameWithOwner'] for repo in starred_repositories])
        }
    else:
        logging.error(f"🚨 Failed to retrieve data for user {username}")
        return {}

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_directory_exists('queries')

def save_csv(data, filename, fieldnames):
    path = os.path.join('queries', filename)
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_organizations(data, filename):
    path = os.path.join('queries', filename)
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['username', 'organization']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in data:
            username = user['username']
            for organization in user['organizations'].split(', '):
                if organization:
                    writer.writerow({'username': username, 'organization': organization})


def save_followings(data, filename):
    path = os.path.join('queries', filename)
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['username', 'following']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in data:
            username = user['username']
            for following in user['following'].split(', '):
                if following:
                    writer.writerow({'username': username, 'following': following})


def save_repos(data, filename):
    path = os.path.join('queries', filename)
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['username', 'starred_repo']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for user in data:
            username = user['username']
            for repo in user['starred_repos'].split(', '):
                if repo:
                    writer.writerow({'username': username, 'starred_repo': repo})

def main():
    logging.info("Starting data collection")
    stargazers, total_count = get_stargazers(REPO_OWNER, REPO_NAME)
    user_details_data = []
    following_data = []
    repos_data = []
    organizations_data = []

    # Define the number of workers
    workers = 2  # Adjust based on your environment capabilities

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_username = {executor.submit(get_user_details, username): username for username in stargazers}

        for i, future in enumerate(as_completed(future_to_username), start=1):
            username = future_to_username[future]
            try:
                user_details = future.result()
                if user_details:  # Check if the user details were actually fetched
                    # Prepare data for individual CSV files
                    user_details_data.append({
                        'username': user_details['username'],
                        'email': user_details['email'],
                        'location': user_details['location'],
                        'company': user_details['company'],
                        'created_at': user_details['created_at'],
                        'updated_at': user_details['updated_at'],
                        'followers_count': user_details['followers_count'],
                        'following_count': user_details['following_count'],
                        'public_repos_count': user_details['public_repos_count'],
                        'starred_repos_count': user_details['starred_repos_count']
                    })
                    following_data.append({
                        'username': user_details['username'],
                        'following': user_details['following']
                    })
                    repos_data.append({
                        'username': user_details['username'],
                        'starred_repos': user_details['starred_repos']
                    })
                    organizations_data.append({
                        'username': user_details['username'],
                        'organizations': user_details['organizations']
                    })
                    logging.info(f"✅ Processed {username}: Following: {user_details['following_count']}, Starred Repos: {user_details['starred_repos_count']} ({i}/{total_count}).")
            except Exception as exc:
                logging.error(f"🚨 {username} generated an exception: {exc}")

    # Save data to CSV files using the unified save_csv function
    save_csv(user_details_data, 'user-details.csv', ['username', 'email', 'location', 'company', 'created_at', 'updated_at', 'followers_count', 'following_count', 'public_repos_count', 'starred_repos_count'])
    save_organizations(organizations_data, 'organizations.csv')
    save_followings(following_data, 'following.csv')
    save_repos(repos_data, 'repos.csv')
    logging.info("Data collection and saving completed.")

if __name__ == '__main__':
    main()