from website import create_app, db
from website.models import SharedPermission

app = create_app()

with app.app_context():
    # 尝试获取 SharedPermission 表的所有记录
    try:
        records = SharedPermission.query.all()
        print(f"✅ 数据库已成功创建 SharedPermission 表，共有 {len(records)} 条记录。")
    except Exception as e:
        print(f"❌ 发生错误，可能是 SharedPermission 表未创建：{e}")
