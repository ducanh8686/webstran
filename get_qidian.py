from playwright.async_api import async_playwright
import asyncio
 
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # headless=False 表示浏览器可见
        page = await browser.new_page()
        
        # 打开起点中文网登录页面
        await page.goto('https://passport.qidian.com')
        
        # 填写登录表单（这里需要根据实际情况调整选择器）
        await page.fill('input[id="username"]', '+840946514859')  # 替换为你的邮箱
        await page.fill('input[id="password"]', '123bcVT!@#')  # 替换为你的密码
        await page.locator('#autologin').click(force=True)
        await page.locator('#agree5').click(force=True)
        await page.get_by_role("link", name="登 录").click(force=True)
        #await page.locator('.login-button').click(force=True)
        #await page.locator('button:text("登 录")').click()
        
        # 等待登录成功（可能需要等待页面跳转或元素加载）
        await page.wait_for_timeout(5000)  # 等待5秒
        
        # 打开一本书的阅读页面
        await page.goto('https://www.qidian.com/')  # 替换为具体的章节链接
        # them hanh dong scroll trinh duyet cho giong nguoi dung
        await page.evaluate("""() => {
    var slider = document.querySelector('.slider'); // 根据实际情况选择器调整
    slider.style.transform = 'translateX(100px)'; // 模拟滑动距离调整，具体值根据需要调整
}""")
        
        # 尝试阅读内容（可能需要处理反爬虫机制，如滑动验证等）
        content = await page.content()  # 获取页面内容，这里可能需要更复杂的处理来提取实际文本内容
        print(content)  # 打印页面内容，或者提取特定元素的内容
        
        await browser.close()
 
asyncio.run(main())