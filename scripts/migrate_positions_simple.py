"""
简化的数据库迁移脚本 - 使用 ORM 方式重构 positions 表
"""
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db
import time

def migrate_positions_table_orm():
    """使用 ORM 方式迁移 positions 表结构"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始数据库迁移（ORM 方式）...")
            
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'positions' in tables:
                print("检测到现有的 positions 表")
                
                # 简单方式：直接删除旧表并创建新表
                # 注意：这将丢失现有数据，建议在重要环境中先手动备份
                print("⚠️  警告：此操作将删除现有的 positions 表数据")
                print("如需保留数据，请先手动备份")
                
                response = input("是否继续？(y/N): ")
                if response.lower() != 'y':
                    print("迁移已取消")
                    return
                
                # 删除所有表并重建
                print("删除现有表结构...")
                db.drop_all()
                db.session.commit()
            
            # 创建新表结构
            print("创建新的表结构...")
            db.create_all()
            db.session.commit()
            
            print("\n=== 迁移完成 ===")
            print("新的 positions 表已创建，包含以下字段：")
            print("- id: 主键")
            print("- symbol: 交易对符号")
            print("- entry_price: 开仓均价")
            print("- mark_price: 标记价格") 
            print("- unrealized_profit: 未实现盈亏")
            print("- liquidation_price: 强平价格")
            print("- break_even_price: 保本价格")
            print("- leverage: 杠杆倍数")
            print("- position_amt: 持仓数量")
            print("- position_side: 持仓方向 (LONG/SHORT)")
            print("- update_time: 更新时间戳（毫秒）")
            print("- created_at: 记录创建时间")
            print("- updated_at: 记录更新时间")
            
            print("\n建议:")
            print("1. 使用 POST /positions/from-binance 从币安同步最新持仓数据")
            print("2. 或使用 POST /positions/batch 批量导入历史数据")
            
        except Exception as e:
            print(f"迁移过程中发生错误: {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()

def create_sample_data():
    """创建示例数据"""
    app = create_app()
    
    with app.app_context():
        try:
            from app.models.position import Position
            
            # 检查是否已有数据
            existing_count = Position.query.count()
            if existing_count > 0:
                print(f"表中已有 {existing_count} 条记录，跳过创建示例数据")
                return
            
            print("创建示例持仓数据...")
            
            # 创建一些示例持仓记录
            sample_positions = [
                {
                    'id': 'sample-btc-long',
                    'symbol': 'BTCUSDT',
                    'entry_price': '45000.00',
                    'mark_price': '45150.50',
                    'unrealized_profit': '15.05',
                    'liquidation_price': '40000.00',
                    'break_even_price': '45025.00',
                    'leverage': '10',
                    'position_amt': '0.01',
                    'position_side': 'LONG',
                    'update_time': int(time.time() * 1000)
                },
                {
                    'id': 'sample-eth-short',
                    'symbol': 'ETHUSDT',
                    'entry_price': '3200.00',
                    'mark_price': '3180.25',
                    'unrealized_profit': '19.75',
                    'liquidation_price': '3600.00',
                    'break_even_price': '3195.00',
                    'leverage': '5',
                    'position_amt': '0.5',
                    'position_side': 'SHORT',
                    'update_time': int(time.time() * 1000)
                }
            ]
            
            for pos_data in sample_positions:
                position = Position(
                    id=pos_data['id'],
                    symbol=pos_data['symbol'],
                    entry_price=pos_data['entry_price'],
                    mark_price=pos_data['mark_price'],
                    unrealized_profit=pos_data['unrealized_profit'],
                    liquidation_price=pos_data['liquidation_price'],
                    break_even_price=pos_data['break_even_price'],
                    leverage=pos_data['leverage'],
                    position_amt=pos_data['position_amt'],
                    position_side=pos_data['position_side'],
                    update_time=pos_data['update_time']
                )
                db.session.add(position)
            
            db.session.commit()
            print(f"成功创建了 {len(sample_positions)} 条示例记录")
            
        except Exception as e:
            print(f"创建示例数据时出错: {e}")
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == "__main__":
    # 执行迁移
    migrate_positions_table_orm()
    
    # 询问是否创建示例数据
    response = input("\n是否创建示例持仓数据？(y/N): ")
    if response.lower() == 'y':
        create_sample_data()
    
    print("\n迁移完成！")