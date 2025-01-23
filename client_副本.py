import socket
import time
import os
import sys
from webdriver_setup import setup_webdriver, login
from scan import star_scan

os.environ["DISPLAY"] = ":0" 

def restart_program():
    """
    重启当前Python程序进程
    """
    print("出现超时错误，重启程序...")
    # 如果 WebDriver 等资源需要先行关闭，这里可处理
    try:
        driver.quit()
    except:
        pass
    python = sys.executable
    os.execl(python, python, *sys.argv)


def handle_task(task):
    """
    处理任务：如果遇到指定的 'Read timed out' 错误，则重启程序
    """
    global driver  # 使用全局变量
    print(f"正在处理任务: {task}")

    try:
        # 此处调用到 star_scan，内部可能会抛出 "Read timed out"
        scan = star_scan(driver, task)
        return f"处理完成: {scan}"

    except Exception as e:
        # 判断是否为超时错误（关键字仅供参考，具体要看你捕获到的实际异常信息）
        if "Read timed out" in str(e):
            restart_program()  # 重启程序
        else:
            # 如果是其他异常，就把异常再抛出去或做其他处理
            raise


def start_client():
    """
    启动客户端
    """
    global driver  # 使用全局变量

    while True:  # 外层循环，确保客户端可以不断重连
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('10.0.4.8', 5000))  # 连接到服务器
            print("已连接到服务器，等待任务...")

            while True:  # 内层循环，处理任务
                try:
                    # 接收服务器发送的消息
                    message = client.recv(1024).decode('utf-8')
                    if not message:  # 如果 recv 返回空字符串，说明服务器关闭了连接
                        print("服务器关闭了连接，5秒后重新连接...")
                        break  # 退出内层循环，重新连接

                    if message == "WAITING":
                        # 如果没有任务，通知服务器已准备好
                        client.send("READY".encode('utf-8'))
                        continue

                    # 处理任务
                    if len(message) > 20:
                        result = handle_task(message)
                        # 将结果发送回服务器
                        client.send(result.encode('utf-8'))

                except (socket.error, ConnectionError) as e:
                    print(f"连接异常: {e}, 5秒后重新连接...")
                    time.sleep(5)  # 等待5秒后重试
                    break  # 退出内层循环，重新连接

                except Exception as e:
                    print(f"任务处理异常: {e}")
                    # 如果任务处理失败，这里视需求处理：
                    # - 直接 break 重连，
                    # - 或者继续下一轮 recv()
                    break  # 退出内层循环，重新连接

        except (socket.error, ConnectionError) as e:
            print(f"连接失败: {e}, 5秒后重新连接...")
            time.sleep(5)  # 等待5秒后重试

        except Exception as e:
            # 如果这里捕获到任何其他未知错误，也可以选择在这里重启
            if "Read timed out" in str(e):
                restart_program()
            print(f"发生未知错误: {e}, 5秒后重新连接...")
            time.sleep(5)  # 等待5秒后重试

        finally:
            # 每次连接失败后，关闭旧的连接
            try:
                client.close()
            except:
                pass
            # 若这里需要重建 WebDriver，也可放在此处
            # driver = setup_webdriver()
            # login(driver)


if __name__ == "__main__":
    global driver  # 使用全局变量
    driver = setup_webdriver()
    try:
        login(driver)
    except Exception as e:
        print(f"登录失败: {e}")
        driver.quit()
        sys.exit(1)  # 登录失败就退出，或根据需要进行重启

    start_client()
