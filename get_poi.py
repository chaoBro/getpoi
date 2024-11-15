import requests
import openpyxl
import time

# 高德API密钥
api_key = 'db9741b828f4ac811937b1793ce4b950'

# 搜索参数
keywords = '海参'  # 搜索关键词
city = '青岛'      # 搜索城市
page_size = 20     # 每页条数，最大值为25
output_file = '商家信息.xlsx'

# 初始化Excel工作簿
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = '商家信息'
headers = ['名称', '地址', '电话', '类型', '坐标']
sheet.append(headers)

# 获取POI数据
page = 1
while True:
    url = f'https://restapi.amap.com/v3/place/text?key={api_key}&keywords={keywords}&city={city}&offset={page_size}&page={page}&extensions=all'
    response = requests.get(url)
    data = response.json()

    if data['status'] != '1':
        print('请求出错：', data.get('info', '未知错误'))
        break

    pois = data.get('pois', [])
    if not pois:
        break

    for poi in pois:
        name = poi.get('name', '')
        address = poi.get('address', '')
        tel = poi.get('tel', '')
        type_ = poi.get('type', '')
        location = poi.get('location', '')
        sheet.append([name, address, tel, type_, location])

    print(f'已获取第{page}页数据')
    page += 1
    time.sleep(0.5)  # 避免请求过于频繁

# 保存Excel文件
workbook.save(output_file)
print(f'商家信息已保存至 {output_file}')