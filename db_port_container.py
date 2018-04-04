import sqlite3
import openpyxl


class DBPortContainer:
    table = 'container'
    _sql_create_container_table = """ CREATE TABLE IF NOT EXISTS container (
                            port text,
                            date integer,
                            TEU real,
                            year integer,
                            month integer,
                            primary key(port, date)                    
                            ); """

    def __init__(self, conn):
        self.conn = conn

        if self.conn is not None:
            # create table
            self._create_table(self.conn, self._sql_create_container_table)
        else:
            print("E : cannot create the DB connection")

            # drop and create

    def reset_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''DROP TABLE ''' + self.table)
        self.conn.commit()

        self._create_table(self.conn, self._sql_create_container_table)

    _sql_insert_container_table = """insert into container(
                                    port,
                                    date,
                                    TEU,
                                    year,
                                    month
                                    ) values (?, ?, ?, ?, ?)"""

    def insert_from_xls(self, xls_files, years, port):
        for year_index, file_name in enumerate(xls_files):
            wb = openpyxl.load_workbook(file_name)
            ws = wb.active

            year = years[year_index]
            cells = ws['B4':'C15']

            for row in cells:
                values = []

                month = row[0].value
                teu = row[1].value

                date = int(str(year) + month)

                values.append(port)
                values.append(date)
                values.append(teu)
                values.append(year)
                values.append(int(month))

                self._insert_table(self.conn, self._sql_insert_container_table, values)

            self.conn.commit()
            wb.close()
            print("db ship container file", file_name, "insert finish")


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
        sql = """select * from container"""
        cur.execute(sql)
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_container_data(self, port):
        cur = self.conn.cursor()
        sql = """select port, year, month, TEU
                    from container
                    where port = :port"""
        cur.execute(sql, {'port': port})
        try:
            return cur.fetchall()
        except Exception:
            return None

    def get_container_data_in_year(self, port, year):
        cur = self.conn.cursor()
        sql = """select port, year, month, TEU
                    from container
                    where port = ? and
                        year = ?"""
        cur.execute(sql, (port, year))
        try:
            return cur.fetchall()
        except Exception:
            return None
