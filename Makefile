build:
	docker-compose build

run: stop
	docker-compose up -d

stop:
	docker-compose stop

test:
	docker-compose run web pytest . --cov=src