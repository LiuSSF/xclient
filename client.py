import os
import sys
import time
import socket
from webdriver_setup import setup_webdriver, login
from scan import star_scan

os.environ["DISPLAY"] = ":0"

MAX_LOGIN_RETRY = 3  # 登录失败/超时时最多重试次数

def restart_program():
    """
    重启当前 Python 程序进程
    """
    print("出现超时错误，重启程序...")
    try:
        driver.quit()
    except:
        pass
    python = sys.executable
    os.execl(python, python, *sys.argv)

def init_driver_and_login():
    """
    初始化 WebDriver，并进行登录。支持多次重试。
    如果在重试次数内始终登录失败（含 read timed out），则直接重启程序。
    """
    for attempt in range(1, MAX_LOGIN_RETRY+1):
        print(f"[init_driver_and_login] 第 {attempt} 次尝试启动driver并登录...")
        driver = setup_webdriver()
        try:
            login(driver)
            print("[init_driver_and_login] 登录成功!")
            return driver  # 返回成功实例化的 driver
        except Exception as e:
            print(f"[init_driver_and_login] 登录失败: {e}")
            # 判断是否含有 read timed out 或其它关键字
            if "Read timed out" in str(e):
                # 先关闭 driver
                try:
                    driver.quit()
                except:
                    pass
                if attempt < MAX_LOGIN_RETRY:
                    # 小延时后再试
                    time.sleep(5)
                    continue
                else:
                    # 超过最大重试次数，直接重启脚本
                    restart_program()
            else:
                # 其他错误也可以 retry，或直接退出，看你的需求
                try:
                    driver.quit()
                except:
                    pass
                time.sleep(5)
                if attempt >= MAX_LOGIN_RETRY:
                    # 超过最大重试次数，退出或重启
                    restart_program()

    # 如果循环意外退出，这里再做一次重启或退出
    restart_program()

def handle_task(task):
    global driver
    print(f"正在处理任务: {task}")
    try:
        result = star_scan(driver, task)  # 这里面如果抛 Read timed out，就会被下面 except 捕获
        return f"处理完成: {result}"
    except Exception as e:
        # 判断是否超时或者其他关键错误
        if "Read timed out" in str(e):
            # 直接进行程序重启，或者只重启 driver 看需求
            print("出现超时错误，重启程序...")
            restart_program()
        # 其他异常，视需求决定如何处理
        raise

def start_client():
    global driver
    while True:  # 外层循环，确保客户端可以不断重连
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('10.0.4.8', 5000))  # 连接到服务器
            print("已连接到服务器，等待任务...")

            while True:  # 内层循环，处理任务
                try:
                    message = client.recv(1024).decode('utf-8')
                    if not message:  
                        print("服务器关闭了连接，5秒后重新连接...")
                        time.sleep(5)
                        break

                    if message == "WAITING":
                        client.send("READY".encode('utf-8'))
                        continue

                    if len(message) > 20:
                        result = handle_task(message)
                        client.send(result.encode('utf-8'))

                except (socket.error, ConnectionError) as e:
                    print(f"连接异常: {e}, 5秒后重新连接...")
                    time.sleep(5)
                    break

                except Exception as e:
                    print(f"任务处理异常: {e}")
                    # 这里可根据需要判断是否要重新连接 / 重启 / 继续
                    break

        except (socket.error, ConnectionError) as e:
            print(f"连接失败: {e}, 5秒后重新连接...")
            time.sleep(5)

        except Exception as e:
            # 如果是在连接时就报了“Read timed out”，可以在这里处理
            if "Read timed out" in str(e):
                restart_program()
            print(f"发生未知错误: {e}, 5秒后重新连接...")
            time.sleep(5)

        finally:
            try:
                client.close()
            except:
                pass
            # 如果你想在每次重连前都重置 driver，
            # 可以在这里把 driver.quit() 放进来，再去 init_driver_and_login()
            # driver.quit()
            # driver = init_driver_and_login()

if __name__ == "__main__":
    global driver
    # 先初始化一次 driver 并完成登录
    driver = init_driver_and_login()
    start_client()
