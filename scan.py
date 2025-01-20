import time
import re
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
def custom_screenshot(driver, file, width, height):
    os.makedirs("png", exist_ok=True)  # Ensure the 'png' directory exists
    file_path = f"png/{file}"
    driver.set_window_size(width, height)
    time.sleep(1)
    driver.save_screenshot(file_path)
def star_scan(driver, address):
    # 打开搜索页面
    driver.get(f"https://x.com/search?q={address}&src=recent_search_click")
    
    # 等待页面完全加载
    time.sleep(5)
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    custom_screenshot(driver, "scan1.png", 1024, 768)

    # 定义要执行的 JavaScript 代码
    js_code = """
    const firstTweet = document.querySelector('article[data-testid="tweet"]');
    let result = {};

    if (firstTweet) {
        // 查找用户名
        const usernameElement = firstTweet.querySelector('div[dir="ltr"] > span');
        const username = usernameElement ? usernameElement.innerText : '未知用户名';
        result["username"] = username;

        // 查找认证状态
        const badgeElement = firstTweet.querySelector('svg[aria-label]');
        if (badgeElement) {
            const badgeLabel = badgeElement.getAttribute('aria-label');
            if (badgeLabel.includes('organization') || badgeLabel.includes('account')) {
                // 用户是认证的，获取个人页面地址
                const profileLink = firstTweet.querySelector('a[href^="/"]');
                if (profileLink) {
                    // 点击用户链接
                    profileLink.click();

                    // 等待页面加载完成
                    await new Promise(resolve => setTimeout(resolve, 5000));  // 等待 5 秒

                    // 获取粉丝数量
                    const getUserInfo = () => {
                        try {
                            // 获取粉丝数量
                            const followersElement = document.querySelector('a[href*="/verified_followers"] span');
                            const followers = followersElement ? followersElement.textContent.trim() : '未知';
                            return followers;
                        } catch (error) {
                            console.error('获取用户信息时出错:', error);
                            return '未知';
                        }
                    };

                    // 调用函数并获取粉丝数量
                    const followers = getUserInfo();
                    result["followers"] = followers;
                    result["profile_url"] = `https://x.com${profileLink.getAttribute('href')}`;
                    result["badge_type"] = badgeLabel.includes('organization') ? '金色认证' : '蓝色认证';
                }
            } else {
                result["badge_type"] = '用户没有认证';
            }
        }
    } else {
        result["error"] = '未找到推文';
    }

    // 返回结果
    return result;
    """
    custom_screenshot(driver, "scan2.png", 1024, 768)
    # 执行 JavaScript 代码并获取返回值
    result = driver.execute_script(js_code)
    print(result)
    # 如果 result 是字典，检查 profile_url
    if isinstance(result, dict):
        return result  # 如果没有找到，返回原始结果
    else:
        return result