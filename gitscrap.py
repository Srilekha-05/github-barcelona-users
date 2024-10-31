import requests
import csv
import os
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Define GitHub Token and headers
GITHUB_TOKEN = 'your_github_token_here'  # Replace with your GitHub token
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Define the path to the Google Drive folder
folder_path = '/content/drive/My Drive/github-scraper/'

# Create the directory if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Function to get users in Barcelona with over 100 followers
def get_users():
    users = []
    url = "https://api.github.com/search/users?q=location:Barcelona+followers:>100&per_page=100"
    while url:
        response = requests.get(url, headers=headers).json()
        users.extend(response.get('items', []))
        url = response.get('next', None)  # Handle pagination if necessary
    return users

# Function to get details of a single user
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    return requests.get(url, headers=headers).json()

# Function to get repositories of a user
def get_user_repos(username):
    repos = []
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    while url:
        response = requests.get(url, headers=headers).json()
        repos.extend(response)
        url = response.get('next', None)
    return repos[:500]  # Limit to the 500 most recent repos

# Save user data to CSV
def save_users_to_csv(users, path=f'{folder_path}users.csv'):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["login", "name", "company", "location", "email", "hireable", "bio", 
                         "public_repos", "followers", "following", "created_at"])
        for user in users:
            user_data = get_user_details(user['login'])
            writer.writerow([
                user_data['login'],
                user_data.get('name', ''),
                clean_company(user_data.get('company', '')),
                user_data.get('location', ''),
                user_data.get('email', ''),
                user_data.get('hireable', ''),
                user_data.get('bio', ''),
                user_data.get('public_repos', 0),
                user_data.get('followers', 0),
                user_data.get('following', 0),
                user_data.get('created_at', '')
            ])

# Save repository data to CSV
def save_repositories_to_csv(users, path=f'{folder_path}repositories.csv'):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["login", "full_name", "created_at", "stargazers_count", "watchers_count", 
                         "language", "has_projects", "has_wiki", "license_name"])
        for user in users:
            repos = get_user_repos(user['login'])
            for repo in repos:
                writer.writerow([
                    user['login'],
                    repo['full_name'],
                    repo['created_at'],
                    repo['stargazers_count'],
                    repo['watchers_count'],
                    repo['language'],
                    repo['has_projects'],
                    repo['has_wiki'],
                    repo.get('license', {}).get('name', '')
                ])

# Utility to clean company names
def clean_company(company):
    if company:
        return company.strip().lstrip('@').upper()
    return ""

# Main execution
users = get_users()
save_users_to_csv(users)
save_repositories_to_csv(users)
print("Data saved to Google Drive!")
