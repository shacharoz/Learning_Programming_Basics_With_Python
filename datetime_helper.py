import datetime

FORMAT = '%d-%m-%Y %H:%M:%S'


""" Returns the current date and time as a string with a standard format """
def date_now():
    return datetime.datetime.utcnow().strftime(FORMAT)


""" Returns the given string in standard format as a datetime object """
def to_datetime_obj(date_string):
    return datetime.datetime.strptime(date_string, FORMAT)
