import sqlite3
import openpyxl


class DBPortShip:
    table = 'ship'
    _sql_create_ship_table = """ CREATE TABLE IF NOT EXISTS ship (
                            port text,
                            date integer,
                            count integer,
                            GT integer,
                            year integer,
                            month integer,
                            primary key(port, date)                    
                            ); """

    def __init__(self, conn):
        self.conn = conn

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_ship_table)
        else:
            print("E : cannot create the DB connection")

            # drop and create

    def reset_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE ''' + self.table)
        self.conn.commit()

        self._create_table(self.conn, self._sql_create_ship_table)

    _sql_insert_ship_table = """insert into ship(
                                    port,
                                    date,
                                    count,
                                    GT,
                                    year,
                                    month
                                    ) values (?, ?, ?, ?, ?, ?)"""

    def insert_from_xls(self, xls_files, years, port):
        for year_index, file_name in enumerate(xls_files):
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active

            cells = ws['E4':'AB4']

            for row in cells:
                values = []
                year = years[year_index]
                month = 0

                for i, cell in enumerate(row):
                    if i % 2 == 0:  # count
                        month = month + 1
                        date = int(str(year) + ('0' + str(month))[-2:])
                        count = cell.value

                        values.append(port)
                        values.append(date)
                        values.append(count)

                    else:           # GT
                        GT = cell.value

                        values.append(GT)
                        values.append(year)
                        values.append(month)
                        self._insert_table(self.conn, self._sql_insert_ship_table, values)
                        values = []

            self.conn.commit()
            wb.close()
            print("db ship count file", file_name, "insert finish")

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
            print("insert error : ", e)

    def get_all(self):
        cur = self.conn.cursor()
        sql = """select * from ship"""
        cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_ship_data(self, port):
        cur = self.conn.cursor()

        sql = """ select port, year, month, count
                    from ship
                    where port = :port;"""
        cur.execute(sql, {'port': port})
        try:
            return cur.fetchall()
        except:
            return None
