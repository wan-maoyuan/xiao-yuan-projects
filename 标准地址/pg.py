import psycopg2
import os
import configparser


class ConnInfo:
    def __init__(self):
        pwd = os.path.split(os.path.realpath(__file__))[0]
        configPath = os.path.join(pwd, "config.ini")

        conf = configparser.ConfigParser()
        conf.read(configPath)
        self.dbname = conf.get("postgres", "dbname")
        self.user = conf.get("postgres", "user")
        self.password = conf.get("postgres", "password")
        self.host = conf.get("postgres", "host")
        self.port = conf.get("postgres", "port")


class PgDB:
    def __init__(self):
        config = ConnInfo()
        self.conn = psycopg2.connect(
            dbname=config.dbname,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port,
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
