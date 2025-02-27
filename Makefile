mercado_livre:
	scrapy crawl ml_simple_db
magalu:
	scrapy crawl magalu_simple_db
carrefas:
	scrapy crawl carrefas_simple_db
build:
	docker build . -t scrapy
docker:
	docker compose run --rm dev	
attach:
	docker exec -it scrapy /bin/bash