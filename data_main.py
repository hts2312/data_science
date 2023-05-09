import pandas as pd
from plot_utils import *

usecols = ['小区', '价格(万元)', '行政区', '地段', '房屋户型', '楼层', '面积(m²)', '朝向', '装修情况',
           '电梯']
df = pd.read_csv('昆明二手房数据.csv', encoding='utf-8', usecols=usecols, na_values=['暂无数据'])

# 删除重复行
df.drop_duplicates(inplace=True)

# 去除行政区房源数量不足200的行政区
area_house_count = df['行政区'].value_counts()
area_house_count = area_house_count[area_house_count < 200]
for key in area_house_count.keys():
    df.drop(df[df['行政区'] == key].index, inplace=True)

# 获取房屋总楼层数
floor_total = df['楼层'].str.extract('(\d+)')
floor_total = floor_total.astype('int')
df['总楼层'] = floor_total

# 格式化房屋楼层
floor_data = df['楼层'].str.extract('(\w\w\w)')
df['楼层'] = floor_data

# 通过总楼层数对电梯缺失值进行填充
for index, row in df[df['电梯'].isnull()].iterrows():
    if row['总楼层'] > 6:
        df.loc[index, '电梯'] = '有'
    else:
        df.loc[index, '电梯'] = '无'

print(df.isnull().sum())

# 去除地段为空值的数据
df.dropna(how='any', inplace=True)

# 格式化面积为数值型
df['面积(m²)'] = df['面积(m²)'].str.replace('㎡', '')
df['面积(m²)'] = df['面积(m²)'].astype('float')

# 增加房屋单价一列
df['单价(元/m²)'] = df['价格(万元)'] * 10000 / df['面积(m²)']

# 处理朝向数据
temp = df['朝向'].str.split(' ')
for key_values in df['朝向'].str.split(' ').items():
    df.loc[key_values[0], '朝向'] = key_values[1][0]

# 去除了小区房源数不足20小区的数据,另存为data_drop_community
df_drop_community = df.copy()
community_house_count = df['小区'].value_counts()
drop_community = community_house_count[community_house_count < 20]
for key in drop_community.keys():
    df_drop_community.drop(df_drop_community[df_drop_community['小区'] == key].index, inplace=True)

# 去除了地段房源数不足20地段的数据,另存为data_drop_district
df_drop_district = df.copy()
district_house_count = df['小区'].value_counts()
drop_district = district_house_count[district_house_count < 20]
for key in drop_district.keys():
    df_drop_district.drop(df_drop_district[df_drop_district['小区'] == key].index, inplace=True)

# 房源数量排名前十的小区
community_list = community_house_count.keys()[:10].tolist()
plot_list = []
for name in community_list:
    plot_list.append(
        df[df['小区'] == name].groupby('朝向')['单价(元/m²)'].median().sort_values(ascending=False))
community_direction_top10 = pd.DataFrame(plot_list)
community_direction_top10.index = community_list

plot_list = []
for name in community_list:
    plot_list.append(
        df[df['小区'] == name].groupby('装修情况')['单价(元/m²)'].median().sort_values(ascending=False))
community_decoration_top10 = pd.DataFrame(plot_list)
community_decoration_top10.index = community_list

plot_list = []
for name in community_list:
    plot_list.append(
        df[df['小区'] == name].groupby('楼层')['单价(元/m²)'].median().sort_values(ascending=False))
community_floor_top10 = pd.DataFrame(plot_list)
community_floor_top10.index = community_list

df_temp = df.copy()
# 数据散点图分布
# data_scatter(df)

# 处理异常值
df.drop(df[df['价格(万元)'] > 1500].index, inplace=True)

data_scatter(df_temp, df)

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.set_option('display.unicode.east_asian_width', True)
# print(df.head())
# print(df.count())

# 绘制图像
pie_chart(df)
price_contrast(df)
district_10(df_drop_district)
community_10(df_drop_community)
layout(df)
elevator(df)
direction(df, community_direction_top10)
decoration(df, community_decoration_top10)
floor(df, community_floor_top10)
price_num(df)
