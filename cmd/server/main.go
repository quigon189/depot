package main

import (
	"db-repo/internal/server"
	"log"
)

func main() {
	log.Fatal(server.StartServer("app.db"))
}
