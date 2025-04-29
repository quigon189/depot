ADDR := $(shell hostname -I | tr -d " ")

dev-start: #Старт окружения разработчика
	podman-compose up -d
	podman image prune -f
	sleep 10
	http :18080/add name=laa email=laa@gmail.com password=ghjgecr123
	./dep-go-catalog/test/test.sh 18081
	@echo "Depot server: http://$(ADDR):5000"
	@echo "dep-go-auth: http://$(ADDR):18080"
	@echo "dep-go-catalog: http://$(ADDR):18081"

dev-stop:
	podman-compose down

dev-update:
	podman rmi localhost/depot_flask-front:latest localhost/depot_go-auth:latest localhost/depot_go-catalog:latest || true
	podman-compose build
