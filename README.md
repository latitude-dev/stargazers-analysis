# Latitude Stargazers Analysis

This is a project to know better the audience of your Github repository. It retrieves the information from your stargazers using the Github API with a Python script and then generates a Latitude app to analyze it.

## Demo

You can find a live demo of this project at the following URL: [Live Demo →](https://repo-analysis-new-alfred.latitude.page/)

## Developing

### Initial requirements

- To start developing in this project, first make sure you have Node.js >= 18 installed. Then install the Latitude CLI:
    ```
    npm install -g @latitude-data/cli
    ```
- To run the script make sure you have Python installed. You can check the official page here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Generate a GitHub Access Token to authenticate you and the GitHub API later. You can generate it from [https://github.com/settings/tokens](https://github.com/settings/tokens)
- In the file fetch_stargazers_data.py replace the repo owner and repo name in lines 14 and 15 with the info of the repo you want to analyze. For example, for [github.com/latitude-dev/latitude/](https://github.com/latitude-dev/latitude/) would be like this:
    
    ```
    14 REPO_OWNER = 'latitude-dev'
    15 REPO_NAME = 'latitude'
    ```

### Running the script

1. Clone **the repo [pending]**
2. Open the terminal and go to the root of the cloned repo.
3. Run `pip install requests`
4. Then, run `export GITHUB_TOKEN='YOUR_TOKEN_HERE’`. Replace YOUR_TOKEN_HERE with the token you generated earlier.
5. Finally, run `python3 fetch_stargazers.py`
6. Important - the script may take a long time to complete. ~500 stargazers took us ~2 hours for reference.

When it is finished, it will save 4 .csv files in the queries folder, which is where the sources must be to analyze the data with Latitude. You can open the .csv files to see if the data is there.

### Initialize the Latitude app

To see the application with your project, run `latitude dev` from the terminal at the root of the project.

### Sharing with the team

So far the project is running locally on your machine, but you probably want to share the information with your team. You have 2 options:

- Deploy it yourself. You can follow the docs [here](https://docs.latitude.so/guides/deploy/latitude_cloud).
- Or just run `latitude deploy` and we'll manage to deploy it in our cloud and give you a URL to easily share it. 

## Documentation

To learn more about using Latitude, check out the [main repository](https://github.com/latitude-dev/latitude).
