import pandas as pd
from python_codes.clear_to_do import auto_login_with_precise_input, search_and_delete
import time
import sys

def process_todo_list(excel_path: str, column_name: str = "表单编号") -> None:
    """
    处理Excel中的待办事项
    
    Args:
        excel_path: Excel文件路径
        column_name: 包含表单编号的列名，默认为"表单编号"
    """
    try:
        # 读取Excel文件
        print(f"\n=== 开始处理待办清单 ===")
        print(f"正在读取文件: {excel_path}")
        df = pd.read_excel(excel_path)
        
        if column_name not in df.columns:
            print(f"错误: 未找到列 '{column_name}'")
            return
            
        # 获取所有待处理的表单编号
        todo_items = df[column_name].dropna().unique().tolist()
        if not todo_items:
            print("没有找到需要处理的表单编号")
            return
            
        print(f"找到 {len(todo_items)} 个待处理项目")
        
        # 执行登录
        driver = auto_login_with_precise_input()
        if not driver:
            print("登录失败，无法继续处理")
            return
            
        # 处理每个待办项
        success_count = 0
        failed_items = []
        
        for index, item in enumerate(todo_items, 1):
            print(f"\n处理第 {index}/{len(todo_items)} 项: {item}")
            try:
                if search_and_delete(driver, str(item)):
                    success_count += 1
                    print(f"✓ 成功处理表单: {item}")
                else:
                    failed_items.append(item)
                    print(f"✗ 处理失败: {item}")
                    
                time.sleep(2)  # 防止操作过快
                
            except Exception as e:
                failed_items.append(item)
                print(f"处理出错: {item}, 错误信息: {str(e)}")
                continue
                
        # 输出处理结果统计
        print("\n=== 处理完成 ===")
        print(f"总计: {len(todo_items)} 项")
        print(f"成功: {success_count} 项")
        print(f"失败: {len(failed_items)} 项")
        
        # 如果有失败项，保存到新的Excel文件
        if failed_items:
            failed_df = pd.DataFrame({column_name: failed_items})
            failed_file = "failed_todos.xlsx"
            failed_df.to_excel(failed_file, index=False)
            print(f"\n失败项已保存至: {failed_file}")
            
    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

def main():
    if len(sys.argv) < 2:
        print("使用方法: python batch_clear_todos.py <Excel文件路径> [表单编号列名]")
        return
        
    excel_path = sys.argv[1]
    column_name = sys.argv[2] if len(sys.argv) > 2 else "表单编号"
    
    process_todo_list(excel_path, column_name)

if __name__ == "__main__":
    main()
