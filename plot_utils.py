import pandas as pd
from pylab import mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体


def pie_chart(data):
    # 不同行政区房源数量占比
    area_house_count = data.groupby('行政区')['行政区'].count().sort_values(ascending=False)

    # 有无电梯房源数量占比
    elevator_count = data.groupby('电梯')['电梯'].count().sort_values(ascending=False)

    # 不同户型房源数量占比()
    house_type_count = data.groupby('房屋户型')['房屋户型'].count().sort_values(ascending=False)
    new_house_type_count = house_type_count[house_type_count > 1000]
    new_house_type_count['其它'] = house_type_count[house_type_count < 1000].sum()

    # 不同朝向房源数量占比()
    direction_count = data.groupby('朝向')['朝向'].count().sort_values(ascending=False)
    new_direction_count = direction_count[direction_count > 800]
    new_direction_count['其它'] = direction_count[direction_count < 800].sum()

    # 不同装修房源数量占比
    decoration_count = data.groupby('装修情况')['装修情况'].count().sort_values(ascending=False)

    # 不同楼层房源数量占比
    floor_count = data.groupby('楼层')['楼层'].count().sort_values(ascending=False)

    fig = plt.figure(figsize=(10, 8), dpi=160)
    ax1 = fig.add_subplot(3, 2, 1)
    plt.title("不同行政区房源数量占比情况")
    area_house_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=90, ax=ax1)

    ax2 = fig.add_subplot(3, 2, 2)
    plt.title("不同房屋户型房源数量占比情况")
    new_house_type_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=45, ax=ax2)

    ax3 = fig.add_subplot(3, 2, 3)
    plt.title("有无电梯房源数量占比情况")
    elevator_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=90, ax=ax3)

    ax4 = fig.add_subplot(3, 2, 4)
    plt.title("不同朝向房源数量占比情况")
    new_direction_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=90, ax=ax4)

    ax5 = fig.add_subplot(3, 2, 5)
    plt.title("不同装修类型的占比情况")
    decoration_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=45, ax=ax5)

    ax6 = fig.add_subplot(3, 2, 6)
    plt.title("不同楼层房源数量占比情况")
    floor_count.plot.pie(shadow=True, autopct='%0.f%%', startangle=45, ax=ax6)

    plt.savefig('不同行政区、户型、朝向、装修、楼层、电梯情况占比饼状图.jpg')
    plt.show()


def price_contrast(data):
    # 不同区的总价对比
    area_house_mean_totalprice = data.groupby('行政区')['价格(万元)'].median()
    area_house_mean_totalprice.sort_values(ascending=False, inplace=True)

    # 不同区的单价对比
    area_house_mean_unitprice = data.groupby('行政区')['单价(元/m²)'].median()
    area_house_mean_unitprice.sort_values(ascending=False, inplace=True)

    fig = plt.figure(figsize=(10, 6), dpi=160)
    ax1 = fig.add_subplot(1, 2, 1)
    plt.title("昆明不同行政区价格对比")
    plt.ylim([30, 200])  # 设置y坐标轴的范围
    area_house_mean_totalprice.plot.bar(alpha=0.7, color='#1E90FF', ax=ax1)
    plt.ylabel('价格')
    plt.grid(alpha=0.5, color='#CD3700', linestyle='--', axis='y')

    ax2 = fig.add_subplot(1, 2, 2)
    plt.title("昆明不同行政区单价对比")
    plt.ylim([5000, 20000])
    area_house_mean_unitprice.plot.bar(alpha=0.7, color='#4876FF', ax=ax2)
    plt.ylabel('单价(元/m$^{2}$)')
    plt.grid(alpha=0.5, color='#CD3700', linestyle='--', axis='y')
    plt.savefig('昆明不同行政区总价、单价对比图.jpg')
    plt.show()


def district_10(data):
    fig = plt.figure(figsize=(7, 6), dpi=160)
    district_top10 = data.groupby('地段')['价格(万元)'].median().sort_values(ascending=False).head(10)

    # 绘图  只展示排名前十的地段
    plt.title("昆明房价排名前十的地段")
    district_top10.plot.barh(alpha=0.7,
                             color=['#CD3700', '#9ACD32', '#7EC0EE', 'y', 'orange', '#4876FF', '#EEA9B8', '#EE7942',
                                    '#CD69C9', '#668B8B'])
    plt.grid(color='#DDA0DD', linestyle='--', alpha=0.5)
    plt.xlabel('价格')
    plt.savefig('昆明房价排名前十地段图.jpg')
    plt.show()


def community_10(data):
    fig = plt.figure(figsize=(10, 5), dpi=160)

    community_top10 = data.groupby('小区')['价格(万元)'].median().sort_values(ascending=False).head(10)
    plt.title("昆明房价排名前十的小区")
    community_top10.plot.barh(alpha=0.7, width=0.7)
    plt.xlabel('价格')
    plt.savefig('昆明小区均价总价排名前10图.jpg')
    plt.show()


def layout(data):
    # 房屋户型对房屋单价的影响
    fig = plt.figure(figsize=(15, 15), dpi=160)
    data_temp = data.copy()
    house_type_count = data['房屋户型'].value_counts()
    house_type = house_type_count[house_type_count.values < 1000]
    for key in house_type.keys():
        data_temp.drop(data_temp[data_temp['房屋户型'] == key].index, inplace=True)

    house_type_price = data_temp.groupby('房屋户型')['单价(元/m²)'].median().sort_values(ascending=False)

    plt.title("房屋户型对价格的影响", size=15)
    house_type_price.plot.bar()
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.ylabel('单价(元/m$^{2}$)', size=15)
    plt.grid(color='#DDA0DD', linestyle='--', alpha=0.5, axis='y')
    plt.savefig('房屋户型对价格影响图.jpg')
    plt.show()


