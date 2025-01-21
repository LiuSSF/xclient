import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import configparser
os.environ["DISPLAY"] = ":0" 
def get_public_ip():
    try:
        # 使用 ipify 的 API 获取外网 IP
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            # 解析返回的 JSON 数据
            ip_data = response.json()
            return ip_data['ip']
        else:
            return "无法获取外网IP地址"
    except Exception as e:
        return f"发生错误: {e}"

def custom_screenshot(driver, file, width, height):
    os.makedirs("png", exist_ok=True)  # Ensure the 'png' directory exists
    file_path = f"png/{file}"
    driver.set_window_size(width, height)
    time.sleep(1)
    driver.save_screenshot(file_path)
def setup_webdriver():
    # 关闭所有的Chrome进程
    subprocess.run(["pkill", "chrome"])
    # 获取当前目录的上层目录路径
    upper_dir = os.path.dirname(os.getcwd())
    user_data_dir = os.path.join(upper_dir, "chrome_user_1")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--lang=zh-CN')
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-hang-monitor')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-prompt-on-repost')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-translate')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # 设置隐式等待时间
    driver.implicitly_wait(10)
    stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
            )
    #driver.get("https://cn.tradingview.com/chart/R5c7qOGM/")
    #WebDriverWait(driver, 20, 1)
    #driver.implicitly_wait(10)
    return driver


def get_verification_code(google2fa):
    try:
        # 示例URL
        url = f'https://2fa.live/tok/{google2fa}'
        # 发送GET请求
        response = requests.get(url)
        
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON数据
            data = response.json()
            
            # 提取token
            token = data.get("token")
            
            if token:
                return token
            else:
                return "Token not found in the response."
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"





def login(driver):
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config.ini')
    # 获取配置项
    configname = get_public_ip()
    xuser = config.get(configname, 'user')
    xpassword = config.get(configname, 'pass')
    two_fa = config.get(configname, '2fa')
    print(xuser, xpassword, two_fa)
    driver.get("https://x.com/home?lang=zh") #   https://cn.tradingview.com/chart/R5c7qOGM/  https://cn.tradingview.com/chart/azMSont9/
    # 等待页面完全加载
    time.sleep(5)
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    time.sleep(1)
    page_title = driver.title
    print(page_title)
    custom_screenshot(driver, "log.png", 1024, 768)

    if 'Home' in page_title:
        print("登录成功")
    else:
        element = driver.find_element(By.CSS_SELECTOR, '#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010 > main > div > div > div.css-175oi2r.r-tv6buo.r-791edh.r-1euycsn > div.css-175oi2r.r-1777fci.r-nsbfu8.r-1qmwkkh > div > div.css-175oi2r > div.css-175oi2r.r-2o02ov > a > div > span > span')
        print(element.text)
        if element.text == 'Sign in':
            element.click()
            print('点击登录')
            time.sleep(5)
            custom_screenshot(driver, "Sign in.png", 1024, 768)
            username = driver.find_element(By.CSS_SELECTOR, '#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div > div > div > div.css-175oi2r.r-1mmae3n.r-1e084wi.r-13qz1uu > label > div > div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-is05cd.r-ttdzmv > div > input')
            username.send_keys(xuser) #fuxiaoman800@gmail.com fuxiaoman1@gmail.com
            print('输入账号')
            custom_screenshot(driver, "login.png", 1024, 768)
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div/span/span')))
            login_button.click()
            print('点击下一步')
            custom_screenshot(driver, "login1.png", 1024, 768)
            try:
                time.sleep(5)
                user = driver.find_element(By.CSS_SELECTOR, '#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1dqxon3 > div > div.css-175oi2r.r-1mmae3n.r-1e084wi > label > div > div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-is05cd.r-ttdzmv > div > input')
                user.send_keys(xuser+'@mifas.com.tr') #fuxiaoman800@gmail.com fuxiaoman1@gmail.com
                print('输入用户')
                custom_screenshot(driver, "login2.png", 1024, 768)
                login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')))
                login_button.click()
                print('点击下一步')
                custom_screenshot(driver, "login3.png", 1024, 768)
            except:
                pass
            time.sleep(5)
            custom_screenshot(driver, "pass0.png", 1024, 768)
            password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1dqxon3 > div > div > div.css-175oi2r.r-1e084wi.r-13qz1uu > div > label > div > div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-is05cd.r-ttdzmv > div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-135wba7.r-16dba41.r-1awozwy.r-6koalj.r-1inkyih.r-13qz1uu > input")))
            password.send_keys(xpassword) #fuxiaoman800@gmail.com fuxiaoman1@gmail.com
            print('输入密码')
            custom_screenshot(driver, "pass01.png", 1024, 768)
            custom_screenshot(driver, "pass.png", 1024, 768)
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div/span/span')))
            login_button.click()
            print('点击下一步')
            custom_screenshot(driver, "pass1.png", 1024, 768)
            time.sleep(5)
            password2fa = driver.find_element(By.CSS_SELECTOR, '#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-kemksi.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-f8sm7e.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1dqxon3 > div > div.css-175oi2r.r-1mmae3n.r-1e084wi > label > div > div.css-175oi2r.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1wzrnnt.r-1udh08x.r-xd6kpl.r-is05cd.r-ttdzmv > div > input')
            password2fa.send_keys(get_verification_code(two_fa)) #fuxiaoman800@gmail.com fuxiaoman1@gmail.com
            custom_screenshot(driver, "2fa.png", 1024, 768)
            login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span')))
            login_button.click()
            custom_screenshot(driver, "2fa1.png", 1024, 768)
            time.sleep(5)
            
            WebDriverWait(driver, 20).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            page_title = driver.title
            if 'Home' in page_title:
                print("登录成功")        
# # 获取验证码
# verification_code = get_verification_code('KHRAQE4TP6V7RSFO')
# print("Verification Code:", verification_code)
