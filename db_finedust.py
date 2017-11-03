import sqlite3
import csv


class DBFineDust:
    _sql_create_dust_table = """ CREATE TABLE IF NOT EXISTS dust (
                    area text NOT NULL,
                    station_code integer NOT NULL,
                    station_name text NOT NULL,
                    date integer NOT NULL,
                    so2 real,
                    co real,
                    o3 real,
                    no2 real,
                    pm10 integer,
                    pm25 integer,
                    address text,
                    primary key(station_name, date)                    
                    ); """

    def __init__(self, db_file):
        self.db_file = db_file

        # create a database connection
        self.conn = self._create_connection(db_file)

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_dust_table)
        else:
            print("E : cannot create the DB connection")

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

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
                self._insert_table(self.conn, self._sql_insert_dust_table, line)
        self.conn.commit()
        file.close()

    def get_row_num(self):
        cur = self.conn.cursor()
        sql = 'select count(*) from dust'
        cur.execute(sql)
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
        sql = 'select distinct * from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        return cur.fetchone()

    def get_area(self, station):
        # get area fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct area from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_code(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station_code from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_station_name(self, station_code):
        # get station name fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct station_name from dust where station_code = :code'
        cur.execute(sql, {"code": station_code})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_so2(self, station, date):
        # get SO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct so2 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_co(self, station, date):
        # get CO fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct co from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_o3(self, station, date):
        # get O3 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct o3 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_no2(self, station, date):
        # get NO2 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct no2 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm10(self, station, date):
        # get pm10 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm10 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_pm25(self, station, date):
        # get pm2.5 fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct pm25 from dust where station_name=? and date=?'
        cur.execute(sql, (station, date))
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    def get_address(self, station):
        # get station code fit to station and date
        cur = self.conn.cursor()
        sql = 'select distinct address from dust where station_name = :name'
        cur.execute(sql, {"name": station})
        try:
            return cur.fetchone()[0]
        except Exception:
            return None

    _sql_insert_dust_table = 'insert into dust(' \
                             'area,' \
                             'station_code,' \
                             'station_name,' \
                             'date,' \
                             'so2,' \
                             'co,' \
                             'o3,' \
                             'no2,' \
                             'pm10,' \
                             'pm25,' \
                             'address' \
                             ') values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

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
            print("error : ", e)

    @staticmethod
    def _insert_table(conn, insert_table_sql, values):
        try:
            cursor = conn.cursor()
            cursor.execute(insert_table_sql, values)
        except Exception as e:
            print("error : ", e)
