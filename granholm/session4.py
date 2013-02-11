#!/usr/bin/env python

from pandas import DataFrame, Series
from dateutil import parser
import requests
import getpass
import json

class ReadRepos(object):

    def __init__(username, password):
        # Github credentials
        self.username = username
        self.password = password

    def read_github_commits():
        '''Produce a DataFrame with commit messages of Pythonkurs repositories'''
        print 'Read through the pythonkurs repositories, store commit messages and times.'
        print 'Repository:'
        # Initialize dictionary to make dataframe
        repo_dict = {}
        # Read Github API
        response = requests.get("https://api.github.com/orgs/pythonkurs/repos", auth=(self.username, self.password))
        repos =  json.loads(response.content)  # Couldn't get the json-method working for response, so I use the json module.
        for repo in repos:
            repo_name = repo['name']
            print repo_name
            commit_response = requests.get("https://api.github.com/repos/pythonkurs/%s/commits" % (repo_name), auth=(self.username, self.password))
            commits = json.loads(commit_response.content)
            messages = []
            times = []
            # It seems, if at least one commit is made, commits has the type list
            if type(commits) == list:
                for commit in commits:
                    times.append(commit['commit']['author']['date'])
                    messages.append(commit['commit']['message'])
                repo_dict[repo_name] = Series(messages, index=times)
            else:
                # No commits...
                pass
        self.df = DataFrame(repo_dict)

class MostCommonHour(object):


def main():
    password = getpass.getpass()
    repositories = ReadRepos('viktorg', password)
    repos.read_github_commits()
    

if __name__ == '__main__':
    main()
    
