madeira:
	cd core/apps/pricing_dular1 && python spider_madeira_async.py
mercado_livre:
	cd core/apps/crawler && scrapy crawl ml_simple_db
magalu:
	cd core/apps/crawler && scrapy crawl magalu_simple_db
carrefas:
	cd core/apps/crawler && scrapy crawl carrefas_simple_db
leroy:
	cd core/apps/crawler && scrapy crawl leroy_simple_db
build:
	docker build . -t scrapy
docker:
	docker compose run --rm dev
attach:
	docker exec -it scrapy /bin/bash