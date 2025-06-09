#! /bin/bash

case $1 in
	"DEV")
		echo "Запускаем сервисы в DEV режиме"
		echo "Используем podman-compose"

		mkdir logs 2> /dev/null

		echo "---------------------" >> ./logs/flask-front.log
		echo "---------------------" >> ./logs/go-auth.log
		echo "---------------------" >> ./logs/go-catalog.log
		
		podman-compose up -d >> ./logs/start.log
		sleep 10
		http :18080/add name=admin email=admin@depot.local password=password >> ./logs/start.log
		
		./dep-go-catalog/test/test.sh 18081 >> ./logs/start.log

		ADDR=$(hostname -I | awk '{print $1}')

		echo "Depot server: http://$ADDR:5000"
		echo "dep-go-auth: http://$ADDR:18080"
		echo "dep-go-catalog: http://$ADDR:18081"
		;;
	*)
		echo "Доступен только режим DEV"
		;;
esac
