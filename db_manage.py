import db_finedust, db_weather_ASOS, db_weather_AWS, db_port_ship, db_port_container
import sqlite3


class DBManage:
    tables = ['dust', 'weatherASOS', 'weatherAWS', 'ship', 'container']

    def __init__(self, db_file):
        self.db_file = db_file

        # create a database connection
        self.conn = self._create_connection(db_file)

        self.fine_dust = db_finedust.DBFineDust(self.conn)
        self.weatherASOS = db_weather_ASOS.DBWeatherASOS(self.conn)
        self.weatherAWS = db_weather_AWS.DBWeatherAWS(self.conn)

        self.port_ship = db_port_ship.DBPortShip(self.conn)
        self.port_container = db_port_container.DBPortContainer(self.conn)

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def insert_finedust_from_csv(self, csv_files, stations):
        self.fine_dust.insert_from_csv(csv_files, stations)

    def insert_weatherAWS_from_csv(self, csv_files, stations):
        self.weatherAWS.insert_from_csv(csv_files, stations)

    def insert_weatherASOS_from_csv(self, csv_files, stations):
        self.weatherASOS.insert_from_csv(csv_files, stations)

    def insert_portShip_from_xls(self, xls_files, years, port):
        self.port_ship.insert_from_xls(xls_files, years, port)

    def insert_portContainer_from_xls(self, xls_files, years, port):
        self.port_container.insert_from_xls(xls_files, years, port)

    @staticmethod
    def angle_add(origin, num):
        value = origin + num
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        return value

    @staticmethod
    def _create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print("error : ", e)

        return None

    # 같은 월 컨테이너 물동량, 미세먼지량
    def get_data_by_ship_container(self, ):
        pass


    # 방향을 기준으로 옆으로 15도
    # 반대방향 기준 옆으로 15도 포함되는
    # 데이타 가져옴
    def get_data_by_ASOSwind_direction(self, stations, direction):
        station_weather = stations[0]
        station_dust = stations[1]

        cur = self.conn.cursor()

        sql = """ select asos.date, asos.velocity, asos.direction, dust.pm10
                    from weatherASOS asos, dust dust
                    where dust.station = ? and
                        asos.station = ? and
                        asos.direction > ? and
                        asos.direction < ? and
                        dust.date = asos.date
                        or
                        dust.station = ? and
                        asos.station = ? and
                        asos.direction > ? and
                        asos.direction < ? and
                        dust.date = asos.date
                        or
                        dust.station = ? and
                        asos.station = ? and
                        asos.direction > ? and
                        asos.direction < ? and
                        dust.date = asos.date
                        or
                        dust.station = ? and
                        asos.station = ? and
                        asos.direction > ? and
                        asos.direction < ? and
                        dust.date = asos.date; """

        effective_area = 15
        dir_low = self.angle_add(direction, -effective_area)
        dir_hig = self.angle_add(direction, effective_area)
        opp_low = self.angle_add(direction, 180 - effective_area)
        opp_hig = self.angle_add(direction, 180 + effective_area)

        par1 = dir_low
        par2 = dir_hig
        par3 = dir_low
        par4 = dir_hig
        par5 = opp_low
        par6 = opp_hig
        par7 = opp_low
        par8 = opp_hig
        if dir_low > 330:
            par2 = 360
            par3 = 0

        elif opp_low > 330:
            par6 = 360
            par7 = 0

        cur.execute(sql, (station_dust, station_weather, par1, par2,
                          station_dust, station_weather, par3, par4,
                          station_dust, station_weather, par5, par6,
                          station_dust, station_weather, par7, par8))
        try:
            return cur.fetchall()
        except Exception:
            return None

    """
    # 방향을 기준으로 옆으로 15도
    # 반대방향 기준 옆으로 15도 포함되는
    # 데이타 가져옴
    # 강수량 없는 날만 가져옴
    def get_data_by_AWSwind_direction(self, stations, direction):
        station_weather = stations[0]
        station_dust = stations[1]

        cur = self.conn.cursor()
        
        sql = """ """ select aws.date, aws.velocity, aws.direction, dust.pm10
                    from weatherAWS aws, dust dust
                    where dust.station = ? and
                        aws.station = ? and
                        not aws.precipitation > 0 and
                        aws.direction > ? and
                        aws.direction < ? and
                        dust.date = aws.date
                        or
                        dust.station = ? and
                        aws.station = ? and
                        not aws.precipitation > 0 and
                        aws.direction > ? and
                        aws.direction < ? and
                        dust.date = aws.date
                        or
                        dust.station = ? and
                        aws.station = ? and
                        not aws.precipitation > 0 and
                        aws.direction > ? and
                        aws.direction < ? and
                        dust.date = aws.date
                        or
                        dust.station = ? and
                        aws.station = ? and
                        not aws.precipitation > 0 and
                        aws.direction > ? and
                        aws.direction < ? and
                        dust.date = aws.date ; """ """

        dir_low = self.angle_add(direction, -15)
        dir_hig = self.angle_add(direction, 15)
        opp_low = self.angle_add(direction, 180 - 15)
        opp_hig = self.angle_add(direction, 180 + 15)

        par1 = dir_low
        par2 = dir_hig
        par3 = dir_low
        par4 = dir_hig
        par5 = opp_low
        par6 = opp_hig
        par7 = opp_low
        par8 = opp_hig
        if dir_low > 330:
            par2 = 360
            par3 = 0

        elif opp_low > 330:
            par6 = 360
            par7 = 0

        cur.execute(sql, (station_dust, station_weather, par1, par2,
                          station_dust, station_weather, par3, par4,
                          station_dust, station_weather, par5, par6,
                          station_dust, station_weather, par7, par8))
        try:
            return cur.fetchall()
        except Exception:
            return None
    """