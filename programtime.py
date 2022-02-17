#!/usr/bin/env python3
#This module stores the code for the dateTime methods
from datetime import date, time, datetime

def getStartTime():
    startTime = datetime.now()
    formatted_start = datetime.strftime(startTime, "%I:%M:%S")
    print("Start time: {}".format(formatted_start))
    return startTime


def getEndTime():
    stopTime = datetime.now()
    formatted_end = datetime.strftime(stopTime, "%I:%M:%S")
    print("Stop Time: {}".format(formatted_end))
    return stopTime


def getElapsedTime(stopTime, startTime):
    elapsed_str = stopTime - startTime
    
    minutes = elapsed_str.seconds // 60
    seconds = elapsed_str.seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    formatted_str = time(hours, minutes, seconds)

    print("Elapsed time: {}".format(formatted_str))
