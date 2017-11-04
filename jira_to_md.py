#!/usr/bin/python

from src.settings import Settings
from src.services.jira_services import JiraServices
from src.services.date_time_service import DateTimeService


class JiraToMd(object):
    """
    Makes a .md file for current's epics issues list
    """
    REPLACE_STR_FROM_ISSUES_NAME = '[BACKEND] '
    PROJECT_MNGMNT_PERCENTAGE = 0.25

    def __init__(self):
        super(JiraToMd, self).__init__()
        sprint_id = int(input("Enter Sprint ID: "))
        epic_id = str(input("Enter EPIC ID: "))
        self.sprint_id = sprint_id
        self.epic_id = epic_id
        self.jira_service = JiraServices()
        self.settings = Settings()
        self.datetime_service = DateTimeService()
        self.make_md_file()

    def make_md_file(self):
        print("writing on {output} file...".format(
            output=self.settings.OUTPUT_FILE_NAME))
        with open(self.settings.OUTPUT_FILE_NAME, 'w') as output_file:
            output_str = self.get_formatted_str()
            output_file.write(output_str)
            print("output.md file made successfully.")

    def get_formatted_str(self, format_str=None):
        sprint_name = ''
        description_list = ''
        formal_sprint_start_date = ''
        sprint_start_date = ''
        formal_sprint_end_date = ''
        sprint_end_date = ''
        formal_qa_release_date = ''
        qa_release_date = ''
        formal_client_release_date = ''
        client_release_date = ''
        version = ''
        epic_id = ''
        spent_hrs = ''
        sprint_name = ''
        project = ''
        label = ''
        estimations_list = ''
        hrs_estimation_str = ''
        total_estimated_hrs = ''
        project_mng_hrs = ''
        total_estimated_hrs = ''
        project_mng_hrs = ''
        total_hrs = ''

        sprint_info = self.get_sprint_info()
        epic_info = self.get_epic_info()
        description_info = self.get_description_list()
        estimation_info = self.get_estimations_info()

        str_vars = {
            'sprint_name': sprint_info['sprint_name'],
            'description_list': description_info['description_list'],
            'formal_sprint_start_date': sprint_info['formal_sprint_start_date'],
            'sprint_start_date': sprint_info['sprint_start_date'],
            'formal_sprint_end_date': sprint_info['formal_sprint_end_date'],
            'sprint_end_date': sprint_info['sprint_end_date'],
            'formal_qa_release_date': sprint_info['formal_qa_release_date'],
            'qa_release_date': sprint_info['qa_release_date'],
            'formal_client_release_date': sprint_info['formal_client_release_date'],
            'client_release_date': sprint_info['client_release_date'],
            'version': epic_info['version'],
            'epic_id': epic_info['epic_id'],
            'spent_hrs': estimation_info['spent_hrs'],
            'project': epic_info['project'],
            'label': epic_info['label'],
            'estimations_list': estimation_info['estimations_list'],
            'hrs_estimation_str': estimation_info['hrs_estimation_str'],
            'total_estimated_hrs': estimation_info['total_estimated_hrs'],
            'project_mng_hrs': estimation_info['project_mng_hrs'],
            'total_hrs': estimation_info['total_hrs'],
        }

        if format_str is None:
            format_str = self.settings.get_output_format()
        formatted_str = format_str.format(**str_vars)
        return formatted_str

    def get_sprint_info(self):
        if self.sprint_id is not None:
            sprint_id = self.sprint_id
        else:
            sprint_id = self.settings.SPRINT_ID

        sprint = self.jira_service.get_sprint_info(
            sprint_id=sprint_id)
        sprint_name = sprint['name']
        sprint_start_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=sprint['startDate'])

        sprint_end_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=sprint['endDate'])

        formal_sprint_start_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=sprint_start_date,
            from_datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            to_datetime_format=self.datetime_service.DATE_FORMAT)
        formal_sprint_end_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=sprint_end_date,
            from_datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            to_datetime_format=self.datetime_service.DATE_FORMAT)

        qa_release_date = self.datetime_service.add_days_to_date(
            datetime_str=sprint_start_date,
            datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            days=8)
        formal_qa_release_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=qa_release_date,
            from_datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            to_datetime_format=self.datetime_service.DATE_FORMAT)

        client_release_date = self.datetime_service.add_days_to_date(
            datetime_str=sprint_end_date,
            datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            days=3)
        formal_client_release_date = self.datetime_service.get_datetime_str_from_str_to_str(
            from_datetime_str=client_release_date,
            from_datetime_format=self.datetime_service.OUTPUT_DATETIME_FORMAT,
            to_datetime_format=self.datetime_service.DATE_FORMAT)

        return {
            'sprint_name': sprint_name,
            'formal_sprint_start_date': formal_sprint_start_date,
            'sprint_start_date': sprint_start_date,
            'formal_sprint_end_date': formal_sprint_end_date,
            'sprint_end_date': sprint_end_date,
            'qa_release_date': qa_release_date,
            'formal_qa_release_date': formal_qa_release_date,
            'client_release_date': client_release_date,
            'formal_client_release_date': formal_client_release_date
        }

    def get_epic_info(self):
        if self.epic_id is not None:
            epic_id = self.epic_id
        else:
            epic_id = self.settings.EPIC_ID
        epic_info = self.jira_service.get_info_of_issue(
            issue_id=epic_id)
        return {
            'epic_id': epic_info['key'],
            'version': epic_info['fields']['fixVersions'][0]['name'],
            'project': epic_info['fields']['project']['name'],
            'label': epic_info['fields']['labels'][0],

        }

    def get_description_list(self):
        description_str = ''
        if self.epic_id is not None:
            epic_id = self.epic_id
        else:
            epic_id = self.settings.EPIC_ID
        epic_info = self.jira_service.get_info_of_issue(
            issue_id=epic_id)
        issues = self.jira_service.get_issues_of_an_epic(
            epic_id=epic_id)

        s_i = 1
        for issue in issues:
            summary = "{s_i}. {summary}\n".format(
                s_i=s_i,
                summary=issue['fields']['summary'].replace(
                    self.REPLACE_STR_FROM_ISSUES_NAME, '')
            )
            description_str += summary
            s_i += 1

        return {
            'description_list': description_str
        }

    def get_estimations_info(self):
        estimations_str = ''
        timetracker_list = []
        timetracker_estimated_seconds_list = []
        timetracker_remaining_seconds_list = []
        timetracker_hrs_list = []
        timetracker_hrs_str_list = []

        hrs_estimation_str = ''
        total_estimated_hrs = ''
        project_mng_hrs = ''
        total_hrs = ''
        spent_hrs = ''
        if self.epic_id is not None:
            epic_id = self.epic_id
        else:
            epic_id = self.settings.EPIC_ID
        epic_info = self.jira_service.get_info_of_issue(
            issue_id=epic_id)

        issues = self.jira_service.get_issues_of_an_epic(
            epic_id=epic_id)

        s_i = 1
        for issue in issues:
            issue_str = "{s_i}. {summary} `{estimated_hrs}`\n".format(
                s_i=s_i,
                summary=issue['fields']['summary'].replace(
                    self.REPLACE_STR_FROM_ISSUES_NAME, ''),
                estimated_hrs=issue['fields']['timetracking']['originalEstimate']
            )
            s_i += 1
            estimations_str += issue_str
            timetracker_estimated_seconds_list.append(
                int(issue['fields']['timetracking']['originalEstimateSeconds']))
            timetracker_remaining_seconds_list.append(
                int(issue['fields']['timetracking']['remainingEstimateSeconds']))
            timetracker_hrs_list.append(float(
                int(issue['fields']['timetracking']
                    ['originalEstimateSeconds']) / 3600.0))
            timetracker_hrs_str_list.append(str(
                float(
                    int(issue['fields']['timetracking']
                        ['originalEstimateSeconds']) / 3600.0)))

        hrs_estimation_str = '+'.join(timetracker_hrs_str_list)
        total_estimated_hrs = sum(timetracker_hrs_list)

        total_estimated_seconds = sum(timetracker_estimated_seconds_list)
        total_remaining_seconds = sum(timetracker_remaining_seconds_list)
        total_spent_seconds = total_estimated_seconds - total_remaining_seconds
        total_spent_hrs = float(total_spent_seconds / 3600.0)
        project_mng_hrs = float(total_estimated_hrs) * \
            self.PROJECT_MNGMNT_PERCENTAGE
        total_hrs = total_estimated_hrs + project_mng_hrs
        spent_hrs = total_spent_hrs

        return {
            'estimations_list': estimations_str,
            'hrs_estimation_str': hrs_estimation_str,
            'total_estimated_hrs': total_estimated_hrs,
            'project_mng_hrs': project_mng_hrs,
            'total_hrs': total_hrs,
            'spent_hrs': spent_hrs if spent_hrs else '?',
        }
