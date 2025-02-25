import os
import psycopg2
from dotenv import load_dotenv

# 确保加载 .env 文件
load_dotenv()

# 打印环境变量，检查是否正确加载
database_url = os.environ.get('DATABASE_URL')
print("DATABASE_URL:", database_url)

try:
    conn = psycopg2.connect(database_url)
    print("数据库连接成功！")
    conn.close()
except Exception as e:
    print("连接错误类型:", type(e))
    print("连接错误详细信息:", str(e)) 