package server

import (
	"db-go-auth/internal/auth"
	"db-go-auth/internal/repo"
	"log"
	"net/http"
)

type server struct {
	userRepo repo.Repo
	auth     auth.Auth
	config   struct {
		port      string
	}
}

func StartServer(path, port, secretKey string) error {
	s := server{
		userRepo: repo.NewUserRepo(path),
	}
	s.config.port = port

	s.auth.SecretKey = []byte(secretKey)

	http.HandleFunc("/user/add", s.UserAdd)
	//http.HandleFunc("/user/all", s.UserGetAll)
	http.HandleFunc("/user/login", s.LoginUser)

	log.Printf("Starting server on port %s", s.config.port)
	return http.ListenAndServe(":"+s.config.port, nil)
}
