ADDR := $(shell hostname -I | tr -d " ")

dev_start: #Старт окружения разработчика
	podman-compose up -d
	http :18080/user/add name=laa email=laa@gmail.com password=ghjgecr123
	@echo "http://$(ADDR):5000"

dev_stop:
	podman-compose down
	podman image prune -f
