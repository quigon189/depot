SERVICES ?= 
ENV ?= DEV
VERSION ?= 1.0.0

REG_IP := $(strip $(shell hostname -I | awk "{print $1}"))

run: #Запуск сервисов (по условию в режиме DEV) 
	./scripts/run.sh $(ENV)

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
	podman build --force-rm --tag $(REG_IP):9000/go-auth:$(VERSION) ./dep-go-auth
	podman build --force-rm --tag $(REG_IP):9000/go-catalog:$(VERSION) ./dep-go-catalog
	podman build --force-rm --tag $(REG_IP):9000/flask-front:$(VERSION) ./dep-flask-front
	podman push $(REG_IP):9000/go-auth:$(VERSION)
	podman push $(REG_IP):9000/go-catalog:$(VERSION)
	podman push $(REG_IP):9000/flask-front:$(VERSION)

local-registry:
	@podman volume create registry-data
	@podman run -d --name local-registry -p 9000:5000 -v registry-data:/var/lib/registry --restart=always docker.io/library/registry:2

	@sed -i 's/^LOCAL_REGISTRY\s*=\s*.*/LOCAL_REGISTRY = $(REG_IP):9000/' project_config.mk

	@echo Добавьте репозиторий в файл /etc/containers/registries.conf
	@echo [[registry]]
	@echo location = $(REG_IP):9000
	@echo insecure = true
