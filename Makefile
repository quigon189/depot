dev_start: #Старт окружения разработчика
	podman-compose up -d
	http :18080/user/add name=laa email=laa@gmail.com password=ghjgecr123
	xdg-open http://localhost:5000/login

dev_stop:
	podman-compose down
	podman image prune -f
