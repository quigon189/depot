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
}

func StartServer(path, host, port, secretKey string) error {
	s := server{
		userRepo: repo.NewUserRepo(path),
	}

	s.auth.SecretKey = []byte(secretKey)

	mux := http.NewServeMux()

	mux.HandleFunc("/user/add", s.UserAdd)
	//mux.HandleFunc("/user/all", s.UserGetAll)
	mux.HandleFunc("/user/login", s.LoginUser)

	log.Printf("Starting server on port %s", port)
	return http.ListenAndServe(host+":"+port, s.logHendler(mux))
}
