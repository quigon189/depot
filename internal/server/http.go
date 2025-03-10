package server

import (
	"db-repo/internal/repo"
	"log"
	"net/http"
)

type server struct{
	r *repo.Repo
}

func StartServer(path string) error {
	s := server{}
	s.r = repo.NewRepo(path) 

	http.HandleFunc("/user/add", s.UserAdd)

	log.Println("Starting server on port 8080")
	return http.ListenAndServe(":8080", nil) 
}
