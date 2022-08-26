# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import re
import os
from datetime import datetime
from matplotlib import dates

def DelmagToFloat(strDelmag): # 입력 : 헤더 29번, 출력 : 헤더 29번의 실수 값
    strList = re.findall("\d+", strDelmag)
    strValue = strList[0] + '.' + strList[1]
    return float(strValue)

def StrToDatetime(strTime): # 입력 : 시간 문자열, 출력 : dateTime
    dateTime = datetime.strptime(strTime, '%H:%M:%S')
    return dateTime

# 파일 리스트 만들기
path_dir = 'D:/Temp/20220503-yz-boo'
file_list = os.listdir(path_dir)
file_list_fits = [file for file in file_list if file.endswith('.fits') and file[0] == 'c']

# R, V filter의 Delmag과 Time 리스트 만들기
delmag_V = []
delmag_R = []
time_V = []
time_R = []
for fits_file in file_list_fits:
    fits_file_dir = path_dir + '/' + fits_file
    with fits.open(fits_file_dir) as hdul:
        hdr = hdul[0].header
        if DelmagToFloat(hdr[29]) == 0:
            continue
        if hdr['FILTER'] == 'R':
            delmag_R.append(DelmagToFloat(hdr[29]))
            print(DelmagToFloat(hdr[29]))
            time_R.append(StrToDatetime(hdr['TIME-OBS']))
        elif hdr['FILTER'] == 'V':
            delmag_V.append(DelmagToFloat(hdr[29]))
            print(DelmagToFloat(hdr[29]))
            time_V.append(StrToDatetime(hdr['TIME-OBS']))            

# Create figure
fig = plt.figure(figsize=(12, 8))

# Define DataFrame
df_V = pd.DataFrame({'time': np.array(time_V), 'delmag': delmag_V})
df_R = pd.DataFrame({'time': np.array(time_R), 'delmag': delmag_R})

# Scatter time series
plt.scatter(df_V.time, df_V.delmag, label='V Filter', linewidth=1)
plt.scatter(df_R.time, df_R.delmag, label='R Filter', linewidth=1)
plt.xticks(rotation=90)
ax = plt.gca()
ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
ax.xaxis.set_major_locator(dates.HourLocator(interval=1))

# Add title and labels
plt.title('Object-Comparison')
ax.title.set_size(30)
plt.xlabel('Hour')
ax.xaxis.label.set_size(16)
plt.ylabel('Comparison')
ax.yaxis.label.set_size(16)

# Add legend
plt.legend(loc='upper left')

# Auto space
plt.tight_layout()

# Display plot
plt.show()