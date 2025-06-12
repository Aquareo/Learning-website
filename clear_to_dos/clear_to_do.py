from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 登录信息
USERNAME = "7837212"
PASSWORD = "Leo123456@"
LOGIN_URL = "请填写登录页面网址"  # 你需要提供这个
t=1

def auto_login_with_precise_input():

    # 初始化浏览器
    service = Service('C:/Users/liu.yu133/chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    try:
        print("正在打开登录页面...")
        driver.get(LOGIN_URL)
        
        # 等待页面完全加载
        wait = WebDriverWait(driver, 15)
        time.sleep(3)
        
        print("正在查找用户名输入框...")
        # 尝试多种方式找到用户名框（工号或登录名）
        username_selectors = [
            # 通过文本内容查找
            (By.XPATH, "//input[contains(@placeholder, '用户名') or contains(@placeholder, '工号') or contains(@placeholder, '登录名')]"),
            (By.XPATH, "//label[contains(text(), '用户名') or contains(text(), '工号')]/following-sibling::input"),
            (By.XPATH, "//label[contains(text(), '用户名') or contains(text(), '工号')]/..//input"),
            # 通过常见属性查找
            (By.NAME, "username"),
            (By.NAME, "user"),
            (By.NAME, "account"),
            (By.NAME, "loginName"),
            (By.NAME, "employeeId"),
            (By.ID, "username"),
            (By.ID, "user"),
            (By.ID, "account"),
            (By.ID, "loginName"),
            # 通过类名查找
            (By.CLASS_NAME, "username"),
            (By.CLASS_NAME, "user-input"),
            # 通过位置查找（第一个输入框）
            (By.XPATH, "//form//input[@type='text'][1]"),
            (By.XPATH, "//input[@type='text'][1]"),
        ]
        
        username_input = None
        for selector_type, selector_value in username_selectors:
            try:
                username_input = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"找到用户名输入框: {selector_value}")
                break
            except:
                continue
        
        if username_input:
            # 清空并输入用户名
            username_input.clear()
            username_input.send_keys(USERNAME)
            print(f"✓ 已输入用户名: {USERNAME}")
            time.sleep(t)
        else:
            print("❌ 未找到用户名输入框")
            # 显示页面信息帮助调试
            print("页面标题:", driver.title)
            print("当前URL:", driver.current_url)
            return False
        
        print("正在查找密码输入框...")
        # 查找密码输入框
        password_selectors = [
            # 通过文本内容查找
            (By.XPATH, "//input[contains(@placeholder, '密码') or contains(@placeholder, 'OA')]"),
            (By.XPATH, "//label[contains(text(), '密码') or contains(text(), 'OA')]/following-sibling::input"),
            (By.XPATH, "//label[contains(text(), '密码') or contains(text(), 'OA')]/..//input"),
            # 通过类型查找
            (By.XPATH, "//input[@type='password']"),
            # 通过常见属性查找
            (By.NAME, "password"),
            (By.NAME, "pwd"),
            (By.NAME, "passwd"),
            (By.ID, "password"),
            (By.ID, "pwd"),
            (By.ID, "passwd"),
            # 通过类名查找
            (By.CLASS_NAME, "password"),
            (By.CLASS_NAME, "pwd-input"),
        ]
        
        password_input = None
        for selector_type, selector_value in password_selectors:
            try:
                password_input = driver.find_element(selector_type, selector_value)
                print(f"找到密码输入框: {selector_value}")
                break
            except:
                continue
        
        if password_input:
            # 清空并输入密码
            password_input.clear()
            password_input.send_keys(PASSWORD)
            print("✓ 已输入密码")
            time.sleep(t)
        else:
            print("❌ 未找到密码输入框")
            return False
        
        print("正在查找登录按钮...")
        # 查找登录按钮
        login_selectors = [
            # 新增针对"立即登录"的匹配
            (By.XPATH, "//button[contains(., '立即登录')]"),
            (By.XPATH, "//input[contains(@value, '立即登录')]"),
            (By.XPATH, "//a[contains(., '立即登录')]"),
            
            # 原有通用匹配规则
            (By.XPATH, "//button[contains(text(), '登录') or contains(text(), '登入') or contains(text(), '提交')]"),
            (By.XPATH, "//input[@value='登录' or @value='登入' or @value='提交']"),
            (By.XPATH, "//a[contains(text(), '登录') or contains(text(), '登入')]"),
            (By.ID, "login"),
            (By.ID, "submit"),
            (By.CLASS_NAME, "login-btn"),
            (By.XPATH, "//button[@type='submit']"),
        ]
        
        login_button = None
        for selector_type, selector_value in login_selectors:
            try:
                login_button = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"找到登录按钮: {selector_value}")
                break
            except:
                continue
        
        if login_button:
            # 确保按钮可见
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", login_button)
            time.sleep(0.5)  # 等待滚动动画
            
            # 使用ActionChains模拟真人点击
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).move_to_element(login_button).pause(0.3).click().perform()
            print("✓ 已执行登录按钮点击")
        else:
            print("❌ 未找到登录按钮")
            # 输出当前页面结构帮助调试
            print("当前页面片段：", driver.page_source[:2000])
            driver.save_screenshot('login_error.png')
            return False
        
        # 等待登录结果
        print("等待登录结果...")
        time.sleep(2)
        
        # 检查登录状态
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"当前页面: {page_title}")
        print(f"当前URL: {current_url}")
        
        # 简单判断是否登录成功
        if "login" not in current_url.lower() or "登录成功" in page_title:
            print("🎉 登录成功！")
            return driver  # 返回 driver 对象
        else:
            print("⚠️ 登录状态未确定，请手动检查")
            return None
            
    except Exception as e:
        print(f"❌ 登录过程中出现错误: {e}")
        return None
    finally:
        if not driver:
            driver.quit()

