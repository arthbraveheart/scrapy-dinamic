from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

def crawl_spider(spider_name):
    process.crawl(spider_name)
    process.start()

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.python import log
from scrapy.utils.reactor import install_reactor

install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")


class SpiderRunner:
    def __init__(self, settings=None):
        configure_logging()
        self.runner = CrawlerRunner(get_project_settings())
        self.observer = log.PythonLoggingObserver()
        self.observer.start()

    def run(self, spider_name, curva=None,**kwargs):
        deferred = self.runner.crawl(spider_name, eans=curva, **kwargs)
        deferred.addCallback(self._stop_reactor)
        deferred.addErrback(self._handle_error)
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