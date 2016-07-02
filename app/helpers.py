import arrow

class TimeHelper():

    @staticmethod
    def format_time(timestamp):
        localtime = arrow.get(timestamp)
        return localtime.format('HH:mm - dddd D MMMM YYYY')

    @staticmethod
    def get_day(timestamp):
        time = arrow.get(timestamp)
        return time.format('D')

    @staticmethod
    def get_month(timestamp):
        time = arrow.get(timestamp)
        month_id = time.format('MM')
        month = time.format('MMMM')
        return dict(month=month, month_id=month_id)

    @staticmethod
    def get_year(timestamp):
        time = arrow.get(timestamp)
        return time.format('YYYY')
