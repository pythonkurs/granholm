#!/usr/bin/env python

from pandas import DataFrame, Series
from dateutil import parser
import requests
import getpass
import json
from collections import Counter

class ReadRepos(object):
    '''Reads github repositories into a pandas dataframe'''

    def __init__(self, username, password):
        # Github credentials
        self.username = username
        self.password = password

    def read_github_commits(self):
        '''Produce a DataFrame with commit messages of Pythonkurs repositories'''
        print 'Reading repositories:',
        # Initialize dictionary to make dataframe
        repo_dict = {}
        # Read Github API
        response = requests.get("https://api.github.com/orgs/pythonkurs/repos", auth=(self.username, self.password))
        repos =  json.loads(response.content)  # Couldn't get the json-method working for response, so I use the json module.
        for repo in repos:
            repo_name = repo['name']
            print repo_name,
            commit_response = requests.get("https://api.github.com/repos/pythonkurs/%s/commits" % (repo_name), auth=(self.username, self.password))
            commits = json.loads(commit_response.content)
            messages = []
            times = []
            # It seems, if at least one commit is made, commits has the type list
            if type(commits) == list:
                for commit in commits:
                    times.append(parser.parse(commit['commit']['author']['date']))
                    messages.append(commit['commit']['message'])
                repo_dict[repo_name] = Series(messages, index=times)
            else:
                # No commits...
                pass
        print ''
        self.df = DataFrame(repo_dict)


class DataFrameOfCommits(object):
    '''Takes a dataframe of github commits, calculates most common dates etc.'''

    def __init__(self, dataframe):
        self.df = dataframe
        self.weekday_list = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

    def most_common_day_for_commits(self):
        weekdays = []
        for row in self.df.iterrows():
            weekdays.append(row[0].weekday())
        c = Counter(weekdays)
        weekday_int = c.most_common()[0][0]  # The index of the most common weekday
        print 'The most common weekday for commits is: %s' % self.weekday_list[weekday_int]

    def most_common_hour_for_commits(self):
        hours = []
        for row in self.df.iterrows():
            hours.append(row[0].hour)
        c = Counter(hours)
        hour = c.most_common()[0][0]  # The int value of the most common hour
        print 'The most common hour for commits is: %s' % hour


def main():
    # Get github pass
    password = getpass.getpass()
    # Get github commits
    repos = ReadRepos('viktorg', password)
    repos.read_github_commits()
    # Count statistics from github commtis
    df_of_commits = DataFrameOfCommits(repos.df)
    df_of_commits.most_common_day_for_commits()
    df_of_commits.most_common_hour_for_commits()
    

if __name__ == '__main__':
    main()
    
