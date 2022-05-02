import sys
import os
import argparse
import pandas as pd
import functools

def CreateParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--calendars')
    parser.add_argument('--duration-in-minutes')
    parser.add_argument('--minumum-people')
    return parser

def next_date(date, minutes = 0, seconds = 0):
    cur_date = pd.Timestamp(date)
    next_date = cur_date + pd.Timedelta(seconds=seconds, minutes=minutes)

    #print(curDate.strftime("%Y-%m-%d %H:%M:%S"))
    return next_date.strftime("%Y-%m-%d %H:%M:%S")

def prev_date(date, minutes = 0, seconds = 0):
    cur_date = pd.Timestamp(date)
    prev_date = cur_date - pd.Timedelta(seconds=seconds, minutes=minutes)

    #print(curDate.strftime("%Y-%m-%d %H:%M:%S"))
    return prev_date.strftime("%Y-%m-%d %H:%M:%S")

def is_interval_fit(a, b, duration_in_minutes):
    if next_date(a[0], minutes=duration_in_minutes) <= b[0]:
        return True
    return False


def is_fit(beginning_list, date, duration_in_minutes, min_people):
    if len(beginning_list) < min_people:
        return "3000-01-01 00:00:00"
    for i in range(min_people-1, len(beginning_list)):
        if is_interval_fit(beginning_list[i], date, duration_in_minutes):
            return beginning_list[i][0]
    return "3000-01-01 00:00:00"


def find_time_in_table(date_list, duration_in_minutes, min_people):
    beginning_list = []
    ans = "3000-01-01 00:00:00"
    for date in date_list:
        if date[1] == 0:
            beginning_list.append(date)
        else:
            ans = min(ans, is_fit(beginning_list, date, duration_in_minutes, min_people))
            ind = -1
            for i in range(len(beginning_list)):
                if beginning_list[i][2] == date[2]:
                    ind = i
            beginning_list.pop(ind)

    return ans



def date_parser(date_list, date):
    if date == "":
        return
    candidates = date.split(' - ')
    if len(candidates) == 1:
        candidates[0] = candidates[0].strip()
        candidates.append(candidates[0])
        candidates[0] = candidates[0] + " 00:00:00"
        candidates[1] = candidates[1] + " 23:59:59"

    #print(candidates[0])
    date_list.append([candidates[0], candidates[1]])


def add_date_to_list(date_list, interval, index):
    date_list.append([interval[0], 0, index])
    date_list.append([interval[1], 1, index])

def calendar_parser(date_list, date_lines, index, date_now):
    busy_intervals = []
    for date in date_lines:
        date_parser(busy_intervals, date)

    busy_intervals.sort()
    prev = date_now
    for interval in busy_intervals:
        if interval[1] > prev:
            if interval[0] > prev:
                add_date_to_list(date_list, [prev, prev_date(interval[0], seconds=1)], index)
            prev = next_date(interval[1], seconds=1)

    add_date_to_list(date_list, [prev, "3000-01-01 00:00:00"], index)


def date_compare(a, b):
    if a[0] < b[0]:
        return -1
    elif a[0] > b[0]:
        return 1
    else:
        if a[1] > b[1]:
            return -1
        elif a[1] < b[1]:
            return 1
        else:
            return 0


if __name__ == '__main__':
    parser = CreateParser()
    namespace = parser.parse_args(sys.argv[1:])

    calendars = namespace.calendars
    duration_in_minutes = namespace.duration_in_minutes
    minumum_people = namespace.minumum_people

    calendars_list = os.listdir(calendars)

    date_list = []
    date_now = "2022-07-01 09:00:00"

    for i in range(len(calendars_list)):
        with open(calendars + "/" + calendars_list[i], 'r') as file:
            calendar_parser(date_list, file.readlines(), i, date_now)


    date_list.sort()

    print(date_list)
    print(find_time_in_table(date_list, int(duration_in_minutes), int(minumum_people)))
