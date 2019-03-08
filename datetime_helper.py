import datetime

FORMAT = '%d-%m-%Y %H:%M:%S'


def date_now():
    """ Returns the current date and time as a string with a standard format """
    return datetime.datetime.utcnow().strftime(FORMAT)


def to_datetime_obj(date_string):
    """
    Returns the given string in standard format as a datetime object

    :param date_string: The string to be converter into a datetime object
    """
    return datetime.datetime.strptime(date_string, FORMAT)