def decoration(data, community_data):
    # 装修情况对单价的影响
    fig = plt.figure(figsize=(15, 15), dpi=160)
    ax1 = fig.add_subplot(2, 1, 1)
    decoration_price = data.groupby('装修情况')['单价(元/m²)'].median().sort_values(ascending=False)
    plt.title('装修情况对价格的影响')
    decoration_price.plot.bar(ax=ax1)
    plt.ylabel('单价(元/m$^{2}$)')

    # 在相同小区进行对比，这里分别选取房源数量前十的小区
    ax2 = fig.add_subplot(2, 1, 2)
    community_data.plot.bar(color=['#00a8e1', '#99cc00', '#e30039', '#fcd300'], ax=ax2)
    plt.title('房源数量前十小区装修情况对价格的影响')
    plt.ylabel('单价(元/m$^{2}$)')
    plt.savefig('装修情况对价格影响图.jpg')
    plt.show()


def elevator(data):
    # 房屋有无电梯对房屋单价的影响
    fig = plt.figure(figsize=(15, 7), dpi=160)

    ax1 = fig.add_subplot(1, 2, 1)
    elevator_price = data.groupby('电梯')['单价(元/m²)'].median().sort_values(ascending=False)
    elevator_price.plot.bar(ax=ax1)
    plt.title('有无电梯对价格的影响')
    plt.ylabel('单价(元/m$^{2}$)')

    # 在相同地段进行对比，这里分别选取房源数量前十的地段
    ax2 = fig.add_subplot(1, 2, 2)
    district = data['地段'].value_counts()
    district_list = district.keys()[1:11].tolist()  # 呈贡区的地段基本为呈贡，不取呈贡区地段
    plot_list = []
    for name in district_list:
        plot_list.append(
            data[data['地段'] == name].groupby('电梯')['单价(元/m²)'].median().sort_values(ascending=False))
    df = pd.DataFrame(plot_list)
    df.index = district_list
    df.plot.bar(color=['#00a8e1', '#e30039'], ax=ax2)
    plt.title('房源数量前十地段有无电梯对价格的影响')
    plt.ylabel('单价(元/m$^{2}$)')
    plt.savefig('有无电梯对价格影响图.jpg')
    plt.show()


def direction(data, community_data):
    # 房屋朝向对房屋单价的影响
    direction_price = data.groupby('朝向')['单价(元/m²)'].median().sort_values(ascending=False)
    fig = plt.figure(figsize=(15, 15), dpi=160)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.title("房屋朝向对价格的影响")
    direction_price.plot.bar(ax=ax1)
    plt.ylabel('单价(元/m$^{2}$)')
    plt.grid(color='#DDA0DD', linestyle='--', alpha=0.5, axis='y')

    # 在相同小区进行对比，这里分别选取房源数量前十的小区
    ax2 = fig.add_subplot(2, 1, 2)
    community_data.plot.bar(
        color=['#00a8e1', '#99cc00', '#e30039', '#fcd300', '#800080', '#00994e', '#ff6600', '#808000'], ax=ax2)
    plt.title('房源数量前十小区朝向对价格的影响')
    plt.ylabel('单价(元/m$^{2}$)')
    plt.savefig('房屋朝向对价格影响图.jpg')
    plt.show()


def floor(data, community_data):
    # 房屋楼层对房屋单价的影响
    floor_price = data.groupby('楼层')['单价(元/m²)'].median().sort_values(ascending=False)
    fig = plt.figure(figsize=(15, 15), dpi=160)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.title("不同楼层对价格的影响")
    floor_price.plot.bar(ax=ax1)
    plt.ylabel('单价(元/m$^{2}$)')
    plt.grid(color='#DDA0DD', linestyle='--', alpha=0.5, axis='y')

    # 在相同小区进行对比，这里分别选取房源数量前十的小区
    ax2 = fig.add_subplot(2, 1, 2)
    community_data.plot.bar(
        color=['#00a8e1', '#99cc00', '#e30039', '#fcd300', '#800080', '#00994e', '#ff6600', '#808000'], ax=ax2)
    plt.title('房源数量前十小区不同楼层对价格的影响')
    plt.ylabel('单价(元/m$^{2}$)')
    plt.savefig('不同楼层对价格影响图.jpg')
    plt.show()


def price_num(data):
    fig = plt.figure(figsize=(9, 6), dpi=160)
    bins_arr = np.arange(0, 1000, 30)
    bins = pd.cut(data['价格(万元)'], bins_arr)
    total_price_counts = data['价格(万元)'].groupby(bins).count()
    plt.title("昆明不同总价区间内的房源数量分析")
    plt.ylabel("社区房数量")
    total_price_counts.plot.barh(alpha=0.7, width=0.7)
    plt.xlabel('数量')
    plt.ylabel('万元')
    plt.savefig('昆明不同总价区间房源数量图.jpg')
    plt.show()


def data_scatter(data1, data2):
    fig = plt.figure(figsize=(15, 5), dpi=160)
    ax1 = fig.add_subplot(1, 2, 1)
    plt.title("房屋面积与价格分布散点图")
    plt.scatter(data1['面积(m²)'], data1['价格(万元)'], s=4)
    plt.xlabel('面积(m$^{2}$)')
    plt.ylabel('价格')

    ax2 = fig.add_subplot(1, 2, 2)
    plt.title("房屋面积与价格分布散点图")
    plt.scatter(data2['面积(m²)'], data2['价格(万元)'], s=4)
    plt.xlabel('面积(m$^{2}$)')
    plt.ylabel('价格')

    plt.savefig('房屋面积与价格分布散点图.jpg')
    plt.show()
