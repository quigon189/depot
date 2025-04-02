ADDR := $(shell hostname -I | tr -d " ")

dev-start: #Старт окружения разработчика
	podman-compose up -d
	http :18080/add name=laa email=laa@gmail.com password=ghjgecr123
	@echo "http://$(ADDR):5000"

dev-stop:
	podman-compose down
	podman image prune -f

dev-update:
	podman rmi localhost/depot_flask-front:latest localhost/depot_go-auth:latest || true
	podman-compose build
