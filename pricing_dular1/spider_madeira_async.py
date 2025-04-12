# -*- coding: utf-8 -*-
"""Enhanced with asynchronous processing using Playwright and async SQLAlchemy"""
import asyncio
from playwright.async_api import async_playwright
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker as async_sessionmaker
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, BigInteger, DateTime
from sqlalchemy.sql import func
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import time

Base = declarative_base()

DATABASE_URI = "postgresql+asyncpg://scrapy:scrapy@db:5432/scrapy"


class Core_Model(Base):
    __tablename__ = 'core'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seller = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    url = Column(Text, nullable=False)
    ean = Column(BigInteger, nullable=False)
    date_now = Column(DateTime, server_default=func.now())


engine = create_async_engine(DATABASE_URI)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

base_url = 'https://www.madeiramadeira.com.br/busca'
concurrency_limit = 10  # Adjust based on system capacity


def get_things_done(element):
    try:
        json_loads = element.text
        pattern_price = re.compile(r'R\$(\d+\.\d+\,\d{2}|\d+\,\d{2}|\d+)')
        pattern_name = re.compile(r'(.*?)R\$')
        prices = re.findall(pattern_price, json_loads)[0]
        names = re.findall(pattern_name, json_loads)[0]
        return names, prices
    except Exception:
        print("****************** Fail to get PRICE *******************")
        return 'empty', 0


async def fetch_eans():
    async with async_session() as session:
        result = await session.execute(text("""SELECT description, ean FROM "dular_eans" """))
        return result.fetchall()


async def process_ean(browser, semaphore, ean, product_name):
    async with semaphore:
        try:
            encoded_query = quote(product_name)
            url = f"{base_url}?q={encoded_query}"

            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await page.wait_for_selector('div.cav--c-gqwkJN', timeout=30000)

            html = await page.content()
            await page.close()

            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.find_all('div', {
                'class': 'cav--c-gqwkJN cav--c-gqwkJN-knmidH-justifyContent-spaceBetween cav--c-gqwkJN-ieFWNPI-css'})

            async with async_session() as session:
                for element in elements:
                    name, price = get_things_done(element)
                    price_val = float(price.replace('R$', '').replace('.', '').replace(',', '.').strip())

                    record = Core_Model(
                        seller='Madeira Madeira',
                        name=name,
                        price=price_val,
                        url=url,
                        ean=int(ean)
                    )
                    session.add(record)
                    await session.commit()
                print(f"Processed EAN: {ean}")
        except Exception as e:
            print(f"Error processing {ean}: {str(e)}")
            async with async_session() as session:
                record = Core_Model(
                    seller='Madeira Madeira',
                    name='empty',
                    price=0,
                    url=url,
                    ean=ean
                )
                session.add(record)
                await session.commit()


async def main():
    semaphore = asyncio.Semaphore(concurrency_limit)
    ean_list = await fetch_eans()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )

        tasks = []
        for row in ean_list:
            product_name = str(row[0]).strip()
            ean = row[1]
            tasks.append(
                process_ean(browser, semaphore, ean, product_name)
            )

        await asyncio.gather(*tasks)
        await browser.close()


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"\nExecution time: {time.time() - start_time} seconds")