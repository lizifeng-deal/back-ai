"""
自动化数据库重建脚本
"""
import os
import sys
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def auto_rebuild():
    """自动重建数据库"""
    print("🔄 开始自动重建数据库...")
    
    try:
        # 删除数据库文件
        db_path = os.path.join(project_root, "instance", "app.db")
        if os.path.exists(db_path):
            print(f"📄 删除数据库文件: {db_path}")
            os.remove(db_path)
        
        # 重新创建应用和数据库
        print("🏗️  重新创建数据库...")
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            # 创建所有表
            db.create_all()
            print("✅ 数据库表创建成功！")
            
            # 验证表结构
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 创建的表: {tables}")
            
            if 'positions' in tables:
                columns = inspector.get_columns('positions')
                print("🔧 positions 表结构:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
            
            # 自动创建示例数据
            print("📦 创建示例数据...")
            create_sample_positions(db)
        
        print("\n🎉 数据库重建完成！")
        print("✨ 现在可以测试API了")
        
    except Exception as e:
        print(f"❌ 重建过程中出错: {e}")
        import traceback
        traceback.print_exc()

def create_sample_positions(db):
    """创建示例持仓数据"""
    from app.models.position import Position
    
    # 创建示例持仓记录
    sample_positions = [
        Position(
            id='sample-btc-long',
            symbol='BTCUSDT',
            entry_price='45000.00',
            mark_price='45150.50',
            unrealized_profit='15.05',
            liquidation_price='40000.00',
            break_even_price='45025.00',
            leverage='10',
            position_amt='0.01',
            position_side='LONG',
            update_time=int(time.time() * 1000)
        ),
        Position(
            id='sample-eth-short',
            symbol='ETHUSDT',
            entry_price='3200.00',
            mark_price='3180.25',
            unrealized_profit='19.75',
            liquidation_price='3600.00',
            break_even_price='3195.00',
            leverage='5',
            position_amt='0.5',
            position_side='SHORT',
            update_time=int(time.time() * 1000)
        ),
        Position(
            id='sample-ada-long',
            symbol='ADAUSDT',
            entry_price='0.5000',
            mark_price='0.5250',
            unrealized_profit='25.00',
            liquidation_price='0.4000',
            break_even_price='0.5005',
            leverage='20',
            position_amt='1000',
            position_side='LONG',
            update_time=int(time.time() * 1000)
        )
    ]
    
    for position in sample_positions:
        db.session.add(position)
    
    db.session.commit()
    print(f"✅ 创建了 {len(sample_positions)} 条示例记录")
    
    # 验证创建的记录
    print("📋 示例记录详情:")
    for pos in sample_positions:
        print(f"   - {pos.symbol} {pos.position_side}: {pos.position_amt} @ {pos.entry_price}")

if __name__ == "__main__":
    auto_rebuild()