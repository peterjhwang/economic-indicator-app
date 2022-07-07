import pandas as pd
import time

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s').strftime('%Y-%m-01')

def getMarks(min_, max_):
    ''' Returns the marks for labeling. 
        Every Nth value will be used.
    '''

    result = {}
    for date in [min_, max_]:
        # Append value to dict
        result[unixTimeMillis(date)] = str(date.strftime('%Y'))

    return result