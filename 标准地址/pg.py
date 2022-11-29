import psycopg2


class PgDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="geo_info",
            user="root",
            password="root",
            host="1.14.103.216",
            port="8432",
        )

    def query_all(self):
        cur = self.conn.cursor()
        try:
            cur.execute("""select * from gch_shanghai limit 10;""")
            result = cur.fetchall()
            for item in result:
                print(item)
        except Exception as e:
            print("query_all function error: ", e)
        finally:
            cur.close()

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    pg = PgDB()
    pg.query_all()
    pg.close()
