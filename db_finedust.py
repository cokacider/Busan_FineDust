import sqlite3
import csv


class DBFineDust:
    table = 'dust'
    _sql_create_dust_table = """ CREATE TABLE IF NOT EXISTS dust (
                    area text NOT NULL,
                    station_code integer NOT NULL,
                    station text NOT NULL,
                    date integer NOT NULL,
                    so2 real,
                    co real,
                    o3 real,
                    no2 real,
                    pm10 integer,
                    pm25 integer,
                    address text,
                    year integer NOT NULL,
                    month integer NOT NULL,
                    day integer NOT NULL,
                    hour integer NOT NULL,
                    primary key(station, date)                    
                    ); """

    def __init__(self, conn):

        self.conn = conn

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_dust_table)
        else:
            print("E : cannot create the DB connection")

    # drop and create
    def reset_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE dust''')
        self.conn.commit()

        self._create_table(self.conn, self._sql_create_dust_table)


    def insert_from_csv(self, csv_files, stations):
        # insert data to DB
        if isinstance(csv_files, list):
            for file_name in csv_files:
                self._insert_csv(file_name, stations)
        else:
            self._insert_csv(csv_files, stations)

    def _insert_csv(self, file_name, stations):
        file = open(file_name, 'r')
        reader = csv.reader(file)
        for line in reader:
            if line[2] in stations:
                the_line = line
                line[3] = self._hour24to0(line[3])
                the_line.append(line[3][0:4])   # year
                the_line.append(line[3][4:6])   # month
                the_line.append(line[3][6:8])   # day
                the_line.append(line[3][8:10])  # hour
                self._insert_table(self.conn, self._sql_insert_dust_table, the_line)
        self.conn.commit()
        file.close()
        print("db fine dust file", file_name, "insert finish")

    @staticmethod
    def _hour24to0(date):
        if date[8:10] == '24':
            hour = '00'  # hour
            day = date[6:8]
            month = date[4:6]
            year = date[0:4]

            month31 = ['01','03','05','07','08','10','12']
            month30 = ['04','06','09','11']
            leapYear = ['2016', '2012']

            if date[4:6] in month31 and date[6:8] == '31':
                month = ('0' + str(int(date[4:6]) + 1))[-2:] # month
                day = '01'    # day

            elif date[4:6] in month30 and date[6:8] == '30':
                month = ('0' + str(int(date[4:6]) + 1))[-2:] # month
                day = '01'  # day

            elif date[4:6] == '02' and date[0:4] in leapYear and date[6:8] == '29':
                month = ('0' + str(int(date[4:6]) + 1))[-2:]  # month
                day = '01'  # day

            elif date[4:6] == '02' and date[0:4] not in leapYear and date[6:8] == '28':
                month = ('0' + str(int(date[4:6]) + 1))[-2:]  # month
                day = '01'  # day

            else:
                day = ('0' + str(int(date[6:8]) + 1))[-2:]

            if int(date[4:6]) == 13:
                month = '01'
                year = str(int(date[0:4]) + 1)
        else:
            return date
        modified = year + month + day + hour
        return modified


    _sql_insert_dust_table = """insert into dust(
                                 area,
                                 station_code,
                                 station,
                                 date,
                                 so2,
                                 co,
                                 o3,
                                 no2,
                                 pm10,
                                 pm25,
                                 address,
                                 year,
                                 month,
                                 day,
                                 hour
                                 ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""


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

    def get_row_num(self):
        cur = self.conn.cursor()
        sql = 'select count(*) from dust'
        cur.execute(sql)
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_row_num_station(self, station):
        cur = self.conn.cursor()
        sql = 'select count(*) from dust where station = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_all(self):
        # get all data
        cur = self.conn.cursor()
        sql = 'select * from dust'
        cur.execute(sql)
        return cur.fetchall()

    def get_all_option(self, station, date):
        # get all options fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct * from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        return cur.fetchone()

    def get_area(self, station):
        # get area fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct area from dust where station = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_code(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station_code from dust where station = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_name(self, station_code):
        # get station name fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station from dust where station_code = :code'
        cur.execute(sql, {"code": station_code})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_so2(self, station, date):
        # get SO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct so2 from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_co(self, station, date):
        # get CO fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct co from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_o3(self, station, date):
        # get O3 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct o3 from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_no2(self, station, date):
        # get NO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct no2 from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm10(self, station, date):
        # get pm10 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm25(self, station, date):
        # get pm2.5 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_address(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct address from dust where station = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_all_pm10_by_station(self, station):
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_pm10_by_station_at_time(self, station, time_from, time_to):
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station=? and hour >= ? and hour <= ?'
        cur.execute(sql, (station, time_from, time_to))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_all_by_day(self, station,year,month, day):
        cur = self.conn.cursor()
        sql = 'select distinct * from dust where station=? and year=? and month=? and day == ?'
        cur.execute(sql, (station, year, month, day))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_pm10_aver_of_station_at_time(self, station, year=-1, month=-1, day=-1, hour=-1):
        para = []

        cur = self.conn.cursor()
        sql = """ select avg(pm10)
                    from dust """
        sql_where = """where station = ? """

        all_false = True

        para.append(station)

        if year != -1:
            sql_where += "and year = ? "
            para.append(year)
            all_false = False
        if month != -1:
            sql_where += "and month = ? "
            para.append(month)
            all_false = False
        if day != -1:
            sql_where += "and day = ? "
            para.append(day)
            all_false = False
        if hour != -1:
            sql_where += "and hour = ? "
            para.append(hour)
            all_false = False
        sql_where += ";"

        if all_false:    # no parameter except station
            sql += "where station = :name;"
            cur.execute(sql, {"name": station})
        else:
            sql += sql_where
            cur.execute(sql, para)

        try:
            return cur.fetchall()
        except Exception:
            return None

    # 월별 평균 미세먼지량
    def get_pm10_aver_of_month(self, station, year, month):
        cur = self.conn.cursor()
        sql = '''select station, year, month, avg(pm10)
                    from dust
                    where station = ? and
                        year = ? and
                        month = ?;'''
        cur.execute(sql, (station, year, month))
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_pm10_aver_of_month_all_station(self, year, month):
        cur = self.conn.cursor()
        sql = '''select year, month, avg(pm10)
                    from dust
                    where year = ? and
                        month = ?;'''
        cur.execute(sql, (year, month))
        try:
            return cur.fetchall()
        except:
            return None

