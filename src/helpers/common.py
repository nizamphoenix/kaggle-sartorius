import os
from datetime import timedelta
from time import localtime, strftime


def current_time():
    """
    Get the current time

    Return
    ------
    string
        current time in year-month-day hour-min-second format
    """
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def elapsed_time_to_str(elapsed):
    """
    Returns a difference in times

    Parameters
    ----------
    elapsed : int/float
        time difference in seconds

    Return
    ------
    string
        stringified time difference
    """
    return str(timedelta(seconds=elapsed))


def silent_remove(filename):
    """
    Removes a file without raising an error if the file doesn't exist

    Parameters
    ----------
    filename : string
        path of the file to be removed

    Return
    ------
    None
    """
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


def make_dirs_for_file(filename):
    """
    Create directories for a given file path if they do not exist

    Parameters
    ----------
    filename : string
        path of the file to create directories for

    Return
    ------
    None
    """
    make_dir = os.path.dirname(filename)
    if make_dir is not None and make_dir != "":
        os.makedirs(make_dir, exist_ok=True)


def sum_lists(inp):
    """
    Sums a list of lists

    Parameters
    ----------
    inp : list of lists
        list of lists of any dtype

    Return
    ------
    list
        sum of internal lists
    """
    ret = []
    for sublist in inp:
        ret += sublist
    return ret
