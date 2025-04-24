from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.reactor import install_reactor
from scrapy.settings import Settings
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

settings = Settings()
os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.crawlers.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')

#settings = get_project_settings()

process = CrawlerProcess(settings)

def crawl_spider(spider_name):
    process.crawl(spider_name)
    process.start()

from twisted.internet import reactor
from twisted.python import log

class SpiderRunner:

    def __init__(self, settigns=settings):
        configure_logging()
        self.runner = CrawlerRunner(settings)
        self.observer = log.PythonLoggingObserver()
        self.observer.start()

    def run(self, spider_name, curva=None,**kwargs):
        deferred = self.runner.crawl(spider_name, eans=curva, **kwargs)
        #deferred.addCallback(self._stop_reactor)
        #deferred.addErrback(self._handle_error)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=0)
        self.observer.stop()

    def _stop_reactor(self, result):
        if reactor.running:
            reactor.stop()
        return result

    def _handle_error(self, failure):
        self.observer.stop()
        print(f"Spider failed: {failure.getTraceback()}")
        if reactor.running:
            reactor.stop()