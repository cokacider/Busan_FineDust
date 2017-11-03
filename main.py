import db_finedust


def main():
    db_file_name = 'fine_dust.db'
    csv_file_list = ['2016년 1분기.csv',
                     '2016년 2분기.csv',
                     '2016년 3분기.csv',
                     '2016년 4분기.csv']
    station_list = ['광복동',
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

    # db_finedust.DBFineDust(DB 파일 이름) : 객체 만들기
    fine_dust = db_finedust.DBFineDust(db_file_name)

    # fine_dust.insert_from_csv(csv 파일[에어코리아 미세먼지 csv] list, 원하는 측정소 이름 list)
    # 입력한 csv 파일들에서 원하는 측정소의 데이터를 읽어서 DB 파일에 넣는다.
    # 중요!!! -> DB 파일에 이미 insert 했으면 또 할 필요 없음!!!! 주석 처리해!!!!!
    # error :  UNIQUE constraint failed: dust.station_name, dust.date 라고 막 뜨는건 이미 넣은 거 또 넣으려고 해서 뜨는건데 값에 영향을 주지는 않음
    fine_dust.insert_from_csv(csv_file_list, station_list)

    # 객체.get_row_num() : DB 행 개수 리턴
    print(fine_dust.get_row_num())

    # 객체.get_all() : DB에 저장된 모든 데이터 리턴, 너무 길어서 쓸 일은 없을 듯
    print(fine_dust.get_all())

    # 객체.get_all_option(측정소 이름, 시각 - yyyymmddhh string도 되고 int도 됨)
    # 원하는 측정소의 원하는 시각의 위치, 측정소코드, 측정소이름, SO2, CO, O3, NO2, PM10(미세먼지), PM2.5(초미세먼지), 주소를 리턴
    print(fine_dust.get_all_option('부곡동', '2016012213')) # 또는
    print(fine_dust.get_all_option('부곡동', 2016012213))

    # 객체.get_area(측정소 이름) : 지역 리턴
    print(fine_dust.get_area('부곡동'))

    # 객체.get_station_code(측정소 이름) : 측정소 코드 리턴
    print(fine_dust.get_station_code('부곡동'))

    # 객체.get_station_name(측정소 코드) : 측정소 이름 리턴
    print(fine_dust.get_station_name('221251'))

    # 객체.get_so2(측정소이름, 시각) : SO2 리턴
    print(fine_dust.get_so2('부곡동', '2016012213'))

    # 객체.get_co(측정소이름, 시각) : CO 리턴
    print(fine_dust.get_co('부곡동', '2016012213'))

    # 객체.get_o3(측정소이름, 시각) : O3 리턴
    print(fine_dust.get_o3('부곡동', '2016012213'))

    # 객체.get_no2(측정소이름, 시각) : NO2 리턴
    print(fine_dust.get_no2('부곡동', '2016012213'))

    # 객체.get_pm10(측정소이름, 시각) : 미세먼지 pm10 리턴
    print(fine_dust.get_pm10('부곡동', '2016012213'))

    # 객체.get_pm25(측정소이름, 시각) : 초미세먼지 pm2.5 리턴
    print(fine_dust.get_pm25('부곡동', '2016012213'))

    # 객체.get_address(측정소이름) : 주소 리턴
    print(fine_dust.get_address('부곡동'))

    # 시각 파라미터는 integer string 상관 없음
    # 없는 데이터는 None 리턴

if __name__ == '__main__':
    main()
