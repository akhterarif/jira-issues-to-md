class Settings(object):
    """
    Initiates all settings here
    """
    JIRA_USERNAME = 'your-jira-username'
    JIRA_PASSWORD = 'your-jira-passwaord'
    SPRINT_ID = 222
    BOARD_ID = 20
    EPIC_ID = 'JIRA-1010'
    OUTPUT_FILE_NAME = 'output.md'
    FORMAT_FILE_NAME = 'format.md'
    OUTPUT_TIME_FORMAT = '%d, %B %Y'

    def __init__(self):
        super(Settings, self).__init__()

    def get_output_format(self):
        print('reading {format_file} file...'.format(
            format_file=self.FORMAT_FILE_NAME))
        with open(self.FORMAT_FILE_NAME, 'r') as format_file:
            format_str = str(format_file.read())
        return format_str
