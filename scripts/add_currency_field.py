"""
为 positions 表添加 currency 字段的迁移脚本
"""
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db
from sqlalchemy import text

def add_currency_column():
    """为 positions 表添加 currency 字段"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 开始为 positions 表添加 currency 字段...")
            
            # 检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'positions' not in tables:
                print("❌ positions 表不存在，请先运行基础迁移脚本")
                return
            
            # 检查 currency 字段是否已存在
            columns = inspector.get_columns('positions')
            column_names = [col['name'] for col in columns]
            
            if 'currency' in column_names:
                print("✅ currency 字段已存在，无需添加")
                print("📋 当前表结构:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
                return
            
            print("📄 当前表结构:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            print("\n🔧 添加 currency 字段...")
            
            # 添加 currency 字段，默认值为 'USDT'
            alter_sql = text("ALTER TABLE positions ADD COLUMN currency VARCHAR(16) NOT NULL DEFAULT 'USDT'")
            db.session.execute(alter_sql)
            db.session.commit()
            
            print("✅ currency 字段添加成功！")
            
            # 验证字段添加
            inspector = inspect(db.engine)
            columns = inspector.get_columns('positions')
            print("\n📋 更新后的表结构:")
            for col in columns:
                print(f"   - {col['name']}: {col['type']}")
            
            # 验证现有数据
            result = db.session.execute(text("SELECT COUNT(*) FROM positions"))
            record_count = result.scalar()
            print(f"\n📊 表中现有记录数: {record_count}")
            
            if record_count > 0:
                # 查看一些示例记录
                result = db.session.execute(text("SELECT id, symbol, currency FROM positions LIMIT 3"))
                rows = result.fetchall()
                print("📋 示例记录:")
                for row in rows:
                    print(f"   - {row[0]}: {row[1]} ({row[2]})")
            
            print("\n🎉 迁移完成！")
            print("💡 提示: 所有现有记录的 currency 字段已设置为默认值 'USDT'")
            
        except Exception as e:
            print(f"❌ 迁移过程中发生错误: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
        finally:
            db.session.close()

if __name__ == "__main__":
    add_currency_column()