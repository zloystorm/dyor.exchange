import loguru
import asyncio
import subprocess
import random
from playwright.async_api import (
    async_playwright,
    Browser as PlaywrightBrowser,
    Error,
    Page,
    ProxySettings,
    Response,
    TimeoutError as PlaywrightTimeoutError,
)
from playwright.sync_api import Playwright, sync_playwright
from playwright_stealth import stealth_async
import logging
import os
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
good = open('registred.txt', 'a')
bad = open('unregistred.txt', 'a')


class Browser:
    def __init__(self):
        self.context = None
        self.color_schemes = ['light', 'dark', 'no-preference']
        self.locations = ['de-DE', 'fr-FR', 'es-ES', 'it-IT', ' ja-JP', 'en-AU', 'zh-CN', 'pt-BR', 'ar-AE', 'hi-IN', 'en-CA', 'en-NZ', 'pt-BR']


    async def create_page(self, link: str):
        page = await self.context.new_page()

        await page.emulate_media(color_scheme=random.choice(self.color_schemes))
        await stealth_async(page)

        await page.goto(link)
        return self.context, page


    async def create(self):
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)

        devices = playwright.devices
        device = random.choice(list(devices.values()))

        self.context = await browser.new_context(
            locale='ua-UA',
        )
        return browser


        
async def main():
    async with async_playwright() as p:
        with open('emails.txt', 'r') as file_to_emails, open('proxy.txt', 'r') as file_to_proxy:
            for jopech in file_to_emails:
                emails_login = jopech.split(':')[0]
                proxy = file_to_proxy.readline().split('@')[1]
                driver = Browser()
                browser = await driver.create()
                page = await browser.new_page()
                await page.goto("https://dyor.exchange/?r=tmMvL", timeout=60000)
                await page.get_by_placeholder("Enter your email").first.fill(emails_login)
                await asyncio.sleep(1)
                await page.locator("#hero").get_by_role("button", name="Get early access").click()

                try:
                    await page.wait_for_selector('text=Thank you for signing up! We’ve added your email to Dyor’s waiting list.', timeout=100000)
                    await asyncio.sleep(1)
                    logger.success(f'Email {emails_login} success registred')
                    good.write(f'{jopech}')
                except Exception as e:
                    logger.error(f'Email {emails_login} failed to register: {e}')
                    bad.write(f'{jopech}')
                finally:
                    #  await browser.clear_cookies()
                    await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
