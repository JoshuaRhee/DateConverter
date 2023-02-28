# **DateConverter**

## Information:
* This function converts a date to a different format.
* All inputs and outputs are string.
* Both upper cases, lower cases, and mixed are usable.
* Every combination between the following formats are available.
  - Date (YYYYMMDD)
  - Modified julian date, MJD
  - Julian day, JD
  - Day-of-year, DOY (YYDDD)
  - GPS week, GPSW (WWWWD)


## Usage:
* To use in python code:
> from convert_date import convert_date\
> \
> result = convert_date('DATE','20230228','MJD')

* To use on cmd:
> python convert_date.py 'DATE' '20230228' 'MJD'

* To test on cmd:
> python convert_date.py test
