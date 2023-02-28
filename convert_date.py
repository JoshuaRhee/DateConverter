## Created by JHR
## Version 2.1
## - GPS week added.
## - check format with re
## - test added.

import datetime
from math import modf
from math import trunc
import re

def convert_date(type, value, convert_to):
    type = type.lower()
    convert_to = convert_to.lower()
    
    if check_format(type, value):
        if type == 'date':
            if convert_to == 'jd':
                return date2jd(value)
            elif convert_to == 'mjd':
                return date2mjd(value)
            elif convert_to == 'doy':
                return date2doy(value)
            elif convert_to == 'gpsw':
                return date2gpsw(value)
        elif type == 'jd':
            if convert_to == 'date':
                return jd2date(value)
            elif convert_to == 'mjd':
                return jd2mjd(value)
            elif convert_to == 'doy':
                return jd2doy(value)
            elif convert_to == 'gpsw':
                return jd2gpsw(value)
        elif type == 'mjd':
            if convert_to == 'date':
                return mjd2date(value)
            elif convert_to == 'jd':
                return mjd2jd(value)
            elif convert_to == 'doy':
                return mjd2doy(value)
            elif convert_to == 'gpsw':
                return mjd2gpsw(value)
        elif type == 'doy':
            if convert_to == 'date':
                return doy2date(value)
            elif convert_to == 'jd':
                return doy2jd(value)
            elif convert_to == 'mjd':
                return doy2mjd(value)
            elif convert_to == 'gpsw':
                return doy2gpsw(value)
        elif type == 'gpsw':
            if convert_to == 'date':
                return gpsw2date(value)
            elif convert_to == 'jd':
                return gpsw2jd(value)
            elif convert_to == 'mjd':
                return gpsw2mjd(value)
            elif convert_to == 'doy':
                return gpsw2doy(value)
    return None

def date2jd(value):
    (year, month, day) = parse_date(value)
    if month == 1 or month == 2:
        yearp = year-1
        monthp = month+12
    else:
        yearp = year
        monthp = month
        
    # Now this checks where we are in relation to October 15, 1582, the beginning of the Gregorian calendar.
    if ((year < 1582) or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day < 15)): # before start of Gregorian calendar
        B = 0
    else: # after start of Gregorian calendar
        A = int(yearp / 100.)
        B = 2 - A + int(A / 4.)
        
    if yearp < 0:
        C = int((365.25 * yearp) - 0.75)
    else:
        C = int(365.25 * yearp)
    D = int(30.6001 * (monthp + 1))
    
    jd = str(B + C + D + day + 1720994.5)
    return jd
    
def date2mjd(value):
    return jd2mjd(date2jd(value))

def date2doy(value):
    (year, month, day) = parse_date(value)
    doy = datetime.date(year, month, day).strftime('%j')
    doy = str(year)[-2:]+doy
    return doy

def date2gpsw(value):
    epoch0 = datetime.datetime.strptime("19800106","%Y%m%d")
    epoch1 = datetime.datetime.strptime(value, "%Y%m%d")
    dt = epoch1-epoch0
    return str(int(dt.days/7)) + str(dt.days%7)

def jd2date(value):
    jd = float(value)
    jd = jd + 0.5
    F, I = modf(jd)
    I = int(I)
    A = trunc((I - 1867216.25)/36524.25)
    if I > 2299160:
        B = I + 1 + A - trunc(A / 4.)
    else:
        B = I    
    C = B + 1524
    D = trunc((C - 122.1) / 365.25)
    E = trunc(365.25 * D)
    G = trunc((C - E) / 30.6001)
    day = int(C - E + F - trunc(30.6001 * G))
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
    date = str(year).zfill(4)+str(month).zfill(2)+str(day).zfill(2)
    return date

def jd2mjd(value):
    mjd = str(int(float(value) - 2400000.5))
    return mjd

def jd2doy(value):
    return date2doy(jd2date(value))

def jd2gpsw(value):
    return date2gpsw(jd2date(value))

def mjd2date(value):
    return jd2date(mjd2jd(value))

def mjd2jd(value):
    jd = str(int(value) + 2400000.5)
    return jd

def mjd2doy(value):
    return date2doy(jd2date(mjd2jd(value)))

def mjd2gpsw(value):
    return date2gpsw(mjd2date(value))

def doy2date(value):
    (year, doy) = parse_doy(value)
    date = datetime.datetime.strptime(f'{year} {doy}', '%Y %j').strftime('%Y%m%d')
    return date
    
def doy2jd(value):
    return date2jd(doy2date(value))

def doy2mjd(value):
    return jd2mjd(date2jd(doy2date(value)))

def doy2gpsw(value):
    return date2gpsw(doy2date(value))

def gpsw2date(value):
    (week, day) = parse_gpsw(value)
    epoch0 = datetime.datetime.strptime("1980-01-06", "%Y-%m-%d")
    dt = datetime.timedelta(days=(week*7)+day)
    return datetime.datetime.strftime(epoch0+dt, "%Y%m%d")

def gpsw2jd(value):
    return date2jd(gpsw2date(value))

def gpsw2mjd(value):
    return date2mjd(gpsw2date(value))

def gpsw2doy(value):
    return date2doy(gpsw2date(value))

def check_format(type, value):
    if type == 'date':
        r = re.compile('\d\d\d\d\d\d\d\d')
    elif type == 'jd':
        r = re.compile('\d+[.]?\d+')
    elif type == 'mjd':
        r = re.compile('\d+')
    elif type == 'doy':
        r = re.compile('\d\d[0-3]\d\d')
    elif type == 'gpsw':
        r = re.compile('\d\d\d\d[0-6]')
    else:
        print(f'ERROR: {type} is not a supported type.')
        return False
    if r.match(value):
        return True
    else:
        print(f'ERROR: {value} is not a proper value.')
        return False
    
def parse_date(date):
    return (int(date[:4]), int(date[4:6]), int(date[6:]))

def parse_doy(doy):
    yy = int(doy[:2])
    if yy > 50:
        year = 1900 + yy
    else:
        year = 2000 + yy
    return (year, int(doy[2:]))

def parse_gpsw(gpsw):
    return (int(gpsw[:4]), int(gpsw[4]))

def test_all():
    typelist = ['date','jd','mjd','doy','gpsw']
    answer = ['20230101','2459945.5','59945','23001','22430']
    for i, type in enumerate(typelist):
        for j, convert_to in enumerate(typelist):
            if type != convert_to:
                if answer[j] == convert_date(type, answer[i], convert_to):
                    print(f'OK: [{type}, {answer[i]}, {convert_to}] {convert_date(type, answer[i], convert_to)} == {answer[j]}')
                else:
                    print(f'Wrong: [{type}, {answer[i]}, {convert_to}] {convert_date(type, answer[i], convert_to)} != {answer[j]}')    

## Running test on console (for example):
## python convert_date date 220010 mjd
if __name__=='__main__':
    import sys
    if sys.argv[1] == 'test':
        test_all()
    else:
        type = sys.argv[1]
        value = sys.argv[2]
        convert_to = sys.argv[3]
        print(convert_date(type, value, convert_to))