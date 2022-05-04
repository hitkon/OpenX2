"""Task 2

This program takes 3 arguments. --calendars, --duration-in-minutes and minumum-people.
The algorithm inverts busy intervals into free intervals, and adds their beginnings and endings to date_list.
Sorts the list.
Then goes throw it saves all beginnings

"""

import sys
import os
import argparse
import pandas as pd
import functools
import datetime
import unittest

def CreateParser():
    """This function parses input args"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--calendars')
    parser.add_argument('--duration-in-minutes')
    parser.add_argument('--minumum-people')
    return parser

def next_date(date, minutes = 0, seconds = 0):
    """The function returns the date and time for a given minute and seconds more"""
    cur_date = pd.Timestamp(date)
    next_date = cur_date + pd.Timedelta(seconds=seconds, minutes=minutes)
    return next_date.strftime("%Y-%m-%d %H:%M:%S")

def prev_date(date, minutes = 0, seconds = 0):
    """The function returns the date and time for a given minute and seconds less"""
    cur_date = pd.Timestamp(date)
    prev_date = cur_date - pd.Timedelta(seconds=seconds, minutes=minutes)
    return prev_date.strftime("%Y-%m-%d %H:%M:%S")

def is_interval_fit(a, b, duration_in_minutes):
    """The function returns is b - a > given minutes"""
    if next_date(a[0], minutes=duration_in_minutes, seconds=-1) <= b[0]:
        return True
    return False


def is_fit(beginning_list, date, duration_in_minutes, min_people):
    """The function takes list of beginnings of free open intervals,
     one date of closing interval, duration in minutes and min people.
    It looks for the earliest fit date and time.
    Returns maxdate if there isn't any.
    """
    if len(beginning_list) < min_people:  # If there are fewer beginnings than min_people, there isn't any answer.
        return "3000-01-01 00:00:00"
    for i in range(min_people-1, len(beginning_list)):
        # Check if there is interval fits our requirements then return it
        if is_interval_fit(beginning_list[i], date, duration_in_minutes):
            return beginning_list[i][0]
    return "3000-01-01 00:00:00"


def find_time_in_table(date_list, duration_in_minutes, min_people):
    """The function takes sorted list of free intervals, duration in minutes and minimum people.
    The algorithm goes throw a list of free intervals, saves the open intervals and,
    when it finds a close of interval, it starts function is_fit() with appropriate args.
    In the result it returns the earliest fit date and time.
    """
    beginning_list = []
    ans = "3000-01-01 00:00:00"
    for date in date_list:
        if date[1] == 0:  # If it is a beginning of any free interval, then add it to already opens
            beginning_list.append(date)
        else:
            # If it is an ending of any free interval, try to improve our answer.
            ans = min(ans, is_fit(beginning_list, date, duration_in_minutes, min_people))
            if ans != "3000-01-01 00:00:00":
                return ans
            ind = -1
            for i in range(len(beginning_list)):
                if beginning_list[i][2] == date[2]:
                    ind = i
            beginning_list.pop(ind) # Remove beginning which met its ending.

    return ans



def date_parser(date_list, date):
    """The function makes all dates and times to one format, and adds it to date list"""
    if date == "":
        return
    candidates = date.split(' - ')
    if len(candidates) == 1:  # In case if there is a date without a time
        candidates[0] = candidates[0].strip()
        candidates.append(candidates[0])
        candidates[0] = candidates[0] + " 00:00:00"
        candidates[1] = candidates[1] + " 23:59:59"

    date_list.append([candidates[0], candidates[1]])


# Comfortable adding interval
def add_date_to_list(date_list, interval, index):
    """This function adds beginning and ending of interval to date list"""
    date_list.append([interval[0], 0, index])
    date_list.append([interval[1], 1, index])


# Find all free intervals instead of busy intervals
def calendar_parser(date_list, date_lines, index, date_now):
    """The function takes as args date_list, calendar(date_lines), index of calendar, and now date.
    As a result it finds all free intervals in calendar between now and max date, and adds it to date list"""
    busy_intervals = []
    for date in date_lines:
        date_parser(busy_intervals, date)  # Make all dates in one format

    busy_intervals.sort()  # Unnecessary if intervals in calendars are ordered

    prev = date_now  # Save a previous end of busy interval.
                        # At the start it equals to date_now because of looking back make no sense
    for interval in busy_intervals:
        if interval[1] > prev: # If interval isn't from left side of prev
            if interval[0] > prev:  # If free interval exists, add it
                add_date_to_list(date_list, [prev, prev_date(interval[0], seconds=1)], index)
            prev = next_date(interval[1], seconds=1)  # A new free interval starts in 1 second after previous busy interval

    add_date_to_list(date_list, [prev, "3000-01-01 00:00:00"], index)
    # There is always one free interval, which starts from end of last busy interval and ends in max date


def get_now_date_and_time_to_str():
    """Returns now date time as appropriate string"""
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

def task():
    """The function parses args, reads all calendars,
     transforms it by calendar parser in list of dates as beginnings and endings of free intervals.
     Then sort this list by date and print an answer as a result of function find_time_in_table()"""
    parser = CreateParser()  # Parse args
    namespace = parser.parse_args(sys.argv[1:])
    calendars = namespace.calendars
    duration_in_minutes = namespace.duration_in_minutes
    minumum_people = namespace.minumum_people

    try:  # Check if minumum_people does not convert to int
        int(minumum_people)
    except:
        print("Wrong format of number of people")
        return

    try:  # Check if duration does not convert to int
        int(duration_in_minutes)
    except:
        print("Wrong format of duration")

    if int(minumum_people) < 1:  # Check if minumum_people is impossible
        print("Wrong number of peoplle")
        return

    if int(duration_in_minutes) < 1: # Check if duration is impossible
        print("Wrong duration")
        return

    if not os.path.exists(calendars):  # If path doesn't exist
        print("Can't find directory")
        return

    calendars_list = os.listdir(calendars)  # Look for directory of calendars

    if len(calendars_list) == 0:  # If calendars directory is empty
        print(get_now_date_and_time_to_str())
        return

    date_list = []
    date_now = get_now_date_and_time_to_str()  # Get now date and time

    date_now = "2022-07-01 09:00:00"
    # date_now = get_now_date_and_time_to_str()

    for i in range(len(calendars_list)):  # Read all calendars and add it free intervals to date_list
        with open(calendars + "/" + calendars_list[i], 'r') as file:
            calendar_parser(date_list, file.readlines(), i, date_now)

    date_list.sort()  # Function required sorted list of dates
    print(date_list)
    print(find_time_in_table(date_list, int(duration_in_minutes), int(minumum_people)))


if __name__ == '__main__':
    task()
