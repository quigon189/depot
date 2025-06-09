SERVICES ?= 
ENV ?= DEV
LOCAL_REPO = 192.168.1.14:9000
VERSION ?= 1.0.0

run: #Запуск сервисов (по условию в режиме DEV) 
	./run.sh $(ENV)

stop:
	@podman-compose down > /dev/null
	@echo "Контейнеры удалены"

build:
ifeq ($(ENV), DEV)
	@echo "Сборка для окружения DEV"
	podman-compose build $(SERVICES)
	podman image prune -f
else
	@echo "Неизвесное окружение $(ENV)"
endif

deploy:
	podman build --force-rm --tag $(LOCAL_REPO)/go-auth:$(VERSION) ./dep-go-auth
	podman build --force-rm --tag $(LOCAL_REPO)/go-catalog:$(VERSION) ./dep-go-catalog
	podman build --force-rm --tag $(LOCAL_REPO)/flask-front:$(VERSION) ./dep-flask-front
	podman push $(LOCAL_REPO)/go-auth:$(VERSION)
	podman push $(LOCAL_REPO)/go-catalog:$(VERSION)
	podman push $(LOCAL_REPO)/flask-front:$(VERSION)

	
