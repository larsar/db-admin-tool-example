admin_db_user=postgres

psql:
	docker-compose run db psql -h db -U postgres

ps:
	docker-compose ps

up:
	docker-compose up -d

down:
	docker-compose down

schema:
	docker-compose run --rm db pg_dump -s --no-owner -h db -U ${admin_db_user}

migrate:
	docker-compose run --rm db bash -c 'cat db/schema/* | psql -h db -U ${admin_db_user}'

seed:
	docker-compose run --rm db bash -c 'cat db/seed/* | psql -h db -U ${admin_db_user}'

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose restart

logs:
	docker-compose logs -f

reset: _reset migrate seed

run:
	docker-compose run --rm admin local

_reset:
	docker-compose down &&\
	docker-compose up -d &&\
	sleep 5
