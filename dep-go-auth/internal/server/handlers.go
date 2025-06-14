package server

import (
	"db-go-auth/internal/repo"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/felixge/httpsnoop"
)

func (s *server) UserAdd(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json; charset=utf-8")
	if r.Method != http.MethodPost {
		error := fmt.Sprintf("{\"error\":\"%s\"}", "Invalid method")
		http.Error(w, error, http.StatusMethodNotAllowed)
		return
	}

	var request struct {
		Name     string `json:"name"`
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusBadRequest)
		return
	}

	user, err := repo.NewUser(
		request.Name,
		request.Email,
		request.Password,
	)

	if err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusBadRequest)
		return
	}

	if err = user.SetPassword(request.Password); err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", "Bad password")
		http.Error(w, error, http.StatusBadRequest)
		return
	}

	id, err := s.userRepo.Add(user)
	if err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusInternalServerError)
		return
	}

	user.ID = id

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

func (s *server) LoginUser(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json; charset=utf-8")
	if r.Method != http.MethodPost {
		error := fmt.Sprintf("{\"error\":\"%s\"}", "Invalid method")
		http.Error(w, error, http.StatusMethodNotAllowed)
		return
	}
	var request struct {
		Name     string `json:"name"`
		Password string `json:"password"`
	}

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusBadRequest)
		return
	}

	user, err := s.userRepo.GetByName(request.Name)
	if err != nil || !user.CheckPassword(request.Password) {
		http.Error(w, "{\"error\":\"Invalid login or password\"}", http.StatusBadRequest)
		return
	}

	var result struct {
		Token string `json:"token"`
	}

	result.Token, err = s.auth.GenerateToken(user)
	if err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusInternalServerError)
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(result)
}

func (s *server) logHendler(h http.Handler) http.Handler {
	fn := func(w http.ResponseWriter, r *http.Request) {
		m := httpsnoop.CaptureMetrics(h, w, r)

		log.Printf("Request: %s %s remoteAddr: %s StatusCode: %v", r.Method, r.URL, r.RemoteAddr, m.Code)
	}

	return http.HandlerFunc(fn)
}
