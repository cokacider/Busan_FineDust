import sqlite3
import csv
import numpy


class DBWeatherAWS:
    table = 'weatherAWS'
    _sql_create_weatherAWS_table = """ CREATE TABLE IF NOT EXISTS weatherAWS (
                        station text,
                        date integer,
                        direction real,
                        velocity real,
                        precipitation real,
                        year integer,
                        month integer,
                        day integer,
                        hour integer,
                        primary key(station, date)                    
                        ); """

    def __init__(self, conn):
        self.conn = conn

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_weatherAWS_table)
        else:
            print("E : cannot create the DB connection")

    # drop and create
    def reset_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE weatherAWS''')
        self.conn.commit()

        self._create_table(self.conn, self._sql_create_weatherAWS_table)

    def insert_from_csv(self, csv_files, stations):
        for file_name in csv_files:
            file = open(file_name, 'r')
            reader = csv.reader(file)

            raw_date = ""
            direction = []
            velocity = []
            precipitation = []

            for line in reader:

                if line[0] in stations:

                    if line[1][:13] != raw_date:
                        raw_date = line[1][:13]
                        direction = []
                        velocity = []
                        precipitation = []

                    try:
                        direction.append(float(line[2]))
                    except Exception:
                        pass

                    try:
                        velocity.append(float(line[3]))
                    except Exception:
                        pass

                    try:
                        precipitation.append(float(line[5]))
                    except Exception:
                        pass


                    if line[1][14:16] == '59':
                        values = []
                        values.append(line[0]) # station

                        year = line[1][:4]
                        month = line[1][5:7]
                        day = line[1][8:10]
                        hour = line[1][11:13]

                        date = year + month + day + hour
                        values.append(date) # date

                        di_aver = None
                        vel_aver = None
                        pre_aver = None

                        if direction.__len__() != 0:
                            di_aver = numpy.average(direction)
                        values.append(di_aver)  # direction

                        if velocity.__len__() != 0:
                            vel_aver = numpy.average(velocity)
                        values.append(vel_aver) # velocity

                        if precipitation.__len__() != 0:
                            pre_aver = numpy.average(precipitation)
                        values.append(pre_aver)  # precipitation

                        values.append(year)
                        values.append(month)
                        values.append(day)
                        values.append(hour)

                        self._insert_table(self.conn, self._sql_insert_weatherAWS_table, values)
            self.conn.commit()
            file.close()
            print("db weather AWS file", file_name, "insert finish")

    def get_all(self):
        cur = self.conn.cursor()
        sql = """ select * from weatherAWS; """
        cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_stations(self):
        cur = self.conn.cursor()
        sql = """ select distinct station from weatherAWS"""
        cur.execute(sql)
        return cur.fetchall()

    # 방향을 기준으로 옆으로 15도
    # 반대방향 기준 옆으로 15도 포함되는
    # 데이타 가져옴
    # 강수량 없는 날만 가져옴
    def get_data_by_wind_direction(self, station,  direction):
        cur = self.conn.cursor()
        sql = """ select date, velocity, direction
                    from weatherAWS
                    where station = ? and
                        not precipitation > 0 and
                        direction > ? and
                        direction < ? 
                        or
                        station = ? and
                        not precipitation > 0 and
                        direction > ? and
                        direction < ? 
                        or
                        station = ? and
                        not precipitation > 0 and
                        direction > ? and
                        direction < ? 
                        or
                        station = ? and
                        not precipitation > 0 and
                        direction > ? and
                        direction < ?; """

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

        cur.execute(sql, (station, par1, par2, station, par3, par4, station, par5, par6, station, par7, par8))
        try:
            return cur.fetchall()
        except Exception:
            return None

    @staticmethod
    def angle_add(origin, num):
        value = origin + num
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        return value

    _sql_insert_weatherAWS_table = """insert into weatherAWS(
                                    station,
                                    date,
                                    direction,
                                    velocity,
                                    precipitation,
                                    year,
                                    month,
                                    day,
                                    hour
                                    ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    @staticmethod
    def _create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Exception as e:
            print("error : ", e)

        return None

    @staticmethod
    def _create_table(conn, create_table_sql):
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
        except Exception as e:
            print("create table error : ", e)

    @staticmethod
    def _insert_table(conn, insert_table_sql, values):
        try:
            cursor = conn.cursor()
            cursor.execute(insert_table_sql, values)
        except Exception as e:
            print("insert error : ", e, values)