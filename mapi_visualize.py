import os.path
import numpy as np
import requests
import matplotlib.pyplot as plt

#ロボット掃除機の情報取得（名前など）
#/get/robot_id

#ステータスの取得（バッテリー残量など）
#/get/status

#イベントログの取得（全部）
#/get/event_log?last_id=0

#掃除開始
#/set/clean_start_or_continue?cleaning_parameter_set=1

#スポット掃除開始
#/set/clean_spot?map_id=0&x1=999&y1=999&cleaning_parameter_set=1

#掃除停止
#/set/stop

#充電ドックへ戻る
#/set/go_home

#時刻設定？（1分置き位で呼ばれてる）
#/set/time?year=2018&month&=1&day=8&hour=20&min=3

#MAP系
#/get/feature_map
#/get/n_n_polygons
#/get/cleaning_grid_map
#/get/rob_pose

# HTTPリクエスト xxx.xxx.xxx.xxxはmapiが接続しているPrivate IP address
url='http://xxx.xxx.xxx.xxx:10009/get/feature_map'
req = requests.get(url)
dict = req.json()
map = dict.get('map')
lines = map.get('lines')
n=len(lines)
print(lines)

#for文で部屋の地図情報を描画
for indx in range(0,n):
    x1=lines[indx].get('x1')
    y1=lines[indx].get('y1')
    x2=lines[indx].get('x2')
    y2=lines[indx].get('y2')
    plt.plot([x1, x2],[y1, y2])

# HTTPリクエスト
url='http://xxx.xxx.xxx.xxx:10009/get/rob_pose'
req = requests.get(url)
dict = req.json()
plt.plot([dict.get('x1'),dict.get('x2')],[dict.get('y1'),dict.get('y2')],marker="*") #イマココ

# HTTPリクエスト
url='http://xxx.xxx.xxx.xxx:10009/get/n_n_polygons'
req = requests.get(url)
dict = req.json()
map = dict.get('map')
polygons = map.get('polygons')

# for文
l=len(polygons)
for i in range(0,l):
    print(i)
    x=[]
    y=[]
    seg=polygons[i].get('segments')
    m=len(seg)
    for ii in range(0,m):
        print(ii)
        x1=seg[ii].get('x1')
        y1=seg[ii].get('y1')
        x2=seg[ii].get('x2')
        y2=seg[ii].get('y2')
        x=[x1,x2]
        print(x)
        y=[y1,y2]
        print(y)
        plt.plot(x,y)

url='http://xxx.xxx.xxx.xxx:10009/get/cleaning_grid_map'
req = requests.get(url)
dict = req.json()
xmin=dict.get('lower_left_x')
ymin=dict.get('lower_left_y')
xsize=dict.get('size_x')
ysize=dict.get('size_y')
res=dict.get('resolution')
plt.xticks(list(filter(lambda x: x%40==0, np.arange(xmin,xmin + xsize * res))))
plt.yticks(list(filter(lambda y: y%40==0, np.arange(ymin,ymin + ysize * res))))
plt.grid()
plt.savefig('result.png')
plt.show()

url='http://xxx.xxx.xxx.xxx:10009/set/clean_spot?map_id=0&x1=999&y1=999&cleaning_parameter_set=1'
req = requests.get(url)
