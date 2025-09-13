package server

import (
	"db-go-auth/internal/auth"
	"db-go-auth/internal/config"
	"db-go-auth/internal/repo"
	"fmt"
	"log"
	"net/http"
)

type server struct {
	userRepo repo.Repo
	auth     auth.Auth
}

func StartServer(cfg *config.Config) error {
	var s server
	switch cfg.DB.Type {
	case "postgres":
		s = server{
			userRepo: repo.NewPostgreSQLRepo(
				fmt.Sprintf(
					"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
					cfg.DB.Postgres.Host,
					cfg.DB.Postgres.Port,
					cfg.DB.Postgres.User,
					cfg.DB.Postgres.Password,
					cfg.DB.Postgres.DBname,
					cfg.DB.Postgres.SSLmode,
				)),
		}

	case "sqlite":
		s = server{
			userRepo: repo.NewSqliteRepo(cfg.DB.SQLite.Path),
		}
	default:
		log.Fatal("Error config file: Type db must be 'postgres' or 'sqlite'")
	}

	s.auth.SecretKey = []byte(cfg.Server.Secret)

	mux := http.NewServeMux()

	mux.HandleFunc("/add", s.UserAdd)
	mux.HandleFunc("/login", s.LoginUser)

	log.Printf("Starting server %s:%s", cfg.Server.Host, cfg.Server.Port)
	return http.ListenAndServe(cfg.Server.Host+":"+cfg.Server.Port, s.logHendler(mux))
}
