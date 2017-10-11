import MySQLdb

from config import Config


class FaXuanUserInfo:
    user_name = ''
    password = ''
    province = ''
    cpc = 0

    def __init__(self, user_name, password, province, cpc):
        self.user_name = user_name
        self.password = password
        self.province = province
        self.cpc = cpc


class MySqlConn:
    host = Config.get_str('mysql', 'host')
    port = Config.get_str('mysql', 'port')
    user = Config.get_str('mysql', 'user')
    passwd = Config.get_str('mysql', 'passwd')
    db = Config.get_str('mysql', 'db')
    is_multi_thread = False

    __is_connected = False
    __connection = None

    def __init__(self):
        self.__connect()
        pass

    def is_connected(self):
        return self.__is_connected

    def close(self):
        self.__connection.close()

    def __connect(self):
        self.__connection = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                            db=self.db)

    def execute_query_sql(self, sql):
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_sql_no_return(self, sql):
        cursor = self.__connection.cursor()
        cursor.execute(sql)
        cursor.close()


class MySqlHelper:
    def __init__(self):
        pass

    @staticmethod
    def insert_user_info(connection, user_info_obj):
        sql = "INSERT INTO user_info VALUES ('" + user_info_obj.user_name + "','" + user_info_obj.password + "','" + user_info_obj.province + "', user_info_obj.cpc)"
        connection.execute_sql_no_return(sql)


if __name__ == '__main__':
    # query_user_info()
    mysql_conn = MySqlConn()
    insert_sql = "INSERT INTO user_info VALUES ('12345678','123456','yunnan',0)"
    mysql_conn.execute_sql_no_return(insert_sql)
    results = mysql_conn.execute_query_sql('select * from user_info')
    for r in results:
        print r
