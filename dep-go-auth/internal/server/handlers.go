package server

import (
	"db-go-auth/internal/repo"
	"encoding/json"
	"fmt"
	"net/http"
)

func (s *server) UserAdd(w http.ResponseWriter, r *http.Request) {
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

	// if len([]rune(request.Password)) < 8 {
	// 	error := fmt.Sprintf("{\"error\":\"%s\"}", "Password must be at least 8 characters long")
	// 	http.Error(w, error, http.StatusBadRequest)
	// 	return
	// }

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

func (s *server) UserGetAll(w http.ResponseWriter, r *http.Request) {
	users, err := s.userRepo.GetAll()
	if err != nil {
		error := fmt.Sprintf("{\"error\":\"%s\"}", err.Error())
		http.Error(w, error, http.StatusInternalServerError)
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(users)
}

func (s *server) LoginUser(w http.ResponseWriter, r *http.Request) {
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
		http.Error(w, "{\"error\":\"Invalid login or password\"}", http.StatusUnauthorized)
		return
	}

	var result struct{
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
