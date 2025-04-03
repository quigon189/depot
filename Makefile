ADDR := $(shell hostname -I | tr -d " ")

dev-start: #Старт окружения разработчика
	podman-compose up -d
	podman image prune -f
	sleep 10
	http :18080/add name=laa email=laa@gmail.com password=ghjgecr123
	@echo "http://$(ADDR):5000"

dev-stop:
	podman-compose down

dev-update:
	podman rmi localhost/depot_flask-front:latest localhost/depot_go-auth:latest || true
	podman-compose build
