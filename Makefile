up:
	docker-compose up --build

down:
	docker-compose down

format:
	black app tests

lint:
	flake8 app

test:
	pytest

worker:
	docker-compose exec worker bash
