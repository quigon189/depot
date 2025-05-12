SERVICES ?= 
ENV ?= DEV

run: #Запуск сервисов (по условию в режиме DEV) 
	./run.sh $(ENV)

stop:
	podman-compose down

build:
ifeq ($(ENV), DEV)
	@echo "Сборка для окружения DEV"
	podman-compose build $(SERVICES)
	podman image prune -f
else
	@echo "Неизвесное окружение $(ENV)"
endif
