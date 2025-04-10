mercado_livre:
	cd m_livre && scrapy crawl ml_simple_db
magalu:
	cd m_livre && scrapy crawl magalu_simple_db
carrefas:
	cd m_livre && scrapy crawl carrefas_simple_db
leroy:
	cd m_livre && scrapy crawl leroy_simple_db
build:
	docker build . -t scrapy
docker:
	docker compose run --rm dev
attach:
	docker exec -it scrapy /bin/bash