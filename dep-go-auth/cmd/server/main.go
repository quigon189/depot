package main

import (
	"db-go-auth/internal/server"
	"log"
	"os"
)

func main() {
	var port, secretKey string
	if val, ok := os.LookupEnv("SECRET_KEY"); !ok {
		log.Fatal("Env SECRET_KEY reqired")
	} else {
		secretKey = val
	}

	if val, ok := os.LookupEnv("DB_PORT"); ok {
		port = val
	} else {
		port = "8080"
	}

	log.Fatal(server.StartServer(
		"app.db",
		port,
		secretKey,
	))
}
