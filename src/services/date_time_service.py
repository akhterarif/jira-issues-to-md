from datetime import date, datetime, timedelta


class DateTimeService(object):
    """
    Datetime services
    """
    DATE_FORMAT = "%d-%m-%Y"
    DATETIME_FORMAT = "%d/%b/%y %I:%M %p"
    OUTPUT_DATETIME_FORMAT = '%d, %B %Y'

    def __init__(self):
        super(DateTimeService, self).__init__()

    def get_datetime_obj(self, datetime_str, datetime_format=None):
        if datetime_format is None:
            datetime_format = self.DATETIME_FORMAT
        return datetime.strptime(datetime_str, datetime_format)

    def get_datetime_str(self, datetime_obj, datetime_format=None):
        if datetime_format is None:
            datetime_format = self.OUTPUT_DATETIME_FORMAT
        return str(datetime_obj.strftime(datetime_format))

    def get_datetime_str_from_str_to_str(self,
                                         from_datetime_str,
                                         from_datetime_format=None,
                                         to_datetime_format=None):

        dt_obj = self.get_datetime_obj(datetime_str=from_datetime_str,
                                       datetime_format=from_datetime_format)
        return self.get_datetime_str(datetime_obj=dt_obj,
                                     datetime_format=to_datetime_format)

    def add_days_to_date(self, datetime_str, days=None, datetime_format=None):
        if days is None:
            days = 0
        given_date_obj = self.get_datetime_obj(datetime_str=datetime_str,
                                               datetime_format=datetime_format)

        date_obj = given_date_obj + timedelta(days=days)
        return self.get_datetime_str(datetime_obj=date_obj,
                                     datetime_format=datetime_format)
