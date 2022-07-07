import datetime
from math import modf
from math import trunc

def date_convert(type, value, convert_to):
    type = type.lower()
    convert_to = convert_to.lower()
    
    if type == 'date':
        if convert_to == 'jd':
            return date2jd(value)
        elif convert_to == 'mjd':
            return date2mjd(value)
        elif convert_to == 'doy':
            return date2doy(value)
    elif type == 'jd':
        if convert_to == 'date':
            return jd2date(value)
        elif convert_to == 'mjd':
            return jd2mjd(value)
        elif convert_to == 'doy':
            return jd2doy(value)
    elif type == 'mjd':
        if convert_to == 'date':
            return mjd2date(value)
        elif convert_to == 'jd':
            return mjd2jd(value)
        elif convert_to == 'doy':
            return mjd2doy(value)
    elif type == 'doy':
        if convert_to == 'date':
            return doy2date(value)
        elif convert_to == 'jd':
            return doy2jd(value)
        elif convert_to == 'mjd':
            return doy2mjd(value)
    else:
        return None

def date2jd(value):
    if not check_date(value):
        return None
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
    if not check_date(value):
        return None
    (year, month, day) = parse_date(value)
    doy = datetime.date(year, month, day).strftime('%j')
    doy = str(year)[-2:]+doy
    return doy

def jd2date(value):
    if not check_jd(value):
        return None
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
    if not check_jd(value):
        return None
    mjd = str(int(float(value) - 2400000.5))
    return mjd

def jd2doy(value):
    return date2doy(jd2date(value))

def mjd2date(value):
    return jd2date(mjd2jd(value))

def mjd2jd(value):
    if not check_mjd(value):
        return None
    jd = str(int(value) + 2400000.5)
    return jd

def mjd2doy(value):
    return date2doy(jd2date(mjd2jd(value)))

def doy2date(value):
    if not check_doy(value):
        return None
    (year, doy) = parse_doy(value)
    date = datetime.datetime.strptime(f'{year} {doy}', '%Y %j').strftime('%Y%m%d')
    return date
    
def doy2jd(value):
    return date2jd(doy2date(value))

def doy2mjd(value):
    return jd2mjd(date2jd(doy2date(value)))

def check_date(date):
    try:
        if len(date) != 8:
            raise
        datetime.date(int(date[:4]), int(date[4:6]), int(date[6:]))
        return True
    except:
        print('ERROR: Improper date value.')
        return False

def parse_date(date):
    return (int(date[:4]), int(date[4:6]), int(date[6:]))

def check_jd(jd):
    try:
        jd = float(jd)
        if jd > 0:
            return True
    except:
        print('ERROR: Improper JD value.')
    return False

def check_mjd(mjd):
    try:
        mjd = int(mjd)
        if mjd > 0:
            return True
    except:
        print('ERROR: Improper MJD value.')
    return False

def check_doy(doy):
    if len(doy) == 5:
        if int(doy[:2]) > 0:
            if int(doy[2:]) >= 0 and int(doy[2:]) <= 366:
                return True
    print('ERROR: Improper DOY value.')
    return False

def parse_doy(doy):
    yy = int(doy[:2])
    if yy > 50:
        year = 1900 + yy
    else:
        year = 2000 + yy
    return (year, int(doy[2:]))

def test_all():
    pass ## To be developed.

if __name__=='__main__':
    import sys
    if sys.argv[1] == 'test':
        print(test_all())
    else:
        type = sys.argv[1]
        value = sys.argv[2]
        convert_to = sys.argv[3]
        print(date_convert(type, value, convert_to))