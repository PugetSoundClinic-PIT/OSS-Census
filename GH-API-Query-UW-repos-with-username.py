# We scraped usernames associated with UW. 
# We already queried the GitHub public API to gather profile metadata for these users.
#### NOTE: profile metadata for each user already contains a url to that user's repos. Example from our data: https://api.github.com/users/shirley1988/repos
# Now we will use the usernames to gather information on these users' repositories.

# There are conditions that determine which repositories we collect from users:
# fork == FALSE OR stargazers_count > 0 OR watchers_count > 0 OR forks_count > 0




# **** Note: Uncomment and specify in the last line your filepath to save final CSV 

# Import libraries
import requests
import time
import pandas as pd


# Import known UW github usernames from OSS repository
usernames = pd.read_csv("https://raw.githubusercontent.com/PugetSoundClinic-PIT/OSS-Census/main/20230413-GHusernames.csv",index_col=0)

# The imported csv has 2 columns. Take just the column with usernames, convert to a list for looping through api query
usernames = usernames["0"].values.tolist()


# Create an empty list where the repo's which meet our conditions will be stored
target_repos = []

# Collect repository info for each known username
for username in usernames:
    # Make an API request to get the repositories for each user
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    
    if response.status_code == 200:
        repositories = response.json()
        
        for repository in repositories:
            # Create variables from the json response so that we can save them into a dataframe later
            owner_details = repository['owner']
            owner_login = owner_details['login']
            repo_name = repository['name']
            repo_url = repository['html_url']
            description = repository['description']
            fork = repository['fork']
            stargazers_count = repository['stargazers_count']
            watchers_count = repository['watchers_count']
            forks_count = repository['forks_count']
            license = repository['license']
            language = repository['language']
            created_at = repository['created_at']
            updated_at = repository['updated_at']
            has_issues = repository['has_issues']
            has_projects = repository['has_projects']
            has_downloads = repository['has_downloads']
            has_wiki = repository['has_wiki']
            has_pages = repository['has_pages']
            has_discussions = repository['has_discussions']
            
            
            # A repository must meet one of these conditions for us to save its details
            if repository['fork'] == 'false' or repository['stargazers_count'] > 0 or repository['watchers_count'] > 0 or repository['forks_count'] > 0:
                #print(repo_name)
                target_repos.append(
                    {
                        "owner": owner_login,
                        "repo_name": repo_name,
                        "repo_url": repo_url,
                        "description": description,
                        "fork": fork,
                        "stargazers_count": stargazers_count,
                        "watchers_count": watchers_count,
                        "forks_count": forks_count,
                        "license": license,
                        "languages": language,
                        "created_at": created_at,
                        "updated_at": updated_at,
                        "has_issues": has_issues,
                        "has_projects": has_projects,
                        "has_downloads": has_downloads,
                        "has_wiki": has_wiki,
                        "has_pages": has_pages,
                        "has_discussions": has_discussions,
                    }
                )

    else:
        print(f"Failed to retrieve repositories for {username}. Status code: {response.status_code}")
        
    #print(target_repos)
    time.sleep(30)


##### Once the data collection is finished #####

# Convert the list into a pretty dataframe
target_repos_df = pd.DataFrame.from_dict(target_repos)

#print(target_repos_df.head(10))    

# What are the dimensions of our complete profile_data_df? How many results did we get?
target_repos_df.shape

# Save the complete df
#profile_data_df.to_csv("~/filepath-goes-here/20230530-UW-GHrepositories-conditions.csv")
