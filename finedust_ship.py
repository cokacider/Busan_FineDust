import db_manage
import numpy as np
import math
import scipy.stats

from PIL import Image
from PIL import ImageDraw, ImageFont

# -------------------------------------------------------- setting

db_file_name = 'FineDust_project.db'

csv_file_list_dust = ['2016년 1분기.csv',
                    '2016년 2분기.csv',
                    '2016년 3분기.csv',
                    '2016년 4분기.csv',
                    '2014년 1분기.csv',
                      '2014년 2분기.csv',
                      '2014년 3분기.csv',
                      '2014년 4분기.csv',
                      '2015년1분기.csv',
                      '2015년2분기.csv',
                      '2015년3분기.csv',
                      '2015년4분기.csv']
station_list_dust = ['광복동',
                    '광안동',
                    '기장읍',
                    '녹산동',
                    '대신동',
                    '대연동',
                    '대저동',
                    '덕천동',
                    '명장동',
                    '부곡동',
                    '수정동',
                    '연산동',
                    '온천동',
                    '용수리',
                    '장림동',
                    '전포동',
                    '좌동',
                    '청룡동',
                    '초량동',
                     '태종대',
                     '학장동']

weatherASOS_file_name = ["SURFACE_ASOS_159_HR_2014_2014_2015.csv",
                         "SURFACE_ASOS_159_HR_2015_2015_2016.csv",
                         "SURFACE_ASOS_159_HR_2016_2016_2017.csv"]
weatherASOS_station = ["159"]

weatherAWS_file_name = ["SURFACE_AWS_938_MI_2016-01_2016-01_2017.csv",
                        "SURFACE_AWS_938_MI_2016-02_2016-02_2017.csv",
                        "SURFACE_AWS_938_MI_2016-03_2016-03_2017.csv",
                        "SURFACE_AWS_938_MI_2016-04_2016-04_2017.csv",
                        "SURFACE_AWS_938_MI_2016-05_2016-05_2017.csv",
                        "SURFACE_AWS_938_MI_2016-06_2016-06_2017.csv",
                        "SURFACE_AWS_938_MI_2016-07_2016-07_2017.csv",
                        "SURFACE_AWS_938_MI_2016-08_2016-08_2017.csv",
                        "SURFACE_AWS_938_MI_2016-09_2016-09_2017.csv",
                        "SURFACE_AWS_938_MI_2016-10_2016-10_2017.csv",
                        "SURFACE_AWS_938_MI_2016-11_2016-11_2017.csv",
                        "SURFACE_AWS_938_MI_2016-12_2016-12_2017.csv",
                        "SURFACE_AWS_968_MI_2016-01_2016-01_2017.csv",
                        "SURFACE_AWS_968_MI_2016-02_2016-02_2017.csv",
                        "SURFACE_AWS_968_MI_2016-03_2016-03_2017.csv",
                        "SURFACE_AWS_968_MI_2016-04_2016-04_2017.csv",
                        "SURFACE_AWS_968_MI_2016-05_2016-05_2017.csv",
                        "SURFACE_AWS_968_MI_2016-06_2016-06_2017.csv",
                        "SURFACE_AWS_968_MI_2016-07_2016-07_2017.csv",
                        "SURFACE_AWS_968_MI_2016-08_2016-08_2017.csv",
                        "SURFACE_AWS_968_MI_2016-09_2016-09_2017.csv",
                        "SURFACE_AWS_968_MI_2016-10_2016-10_2017.csv",
                        "SURFACE_AWS_968_MI_2016-11_2016-11_2017.csv",
                        "SURFACE_AWS_968_MI_2016-12_2016-12_2017.csv"]
weatherAWS_station = ["938",    # 부산진
                      "968"]    # 남항

port_name = '부산'
port_ship_file_name = ["항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2014.xlsx",
                       "항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2015.xlsx",
                       "항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2016.xlsx"]
port_container_file_name = ["항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2014.xlsx",
                            "항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2015.xlsx",
                            "항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2016.xlsx"]
port_name_sinhang = '신항'
port_ship_file_name_sinhang = ['항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2014_신항.xlsx',
                               '항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2015_신항.xlsx',
                               '항만정보통계_선박_부두별선박입출항통계(연월간)(확정)_2016_신항.xlsx']
