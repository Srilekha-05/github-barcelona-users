# GitHub Users in Barcelona

This repository contains data about GitHub users in Barcelona with over 100 followers and their repositories.

1. I used the GitHub API to gather information on users from Barcelona with over 100 followers. The process involved fetching their profiles and repository details.
2. A notable observation was that many developers do not leverage wikis or project boards in their repositories.  This underutilization indicates a missed 
   opportunity for enhancing project collaboration and documentation.
3. Developers should use wikis and project boards more effectively to enhance collaboration and documentation in their projects.

## Files

1. `users.csv`: Contains information about 337 GitHub users in Barcelona with over 100 followers
2. `repositories.csv`: Contains information about 27172 public repositories from these users
3. `gitscrap.py`: Python script used to collect this data

## Data Collection

- Data collected using GitHub API
- Date of collection: 2024-10-31
- Only included users with 100+ followers
- Up to 500 most recently pushed repositories per user
