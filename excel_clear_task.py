import pandas as pd
from clear_to_dos.clear_to_do import auto_login_with_precise_input, search_and_delete
import sys
import time

def process_excel_tasks(excel_path: str, column_name: str) -> None:
    """
    处理Excel文件中的任务并执行删除操作
    
    Args:
        excel_path: Excel文件路径
        column_name: 包含要删除内容的列名
    """
    try:
        # 读取Excel文件
        print(f"正在读取Excel文件: {excel_path}")
        df = pd.read_excel(excel_path)
        
        if column_name not in df.columns:
            print(f"错误: 列名 '{column_name}' 在Excel文件中不存在")
            return
            
        # 获取要删除的内容列表(去重和去除空值)
        items = df[column_name].dropna().unique().tolist()
        if not items:
            print("没有找到要删除的内容")
            return
            
        print(f"找到 {len(items)} 个待删除项目")
        
        # 执行登录
        print("\n=== 开始自动登录 ===")
        driver = auto_login_with_precise_input()
        if not driver:
            print("登录失败，程序退出")
            return
            
        # 逐个处理删除任务
        success_count = 0
        for index, item in enumerate(items, 1):
            print(f"\n正在处理第 {index}/{len(items)} 项: {item}")
            if search_and_delete(driver, item):
                success_count += 1
                time.sleep(2)  # 等待操作完成
                
        # 输出结果统计
        print(f"\n=== 任务完成 ===")
        print(f"总计: {len(items)} 项")
        print(f"成功: {success_count} 项")
        print(f"失败: {len(items) - success_count} 项")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

def main():
    if len(sys.argv) != 3:
        print("使用方法: python excel_clear_task.py <Excel文件路径> <列名>")
        return
        
    excel_path = sys.argv[1]
    column_name = sys.argv[2]
    
    process_excel_tasks(excel_path, column_name)

if __name__ == "__main__":
    main()