port_container_file_name_sinhang = ['항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2014_신항.xlsx',
                                    '항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2015_신항.xlsx',
                                    '항만정보통계_컨테이너_부산항컨테이너물동량추이(확정)_2016_신항.xlsx']
port_years = [2014, 2015, 2016]

# Busan yellow dust date from 'http://www.kma.go.kr'
date_yellow_dust = ['20160409',
                    '20160410',
                    '20160414',
                    '20160423',
                    '20160424',
                    '20160507',
                    '20160508',
                    '20150223',
                    '20150224',
                    '20150302',
                    '20150322',
                    '20150417',
                    '20140101',
                    '20140102',
                    '20140120',
                    '20140318',
                    '20140526',
                    '20140527',
                    '20140528',
                    '20140529']

xy_image = [(220, 330), # 중구 광복동
            (295, 255), # 수영구 광안동
            (395, 150), # 기장군 기장읍
            (73, 340),  # 강서구 녹산동
            (205, 300), # 서구 대신동
            (268, 285), # 남구 대연동
            (150, 198), # 강서구 대저동
            (203, 205), # 북구 덕천동
            (274, 212), # 동래구 명장동
            (277, 184), # 금정구 부곡동
            (228, 292), # 동구 수정동
            (266, 234), # 연제구 연산동
            (0, 0),     # 동래구 온천동
            (347, 80),  # 기장군 용수리
            (183, 350), # 사하구 장림동
            (231, 258), # 부산진구 전포동
            (348, 261), # 해운대구 좌동
            (282, 134), # 금정구 청룡동
            (0, 0),     # 동구 초량동
            (254, 335), # 영도구 태종대
            (170, 262)] # 사상구 학장동

# 측정소 위도 경도
latitude_longitude = [(35.099888, 129.030383),  # 중구 광복동
                      (35.129286, 129.045464),  # 동구 수정동
                      (35.152960, 129.063871)  # 부산진구 전포동
                      ]

db = db_manage.DBManage(db_file_name)

# table drop 하고 다시 create
#db.fine_dust.reset_table()
#db.weatherASOS.reset_table()
#db.weatherAWS.reset_table()
#db.port_ship.reset_table()
#db.port_container.reset_table()

# csv 파일에서 데이터 불러와서 db에 저장하기
#db.insert_finedust_from_csv(csv_file_list_dust, station_list_dust)
#db.insert_weatherASOS_from_csv(weatherASOS_file_name, weatherASOS_station)
#db.insert_weatherAWS_from_csv(weatherAWS_file_name, weatherAWS_station)

#db.insert_portShip_from_xls(port_ship_file_name, port_years, port_name)
#db.port_container.insert_from_xls(port_container_file_name, port_years, port_name)
#db.insert_portShip_from_xls(port_ship_file_name_sinhang, port_years, port_name_sinhang)
#db.port_container.insert_from_xls(port_container_file_name_sinhang, port_years, port_name_sinhang)
# --------------------------------------------------------------------- setting end

def compare_specific_month():
    return_teajongdea = ""
    return_gwangbok = ""

    # print('---------------------------------------------------')
    # print('영도구 태종대 년도별 1~3월 월별 미세먼지 평균량')
    # print("(위치 , 년도 , 월 , 월별 미세먼지 평균량)")
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 3))
    #
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 3))
    #
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 3))

    return_teajongdea += '영도구 태종대 년도별 1~3월 월별 미세먼지 평균량\n' +\
                        "(위치 , 년도 , 월 , 월별 미세먼지 평균량)\n" +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 1)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 2)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2014, 3)) + '\n\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 1)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 2)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2015, 3)) + '\n\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 1)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 2)) + '\n' +\
                        str(db.fine_dust.get_pm10_aver_of_month('태종대', 2016, 3))


    # print('---------------------------------------------------')
    # print('중구 광복동 년도별 1~3월 월별 미세먼지 평균량')
    # print("(위치 , 년도 , 월 , 월별 미세먼지 평균량)")
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 3))
    #
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 3))
    #
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 1))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 2))
    # print(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 3))

    return_gwangbok += '중구 광복동 년도별 1~3월 월별 미세먼지 평균량\n' +\
                    "(위치 , 년도 , 월 , 월별 미세먼지 평균량)\n" +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 1)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 2)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2014, 3)) + '\n\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 1)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 2)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2015, 3)) + '\n\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 1)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 2)) + '\n' +\
                    str(db.fine_dust.get_pm10_aver_of_month('광복동', 2016, 3))

    return return_teajongdea, return_gwangbok

