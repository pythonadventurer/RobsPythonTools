from datetime import datetime, timezone
import dateutil.parser
import pytz
from time import sleep

"""
Tools for working with dates and times
"""


def iso_dt(iso_str):
    """Convert an ISO 8601 date/time string to a datetime object. Once it's
    in this format, it can be parsed easily

    Parameters
    ----------
    iso_str : str
        A string representing a date and time in ISO 8601 format. Example:
            '2019-11-24T01:27:29-05:00'

    Returns
    -------
    a datetime.datetime object
    """
    return dateutil.parser.parse(iso_str)


def dt_local(utc_dt):
    """Convert a UTC datetime to a local time string in the format
       YYYY-MM-DD HH:MM:SS.

    Parameters
    ----------
    utc_dt: datetime
        The datetime object to be converted.
            Example: 2019-11-24T01:27:29-05:00

    Returns
    -------
    String representation of the localized date time.
        Example:
        Localized date/time based on the given UTC offset of -5 hours,
        which is US Eastern Time: 2019-11-23 20:27:29
    """

    # I believe setting time zone to None forces a default to the local tz.
    converted_time = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    # strips off the time zone offset
    converted_time_str = str(converted_time)[:19]

    return converted_time_str


def iso_local(iso_str):
    """
    Combine both functions above to convert an ISO 8601 date time directly to
    a local time string.

    """
    return dt_local(iso_dt(iso_str))


def time_diff(start, end):
    """Calculate the difference between two datetimes in days, hours, minutes
    and seconds.

    Parameters
    ----------
    start : datetime object.
    end : datetime object

    Returns

    """
    diff = end - start

    days = diff.days

    hours = int((diff.seconds - diff.seconds % 3600)/3600)

    minutes =  int((diff.seconds - hours * 3600)/60)

    seconds = int((diff.seconds - hours * 3600 - minutes * 60))

    return f"{days} days {hours} hours {minutes} min {seconds} sec"


def timestamp():
    """Return the current time on the US East Coast as a timezone aware
    string in ISO format.
    """
    my_time_utc = datetime.utcnow()

    timezone = pytz.timezone("America/New_York")

    my_time_loc = timezone.localize((my_time_utc))

    return my_time_loc.strftime("%Y-%m-%dT%H:%M:%S%z")

def timestamp_short():
    """
    Return the current local time date and time in the format
    "YYYY-MM-DD-HH-MM-SS".
    """
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def date_fixer(date_str):
    """
    Converts a date-like string to 'YYYY-MM-DD' format.
    """
    return str(dateutil.parser.parse(date_str))[:10]


def count_down(seconds,message):
    print(f"{message} {seconds} seconds..", end=" ")
    
    for n in range(seconds,-1,-1):
        sleep(1)

        print(n,end=" ")

