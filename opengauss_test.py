import psycopg2


class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """初始化数据库连接参数"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        """连接到数据库"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("数据库连接成功")
        except psycopg2.DatabaseError as e:
            print(f"数据库连接失败: {e}")
            return None

    def close(self):
        """关闭数据库连接"""
        if self.conn is not None:
            self.conn.close()
            print("数据库连接已关闭")

    def execute_query(self, query):
        """执行查询"""
        if not self.conn:
            raise Exception("数据库连接未建立")
            return
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query)
                # 提交事务
                self.conn.commit()
                # 对于SELECT语句，返回所有结果
                if query.lower().startswith('select'):
                    return cursor.fetchall()
            except psycopg2.DatabaseError as e:
                print(f"查询执行失败: {e}")
                self.conn.rollback()
                return None


# 使用示例
if __name__ == "__main__":
    # 替换下面的参数为你的数据库实际参数
    db = Database(dbname="datachat", user="datachat", password="BJ*9CG7benkU1", host="8.130.13.53", port=5432)
    # db = Database(dbname="postgres", user="test_data;", password="BJ*9CG7benkU", host="8.131.229.55", port=5432)
    db.connect()

    # 执行一个查询示例
    query_result = db.execute_query("SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
    print(query_result)

    db.close()