def pm10_according_to_traffic_sinhang():

    return_all_station_container = ""
    return_all_station_ship = ""

    return_noksan_container = ""
    return_noksan_ship = ""


    # 부산 전체 월별 평균 미세먼지량
    all_station_pm10_per_month = []
    for year in (2014, 2015, 2016):
        for month in range(1, 13):
            pm10_aver = db.fine_dust.get_pm10_aver_of_month_all_station(year, month)
            all_station_pm10_per_month.append(pm10_aver[0][2])


    # 월별 평균 미세먼지량
    noksan_month_data = pm10_average_each_month("녹산동", [2014, 2015, 2016], range(1, 13))  # 강서구 녹산동
    noksan_pm10_per_month = [data[3] for data in noksan_month_data]

    ship_num_month_data = db.port_ship.get_ship_data('신항')  # 월별 선박 입출항 수
    ship_num_per_month = [data[3] for data in ship_num_month_data]

    container_num_month_data = db.port_container.get_container_data('신항')  # 월별 컨테이너 물동량 TEU
    container_num_per_month = [data[3] for data in container_num_month_data]


    # print('-------------------------------------------------------------------')
    # print("*부산신항 컨테이너 물동량에 따른 미세먼지량(월별 평균값)")
    # print(' ')
    # print("x : 2014~2016년 신항 컨테이너 월별 물동량")
    # print("y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, all_station_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, all_station_pm10_per_month)[0])
    # print("x : 2014~2016년 신항 선박 월별 입출항량")
    # print("y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, all_station_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, all_station_pm10_per_month)[0])

    return_all_station_container = "x : 2014~2016년 신항 컨테이너 월별 물동량\n" +\
                                "y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값\n" +\
                                '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, all_station_pm10_per_month)[0][1]) + '\n' +\
                                '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, all_station_pm10_per_month)[0])
    return_all_station_ship = "x : 2014~2016년 신항 선박 월별 입출항량\n" +\
                            "y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값\n" +\
                            '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, all_station_pm10_per_month)[0][1]) + '\n' +\
                            '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, all_station_pm10_per_month)[0])

    # print('-------------------------------------------------------------------')
    # print("*신항 선박 입출항량, 컨테이너 물동량에 따른 미세먼지량(월별 평균값)")
    # print(' ')
    # print("x : 2014~2016년 신항 컨테이너 월별 물동량")
    # print("y : 2014~2016년 녹산동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, noksan_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, noksan_pm10_per_month)[0])
    # print("x : 2014~2016년 신항 선박 월별 입출항량")
    # print("y : 2014~2016년 녹산동 전체 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, noksan_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, noksan_pm10_per_month)[0])

    return_noksan_container = "x : 2014~2016년 신항 컨테이너 월별 물동량\n" +\
                            "y : 2014~2016년 녹산동 측정소 미세먼지 월별 평균값\n" +\
                            '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, noksan_pm10_per_month)[0][1]) + '\n' +\
                            '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, noksan_pm10_per_month)[0])
    return_noksan_ship = "x : 2014~2016년 신항 선박 월별 입출항량\n" +\
                        "y : 2014~2016년 녹산동 전체 측정소 미세먼지 월별 평균값\n"+\
                        '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, noksan_pm10_per_month)[0][1]) + '\n' +\
                        '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, noksan_pm10_per_month)[0])

    # the_year = 2014
    #
    # ship_num_per_month = [data[3] for data in ship_num_month_data
    #                       if data[1] == the_year]
    # container_num_per_month = [data[3] for data in container_num_month_data
    #                            if data[1] == the_year]
    # noksan_pm10_per_month = [data[3] for data in noksan_month_data
    #                            if data[1] == the_year]

    # print(' ')
    # print(str(the_year) + "년")
    # print("x :" + str(the_year) + "년 신항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 강서구 녹산동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, noksan_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, noksan_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 신항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 강서구 녹산동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, noksan_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, noksan_pm10_per_month)[0])

    # 2014년은 결과에 안 나옴

    return return_all_station_container, return_all_station_ship, return_noksan_container, return_noksan_ship


