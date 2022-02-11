# 讀取ubike線上即時資訊
# 建立一個自訂函數 讀取ubike資料,透過傳遞進來區域參數 找出相對資訊
import requests as re  # as 定義一個別名alias Name


def ubikeQry(search_area):
    # 1.Ubike即時資訊網路網址
    urlString = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    response = re.get(urlString)
    listData = response.json()  # json() 一般稱呼為function/物件.method

    listResult = []
    for pos in range(len(listData)):
        ubike = listData[pos]
        sna = ubike['sna']
        area = ubike['sarea']
        content = '順序:{index} 場站名稱:{sna} 區域:{area}'.format(
            index=pos, sna=sna, area=area)
        if area == search_area:  # 區域是否等於參數
            listResult.append(ubike)

    print(len(listResult))
    print(listResult)


def search_hint(currentWord):
    hint_list = ["信義區", "大同區", "中山區", "士林區", "中正區", "萬華區",
                 "大安區", "文山區", "內湖區", "松山區", "南港區", "淡水區", "天母區"]
    result = ",".join([h for h in hint_list if currentWord in h])
    return result
