import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd

# 지수 이동 평균 공식을 이용해 다음 예측 값 리턴
def PredictaedValue(alpha, t, tau):
    if alpha == 0:
        newTau = tau
    elif alpha == 1:
        newTau = t
    else:
        newTau = alpha*t + (1 - alpha)*tau
    
    return newTau

# 실제 값들로 이루어진 data list에 지수 이동 평균을 이용해 예측 값들의 list 리턴
def ExponentialAveraging(dataList, alpha, initialTau):
    predictedList = []
    
    for data in dataList:
        if not predictedList:
            predictedList.append(PredictaedValue(alpha, data, initialTau))
        else:
            predictedList.append(PredictaedValue(alpha, data, predictedList[-1]))
        
    return predictedList

# Create figure
fig = plt.figure(figsize=(12, 8))

# Define List
trueDataDateList = []
predictedDataDateList = []
trueDataPriceList = [864, 863, 835, 795, 723, 633, 558, 557, 543, 543, 507, 495] # 단위는 1천원
predictedDataPriceList = ExponentialAveraging(trueDataPriceList, 0.5, 800) # alpha 값은 0.5, 초기 Tau 값은 80만원

for i in range(12):
    start_date_true = datetime.datetime(2022, 2, 22)
    start_date_predicted = datetime.datetime(2022, 3, 1)
    trueDataDateList.append(start_date_true + datetime.timedelta(days=7*i))
    predictedDataDateList.append(start_date_predicted + datetime.timedelta(days=7*i))

# Define DataFrame
trueDataFrame = pd.DataFrame({'date' : np.array(trueDataDateList), 'price' : trueDataPriceList})
predictedDataFrame = pd.DataFrame({'date' : np.array(predictedDataDateList), 'price' : predictedDataPriceList})

# Plot time series
plt.plot(trueDataFrame.date, trueDataFrame.price, label='True Data', linewidth=3)
plt.plot(predictedDataFrame.date, predictedDataFrame.price, label='Predicted Data', linewidth=3)

# Add title and labels
ax = plt.gca()
plt.title('RTX 3060 Price')
ax.title.set_size(30)
plt.xlabel('Date')
ax.xaxis.label.set_size(16)
plt.ylabel('Price(1k won)')
ax.yaxis.label.set_size(16)

# Add legend
plt.legend(fontsize=14)

# Auto space
plt.tight_layout()

# Display plot
plt.show()