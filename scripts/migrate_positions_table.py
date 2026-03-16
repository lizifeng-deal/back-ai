"""
数据库迁移脚本 - 重构 positions 表以适配 ContractPosition 接口
"""
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app, db
from sqlalchemy import text
import time

def migrate_positions_table():
    """迁移 positions 表结构"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'positions' in tables:
                print("检测到现有的 positions 表，开始备份数据...")
                
                # 备份现有数据
                backup_data = []
                try:
                    result = db.session.execute(text("SELECT * FROM positions"))
                    backup_data = [dict(row._mapping) for row in result]
                    print(f"备份了 {len(backup_data)} 条记录")
                except Exception as e:
                    print(f"备份数据时出错: {e}")
                
                # 删除现有表
                print("删除现有的 positions 表...")
                db.session.execute(text("DROP TABLE IF EXISTS positions"))
                
                # 删除相关的枚举类型（如果存在）
                try:
                    db.session.execute(text("DROP TYPE IF EXISTS position_side"))
                except Exception as e:
                    print(f"删除旧枚举类型时出错: {e}")
                
                db.session.commit()
            
            # 创建新表结构
            print("创建新的 positions 表结构...")
            db.create_all()
            print("新表结构创建成功！")
            
            # 如果有备份数据，尝试迁移兼容的字段
            if backup_data:
                print("尝试迁移兼容的数据...")
                migrated_count = 0
                
                for old_record in backup_data:
                    try:
                        # 映射旧字段到新字段
                        new_record = {
                            'id': old_record.get('id', f"migrated-{int(time.time() * 1000)}"),
                            'symbol': old_record.get('name', 'UNKNOWN'),  # 使用 name 作为 symbol
                            'entry_price': str(old_record.get('open_price', '0')),
                            'mark_price': str(old_record.get('market_value', '0')),  # 临时用 market_value 作为 mark_price
                            'unrealized_profit': str(old_record.get('pnl', '0')),
                            'liquidation_price': None,  # 旧数据没有该字段
                            'break_even_price': None,   # 旧数据没有该字段
                            'leverage': str(old_record.get('leverage', '1')),
                            'position_amt': str(old_record.get('quantity', '0')),
                            'position_side': 'LONG' if old_record.get('side', 'long').lower() == 'long' else 'SHORT',
                            'update_time': int(time.time() * 1000)
                        }
                        
                        # 插入迁移后的记录
                        insert_sql = text("""
                        INSERT INTO positions (
                            id, symbol, entry_price, mark_price, unrealized_profit,
                            liquidation_price, break_even_price, leverage, 
                            position_amt, position_side, update_time,
                            created_at, updated_at
                        ) VALUES (
                            :id, :symbol, :entry_price, :mark_price, :unrealized_profit,
                            :liquidation_price, :break_even_price, :leverage,
                            :position_amt, :position_side, :update_time,
                            datetime('now'), datetime('now')
                        )
                        """)
                        
                        db.session.execute(insert_sql, new_record)
                        migrated_count += 1
                        
                    except Exception as e:
                        print(f"迁移记录 {old_record.get('id', 'unknown')} 时出错: {e}")
                
                db.session.commit()
                print(f"成功迁移了 {migrated_count} 条记录")
            
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
            
        except Exception as e:
            print(f"迁移过程中发生错误: {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()

if __name__ == "__main__":
    print("开始数据库迁移...")
    migrate_positions_table()
    print("迁移完成！")