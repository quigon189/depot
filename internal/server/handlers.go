package server

import (
	"db-repo/internal/repo"
	"encoding/json"
	"net/http"
)

func (s *server) UserAdd(w http.ResponseWriter, r *http.Request) {
	var request struct {
		Name     string `json:"name"`
		Email    string `json:"email"`
		Password string `json:"password"`
	}

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	user := repo.User{
		Name:  request.Name,
		Email: request.Email,
	}

	if err := user.SetPassword(request.Password); err != nil {
		http.Error(w, "Bad password", http.StatusBadRequest)
		return
	}

	id, err := s.r.UserAdd(&user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	user.ID = id

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}