def search_and_delete(driver, search_content):
    try:
        print("正在查找主题搜索栏...")
        # 查找主题搜索栏
        search_bar_selectors = [
            (By.XPATH, "//input[contains(@placeholder, '搜索') or contains(@placeholder, '主题')]"),
            (By.XPATH, "//input[@type='search']"),
            (By.NAME, "search"),
            (By.ID, "search"),
            (By.CLASS_NAME, "search-bar"),
        ]
        
        search_bar = None  # 初始化变量
        selector_value = None  # 初始化变量
        for selector_type, selector_value in search_bar_selectors:
            try:
                search_bar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                print(f"找到搜索栏: {selector_value}")
                break
            except:
                continue
        
        if search_bar:
            # 清空并输入搜索内容
            search_bar.clear()
            search_bar.send_keys(search_content)
            print(f"✓ 已输入搜索内容: {search_content}")
            #time.sleep(t)
            
            # 模拟按下回车键
            search_bar.send_keys("\n")
            time.sleep(t)  # 等待搜索结果加载
        else:
            print("❌ 未找到搜索栏")
            return False
        
        print("正在查找全选框...")
        # 使用JavaScript查找全选框
        select_all_checkbox = None
        try:
            # 使用JavaScript获取第一个ant-checkbox-input元素
            checkbox_element = driver.execute_script("return document.getElementsByClassName('ant-checkbox-input')[0]")
            if checkbox_element:
                # 使用JavaScript点击元素
                driver.execute_script("arguments[0].click();", checkbox_element)
                print("✓ 已点击全选框")
                time.sleep(t)
            else:
                raise Exception("未找到全选框元素")
        except Exception as e:
            print(f"❌ 未找到全选框: {e}")
            return False
        
        print("正在查找删除按钮...")
        # 查找删除按钮 - 使用类名定位
        delete_button = None
        try:
            # 使用JavaScript获取指定类名的删除按钮
            delete_button = driver.execute_script("return document.getElementsByClassName('ant-btn ant-btn-primary ant-btn-sm')[0]")
            if delete_button:
                # 使用JavaScript点击删除按钮
                driver.execute_script("arguments[0].click();", delete_button)
                print("✓ 已点击删除按钮")
                #time.sleep(t)
            else:
                raise Exception("未找到删除按钮元素")
        except Exception as e:
            print(f"❌ 未找到删除按钮: {e}")
            return False
        
        # 确认删除（如果有弹窗）
        try:
            # 等待弹窗完全显示
            #time.sleep(t)  # 增加等待时间确保弹窗完全显示
            
            # 使用更精确的选择器定位和操作按钮
            confirm_js = """
                const button = document.querySelector('.ant-modal.ant-confirm.ant-confirm-confirm .ant-confirm-btns .ant-btn.ant-btn-primary');
                if (button) {
                    if (button.disabled) {
                        button.disabled = false;  // 移除禁用状态
                    }
                    button.click();
                    return true;
                }
                return false;
            """
            
            result = driver.execute_script(confirm_js)
            
            if result:
                print("✓ 已确认删除")
                #time.sleep(t)  # 等待删除操作完成
            else:
                print("⚠️ 未找到确认按钮")
                driver.save_screenshot('confirm_button_not_found.png')
                
        except Exception as e:
            print(f"⚠️ 确认删除时出现错误: {e}")
            driver.save_screenshot('error_screenshot.png')
        
        return True
    except Exception as e:
        print(f"❌ 搜索和删除过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 自动登录脚本 ===")
    print(f"用户名: {USERNAME}")
    print(f"密码: {'*' * len(PASSWORD)}")
    
    if LOGIN_URL == "请填写登录页面网址":
        print("\n⚠️ 请先提供登录页面的网址!")
        print("将 LOGIN_URL 变量改为实际的登录页面地址")
        login_url = input("请输入登录页面网址: ").strip()
        if login_url:
            LOGIN_URL = login_url
        else:
            print("未提供网址，程序退出")
            exit()
    
    print(f"\n正在访问: {LOGIN_URL}")
    driver = auto_login_with_precise_input()
    if driver:
        print("\n=== 开始搜索并删除 ===")
        search_content = "xxxxxx"  # 替换为实际搜索内容
        search_and_delete(driver, search_content)
        driver.quit()  # 确保退出浏览器
