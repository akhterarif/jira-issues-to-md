import sys
sys.path.insert(0, "./src")

from collections import Counter
from jira import JIRA
import re
import json

try:
    from settings import Settings
except ImportError:
    print('No Import')


class JiraServices(object):

    def __init__(self):
        options = {
            'server': 'https://wammumobi.atlassian.net',
            'basic_auth': (Settings.JIRA_USERNAME, Settings.JIRA_PASSWORD)
        }
        self.jira = JIRA(**options)

    def get_sprint_info(self, sprint_id):
        """
        Returns sprint info

        """
        sprint = self.jira.sprint(sprint_id)
        return sprint.raw

    def get_info_of_issue(self, issue_id):
        issue = self.jira.issue(id=issue_id)
        return issue.raw

    def get_issues_of_an_epic(self, epic_id):
        """
        Returns the issues of an epic
        """
        jql_str = '"epic link" = {epic_id}'.format(
            epic_id=epic_id, json_result=True)
        issues = self.jira.search_issues(
            jql_str=jql_str)
        issues_name_list = []
        for issue in issues:
            issue_info = self.get_info_of_issue(issue_id=issue.key)
            issues_name_list.append(issue_info)
        return issues_name_list