def pm10_according_to_traffic():

    return_all_station_ship = ""
    return_all_station_container = ""

    return_teajongdea_ship = ""
    return_teajongdea_container = ""
    return_gwangbok_ship = ""
    return_gwangbok_container = ""

    return_teajongdea_ship2014 = ""
    return_teajongdea_container2014 = ""
    return_gwangbok_ship2014 = ""
    return_gwangbok_container2014 = ""

    return_teajongdea_ship2015 = ""
    return_teajongdea_container2015 = ""
    return_gwangbok_ship2015 = ""
    return_gwangbok_container2015 = ""

    return_teajongdea_ship2016 = ""
    return_teajongdea_container2016 = ""
    return_gwangbok_ship2016 = ""
    return_gwangbok_container2016 = ""


    # 부산 전체 월별 평균 미세먼지량
    all_station_pm10_per_month = []
    for year in (2014,2015,2016):
        for month in range(1,13):
            pm10_aver = db.fine_dust.get_pm10_aver_of_month_all_station(year, month)
            all_station_pm10_per_month.append(pm10_aver[0][2])

    # 월별 평균 미세먼지량
    teajongdea_month_data = pm10_average_each_month("태종대", [2014, 2015, 2016], range(1, 13))   # 영도 태종대
    teajongdea_pm10_per_month = [data[3] for data in teajongdea_month_data]

    gwangbok_month_data = pm10_average_each_month("광복동", [2014, 2015, 2016], range(1, 13))    # 중구 광복동
    gwangbok_pm10_per_month = [data[3] for data in gwangbok_month_data]

    ship_num_month_data = db.port_ship.get_ship_data('부산')     # 월별 선박 입출항 수
    ship_num_per_month = [data[3] for data in ship_num_month_data]

    container_num_month_data = db.port_container.get_container_data('부산')  # 월별 컨테이너 물동량 TEU
    container_num_per_month = [data[3] for data in container_num_month_data]

    # print('-------------------------------------------------------------------')
    # print("*부산항 컨테이너 물동량에 따른 미세먼지량(월별 평균값)")
    # print(' ')
    # print("x : 2014~2016년 부산항 컨테이너 월별 물동량")
    # print("y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, all_station_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, all_station_pm10_per_month)[0])
    # print("x : 2014~2016년 부산항 선박 월별 입출항량")
    # print("y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, all_station_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, all_station_pm10_per_month)[0])

    return_all_station_ship += "x : 2014~2016년 부산항 선박 월별 입출항량" + '\n'
    return_all_station_ship += "y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값" + '\n'
    return_all_station_ship += '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, all_station_pm10_per_month)[0][1]) + '\n'
    return_all_station_ship += '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, all_station_pm10_per_month)[0])

    return_all_station_container += "x : 2014~2016년 부산항 컨테이너 월별 물동량" + '\n'
    return_all_station_container += "y : 2014~2016년 부산 전체 측정소 미세먼지 월별 평균값" + '\n'
    return_all_station_container += '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, all_station_pm10_per_month)[0][1]) + '\n'
    return_all_station_container += '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, all_station_pm10_per_month)[0])

    # print(' ')
    # print("2014~2016년")
    # print("x : 2014~2016년 부산항 컨테이너 월별 물동량")
    # print("y : 2014~2016년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x : 2014~2016년 부산항 컨테이너 월별 물동량")
    # print("y : 2014~2016년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])
    # print("x : 2014~2016년 부산항 선박 월별 입출항량")
    # print("y : 2014~2016년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x : 2014~2016년 부산항 선박 월별 입출항량")
    # print("y : 2014~2016년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])

    return_teajongdea_ship = "x : 2014~2016년 부산항 선박 월별 입출항량\n" +\
                            "y : 2014~2016년 영도구 태종대 측정소 미세먼지 월별 평균값\n" +\
                            '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' +\
                            '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    return_teajongdea_container = "x : 2014~2016년 부산항 컨테이너 월별 물동량\n" +\
                                "y : 2014~2016년 영도구 태종대 측정소 미세먼지 월별 평균값\n" +\
                                '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' +\
                                '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    return_gwangbok_ship = "x : 2014~2016년 부산항 선박 월별 입출항량\n" +\
                        "y : 2014~2016년 중구 광복동 측정소 미세먼지 월별 평균값\n" +\
                        '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' +\
                        '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])
    return_gwangbok_container = "x : 2014~2016년 부산항 컨테이너 월별 물동량\n" +\
                            "y : 2014~2016년 중구 광복동 측정소 미세먼지 월별 평균값\n" +\
                            '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' +\
                            '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])


    the_year = 2014

    ship_num_per_month = [data[3] for data in ship_num_month_data
                          if data[1] == the_year]
    teajongdea_pm10_per_month = [data[3] for data in teajongdea_month_data
                                 if data[1] == the_year]
    container_num_per_month = [data[3] for data in container_num_month_data
                               if data[1] == the_year]
    gwangbok_pm10_per_month = [data[3] for data in gwangbok_month_data
                               if data[1] == the_year]
    # print(' ')
    # print(str(the_year) + "년")
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])

    return_teajongdea_ship2014 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" +\
                                "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" +\
                                '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' +\
                                '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    return_teajongdea_container2014 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" +\
                                    "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" +\
                                    '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' +\
                                    '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    return_gwangbok_ship2014 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" +\
                            "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" +\
                            '피어슨 상관계수   : ' + str(np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' +\
                            '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])
    return_gwangbok_container2014 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" +\
                                "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" +\
                                '피어슨 상관계수   : ' + str(np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' +\
                                '스피어만 상관계수 : ' + str(scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])


    the_year = 2015

    ship_num_per_month = [data[3] for data in ship_num_month_data
                          if data[1] == the_year]
    teajongdea_pm10_per_month = [data[3] for data in teajongdea_month_data
                                 if data[1] == the_year]
    container_num_per_month = [data[3] for data in container_num_month_data
                               if data[1] == the_year]
    gwangbok_pm10_per_month = [data[3] for data in gwangbok_month_data
                               if data[1] == the_year]
    # print(' ')
    # print(str(the_year) + "년")
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])

    return_teajongdea_ship2015 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" + \
                                 "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" + \
                                 '피어슨 상관계수   : ' + str(
        np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' + \
                                 '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    return_teajongdea_container2015 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" + \
                                      "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" + \
                                      '피어슨 상관계수   : ' + str(
        np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' + \
                                      '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    return_gwangbok_ship2015 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" + \
                               "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" + \
                               '피어슨 상관계수   : ' + str(
        np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' + \
                               '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])
    return_gwangbok_container2015 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" + \
                                    "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" + \
                                    '피어슨 상관계수   : ' + str(
        np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' + \
                                    '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])

    the_year = 2016

    ship_num_per_month = [data[3] for data in ship_num_month_data
                          if data[1] == the_year]
    teajongdea_pm10_per_month = [data[3] for data in teajongdea_month_data
                                 if data[1] == the_year]
    container_num_per_month = [data[3] for data in container_num_month_data
                               if data[1] == the_year]
    gwangbok_pm10_per_month = [data[3] for data in gwangbok_month_data
                               if data[1] == the_year]
    # print(' ')
    # print(str(the_year) + "년")
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    # print("x :" + str(the_year) + "년 부산항 선박 월별 입출항량")
    # print("y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값")
    # print('피어슨 상관계수   :', np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1])
    # print('스피어만 상관계수 :', scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])
    #
    # print('-------------------------------------------------------------------')

    return_teajongdea_ship2016 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" + \
                                 "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" + \
                                 '피어슨 상관계수   : ' + str(
        np.corrcoef(ship_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' + \
                                 '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(ship_num_per_month, teajongdea_pm10_per_month)[0])
    return_teajongdea_container2016 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" + \
                                      "y :" + str(the_year) + "년 영도구 태종대 측정소 미세먼지 월별 평균값\n" + \
                                      '피어슨 상관계수   : ' + str(
        np.corrcoef(container_num_per_month, teajongdea_pm10_per_month)[0][1]) + '\n' + \
                                      '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(container_num_per_month, teajongdea_pm10_per_month)[0])
    return_gwangbok_ship2016 = "x :" + str(the_year) + "년 부산항 선박 월별 입출항량\n" + \
                               "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" + \
                               '피어슨 상관계수   : ' + str(
        np.corrcoef(ship_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' + \
                               '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(ship_num_per_month, gwangbok_pm10_per_month)[0])
    return_gwangbok_container2016 = "x :" + str(the_year) + "년 부산항 컨테이너 월별 물동량\n" + \
                                    "y :" + str(the_year) + "년 중구 광복동 측정소 미세먼지 월별 평균값\n" + \
                                    '피어슨 상관계수   : ' + str(
        np.corrcoef(container_num_per_month, gwangbok_pm10_per_month)[0][1]) + '\n' + \
                                    '스피어만 상관계수 : ' + str(
        scipy.stats.spearmanr(container_num_per_month, gwangbok_pm10_per_month)[0])

    return return_all_station_ship, return_all_station_container, return_teajongdea_ship, return_teajongdea_container,\
    return_gwangbok_ship, return_gwangbok_container, return_teajongdea_ship2014, return_teajongdea_container2014,\
    return_gwangbok_ship2014, return_gwangbok_container2014, return_teajongdea_ship2015, return_teajongdea_container2015,\
    return_gwangbok_ship2015, return_gwangbok_container2015, return_teajongdea_ship2016, return_teajongdea_container2016,\
    return_gwangbok_ship2016, return_gwangbok_container2016


def pm10_average_each_month(station, years, months):

    pm10_aver = []
    for year in years:
        for month in months:
            pm10_aver.append(db.fine_dust.get_pm10_aver_of_month(station, year, month)[0])

    return pm10_aver

def pm10_according_to_windASOS():
    busanjin_ASOS = ("159", '전포동')  # (종관(중구), 부산진구 전포동)

    myeongjang = ("159", '명장동')     # (종관(중구), 동래구 명장동)
    daeyeon = ("159", '대연동')        # (종관(중구), 남구 대연동)
    daesin = ('159', "대신동")         # 서구 대신동
    jangnim = ('159', '장림동')        # 사하구 장림동
    gwangan = ('159', '광안동')        # 수영구 광안동
    hakjang = ('159', '학장동')        # 사상구 학장동
    soojung = ('159', '수정동')        # 동구 수정동

    lat_lon_busanjin = (35.152960, 129.063871)  # 부산진구 전포동 위도, 경도

    lat_lon_myeongjang = (35.204889, 129.104318)    # 동래구 명장동 위도, 경도
    lat_lon_daeyeon = (35.130881, 129.087954)       # 남구 대연동 위도, 경도
    lat_lon_daesin = (35.114374, 129.017495)        # 서구 대신동 위도, 경도
    lat_lon_jangnim = (35.083063, 128.966875)       # 사하구 장림동
    lat_lon_gwangan = (35.152089, 129.108066)       # 수영구 광안동
    lat_lon_hakjang = (35.146596, 128.984111)       # 사상구 학장동
    lat_lon_soojung = (35.129320, 129.045383)       # 동구 구청


    lat_lon_busan_ASOS_station = (35.104814, 129.032273)    # 종관 기상 관측소 위도, 경도
    lat_lon_busan_port = (35.104307, 129.042197)    # 부산항 위도, 경도

    return_gwangan = cal_according_to_asos(gwangan, lat_lon_busan_port, lat_lon_gwangan)
    return_daesin = cal_according_to_asos(daesin, lat_lon_busan_port, lat_lon_daesin)
    return_hakjang = cal_according_to_asos(hakjang, lat_lon_busan_port, lat_lon_hakjang)
    return_soojung = cal_according_to_asos(soojung, lat_lon_busan_port, lat_lon_soojung)

    return_busanjin = cal_according_to_asos(busanjin_ASOS, lat_lon_busan_port, lat_lon_busanjin)
    return_busanjin2014 = cal_according_to_asos(busanjin_ASOS, lat_lon_busan_port, lat_lon_busanjin, 2014)
    return_busanjin2015 = cal_according_to_asos(busanjin_ASOS, lat_lon_busan_port, lat_lon_busanjin, 2015)
    return_busnajin2016 = cal_according_to_asos(busanjin_ASOS, lat_lon_busan_port, lat_lon_busanjin, 2016)

    return return_gwangan, return_daesin, return_hakjang, return_soojung, return_busanjin, return_busanjin2014, return_busanjin2015, return_busnajin2016


def cal_according_to_asos(station, lat_lon_port, lat_lon, year=0):
    direction_bt = bearingP1toP2(lat_lon_port, lat_lon)  # 두 지점 사이 방위각

    # 두 지점 사이의 방위각과 일직선 방향으로 바람이 불 때만 비교
    # 방위각을 기준으로 +- 15도 또는 방위각 + 180도 +- 15도 내의 풍향의 날짜에 해당하는 데이터
    related_wind_list = db.get_data_by_ASOSwind_direction(station, direction_bt)

    #print('가공 전 데이터 개수',related_wind_list.__len__())

    # 미세먼지 값이 None 인 거 없애기, 황사 발생일 없애기
    if year == 0:
        related_wind_list = [data for data in related_wind_list if data[3] != '' and not str(data[0])[:8] in date_yellow_dust]
    else:   # 특정 연도만
        related_wind_list = [data for data in related_wind_list if
                             data[3] != '' and
                             not str(data[0])[:8] in date_yellow_dust and
                             str(data[0])[:4] == str(year)]

    velocity_related_wind = [data[1] for data in related_wind_list]  # 풍속
    pm10_related_wind = [data[3] for data in related_wind_list]  # 미세먼지

    for i, data in enumerate(related_wind_list):
        if direction_bt < 15:
            if data[2] < direction_bt + 15 or data[2] > 360 + direction_bt - 15:
                # 반대방향은 음수로
                velocity_related_wind[i] *= -1
        elif direction_bt > 345:
            if data[2] > direction_bt - 15 or data[2] < direction_bt - 360 + 15:
                # 반대방향은 음수로
                velocity_related_wind[i] *= -1
        else:
            if direction_bt - 15 < data[2] < direction_bt + 15:
                # 반대방향은 음수로
                velocity_related_wind[i] *= -1

    pearson = np.corrcoef(velocity_related_wind, pm10_related_wind)[0][1]
    spearmanr = scipy.stats.spearmanr(velocity_related_wind, pm10_related_wind)[0]

    if year == 0:
        year_str = '2014, 2015, 2016'
    else:
        year_str = str(year)

    # print('-------------------------------------------------------------------------------------------------')
    # print('*부산항의 풍향이 ' + station[1] + ' 방향일 때와 그 반대 방향일 때 ' + station[1] + '의 미세먼지량과 풍속의 상관관계 계수')
    # print('부산항 위도 경도 :                    ', lat_lon_port)
    # print(station[1] + ' (미세먼지 측정소) 위도 경도 :  ', lat_lon)
    # print('부산항에서 ' + station[1] + ' 미세먼지 측정소로의 방위각 :', direction_bt, '도')
    # print('풍향이 ' + station[1] + ' 방향일 때 풍속은 양수, 그 반대 방향일 때는 풍속이 음수로 표현')
    # print(station[1] + ' 방향이나 부산항 방향(방위각 +- 15도 또는 방위각+180도 +- 15도)이 아닌 풍향에 대해서는 데이터 제외')
    # print("data 수 :", related_wind_list.__len__(), "개")
    # print('x = ' + year_str + '년 ' + station[1] + '의 방향이 있는(양,음수) 풍속')
    # print('y = ' + year_str + '년 부산진구 미세먼지량')
    # print('피어슨 상관계수   :', pearson)
    # print('스피어만 상관계수 :', spearmanr)
    # print('-------------------------------------------------------------------------------------------------')
    return_str = '-------------------------------------------------------------------------------------------------' +'\n' +\
                 '*부산항의 풍향이 ' + station[1] + ' 방향일 때와 그 반대 방향일 때' + '\n' + station[1] + '의 미세먼지량과 풍속의 상관관계 계수' +'\n' + \
                 '부산항 위도 경도 :                    ' + str(lat_lon_port) +'\n' +\
                 station[1] + ' (미세먼지 측정소) 위도 경도 :  ' + str(lat_lon) +'\n' + \
                 '부산항에서 ' + station[1] + ' 미세먼지 측정소로의 방위각 : ' + str(direction_bt) + ' 도' + '\n' + \
                 '풍향이 ' + station[1] + ' 방향일 때 풍속은 양수, 그 반대 방향일 때는 풍속이 음수로 표현' + '\n' + \
                 station[1] + ' 방향이나 부산항 방향(방위각 +- 15도 또는 방위각+180도 +- 15도)이' + '\n' + '아닌 풍향에 대해서는 데이터 제외' +'\n' + \
                 "data 수 : " + str(related_wind_list.__len__())+ " 개" +'\n'+ \
                 'x = ' + year_str + '년 ' + station[1] + '의 방향이 있는(양,음수) 풍속' +'\n' +\
                 'y = ' + year_str + '년 부산진구 미세먼지량' + '\n'+\
                 '피어슨 상관계수   : ' + str(pearson) + '\n' +\
                 '스피어만 상관계수 : ' + str(spearmanr) + '\n' +\
                 '-------------------------------------------------------------------------------------------------'
    return return_str

# 두 좌표 사이 방위각
# 출처 : 'http://www.androidpub.com/1159375'
def bearingP1toP2(p1, p2):
    p1_lat = p1[0]
    p1_lon = p1[1]
    p2_lat = p2[0]
    p2_lon = p2[1]

    cur_lat_radian = p1_lat * (math.pi / 180)
    cur_lon_radian = p1_lon * (math.pi / 180)

    dest_lat_radian = p2_lat * (math.pi / 180)
    dest_lon_radian = p2_lon * (math.pi / 180)

    radian_distance = 0
    radian_distance = math.acos(math.sin(cur_lat_radian) * math.sin(dest_lat_radian) +
                                math.cos(cur_lat_radian) * math.cos(dest_lat_radian) *
                                math.cos(cur_lon_radian - dest_lon_radian))

    radian_bearing = math.acos((math.sin(dest_lat_radian) - math.sin(cur_lat_radian) *
                                math.cos(radian_distance)) / (math.cos(cur_lat_radian) *
                                                              math.sin(radian_distance)))

    true_bearing = 0
    if math.sin(dest_lon_radian - cur_lon_radian) < 0:
        true_bearing = radian_bearing * (180 / math.pi)
        true_bearing = 360 - true_bearing

    else:
        true_bearing = radian_bearing * (180 / math.pi)

    return true_bearing


def get_map():

    return_station = ""
    return_value = ""

    pm10_in_stations = []

    date = [-1, -1, -1, -1]  # 원하는 시간 년, 월, 일, 시간, -1하면 해당 단위 모든 값 평균
    title = "2014~2016 year average fine dust each station"

    #print("지도에 출력할 수치")
    #print(title)
    #return_string += "\n\n" + title + "\n\n"

    # 단위 시간별 평균
    for i, station in enumerate(station_list_dust):

        pm10_of_station = \
            db.fine_dust.get_pm10_aver_of_station_at_time(
                station, date[0], date[1], date[2], date[3])[0][0]
        pm10_in_stations.append(pm10_of_station)
        #print(i + 1, db.fine_dust.get_area(station), station, pm10_of_station)
        return_station += str(db.fine_dust.get_area(station)) + ' ' + str(station) + '\n'
        return_value += str(pm10_of_station)[:8] + '\n'
    show_map(pm10_in_stations, title)
    return return_station, return_value

def show_map(pm10_in_stations, title):
    # 그림 -------------------------------------------------------
    img = Image.open("busandust.png")
    font = ImageFont.truetype("arial.ttf", 15)
    draw = ImageDraw.Draw(img)

    # title
    draw.text((10, 10), title, (0, 0, 0), font)

    for i, station in enumerate(station_list_dust):
        if station != "초량동" and station != "온천동":  # 도로변 대기 측정은 제외
            # 각 측정소에 수치 표시
            draw.text(xy_image[i], str(int(pm10_in_stations[i])), (255, 0, 0), font)

    #img.show()
    img.save('2014_2016_year_aver_dust.gif')
    # ---------------------------------------------------  그림 end