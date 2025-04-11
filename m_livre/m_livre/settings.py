# Scrapy settings for m_livre project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = "m_livre"

SPIDER_MODULES = ["m_livre.spiders"]
NEWSPIDER_MODULE = "m_livre.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "m_livre (+http://www.yourdomain.com)"
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#USER_AGENT = shadow_useragent.firefox
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "m_livre.middlewares.MLivreSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "m_livre.middlewares.MLivreDownloaderMiddleware": 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #"m_livre.pipelines.MLivrePipeline": 300,
    #"m_livre.pipelines.MagaluPipeline":200,
    "m_livre.pipelines.CorePipeline": 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False


# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "firefox"
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000  # 30 seconds
PLAYWRIGHT_DEBUG = True  # Enable verbose logging
PLAYWRIGHT_LAUNCH_OPTIONS = {
            "headless": True,
            "timeout": 60000,  # Increase to 60 seconds
            #"args": [
                #"--disable-blink-features=AutomationControlled",
                #"--no-sandbox",
                #"--single-process",
                #"--disable-dev-shm-usage",
                #"--disable-web-security",
                #"--aggressive-cache-discard",
                #"--disable-cache",
                #"--disable-application-cache",
                #"--disable-offline-load-stale-cache",
                #"--disk-cache-size=0",
                #"--disable-back-forward-cache",
                #"--disable-notifications",
                #"--disable-popup-blocking",
            #],
        },
PLAYWRIGHT_MAX_CONTEXTS = 4  # Limit concurrent contexts


# Enable Redis as the scheduler and dupefilter
#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#SCHEDULER_PERSIST = True  # Persist jobs across spider runs

# Redis connection settings
REDIS_URL = 'redis://localhost:6379'  # Default Redis URL
## Insert Your List of Proxies Here
USER_NAME='bravebrave'
USER_PASS='Proxy_1728_Brave'
ROTATING_PROXY_LIST = [
    #f'http://{USER_NAME}:{USER_PASS}@unblock.oxylabs.io:60000',
    f'https://{USER_NAME}:{USER_PASS}@unblock.oxylabs.io:60000',
    #'193.181.35.133:8118',
    #'185.82.126.195:8080',
    #'https://159.65.56.88:8888',
    #'83.217.23.35:8090',
    #'https://86.98.222.71:8080',
    #'13.38.176.104:3128',
    #'43.156.148.170',
]

# Enable rotating proxies
#ROTATING_PROXY_LIST_PATH = 'proxies.txt'  # Path to your proxy list file
"""DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}
"""
# Optional: Set a delay between requests to avoid being blocked
#DOWNLOAD_DELAY = 2ß
DATABASE_URI = "postgresql://scrapy:scrapy@db:5432/scrapy"