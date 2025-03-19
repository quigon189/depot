package server

import (
	"bytes"
	"db-repo/internal/repo"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"golang.org/x/crypto/bcrypt"
)
type MockRepo struct {} 

func (r *MockRepo) Close(drop bool) {}

func (r *MockRepo) Add(u *repo.User) (int, error) {
		return 1, nil
}

func (r *MockRepo) GetAll()([]repo.User, error) {
	return []repo.User{}, nil
}

func (r *MockRepo) GetByName (name string) (*repo.User, error) {
	passHash, _ := bcrypt.GenerateFromPassword([]byte("123123123"), 14)
	return &repo.User{Name: "test", PasswordHash: string(passHash)}, nil 
} 

func TestUserHandlers(t *testing.T) {
	user := struct {
		Name string `json:"name"`
		Email string `json:"email"`
		Password string `json:"password"`
	} {
		Name: "test",
		Email: "test@test.com",
		Password: "123123123",
	}
	var buf bytes.Buffer
	json.NewEncoder(&buf).Encode(user)

	s := server{ userRepo: &MockRepo{}}

	rec := httptest.NewRecorder()
	request := httptest.NewRequest(http.MethodPost, "http://localhost:8080/user/add", &buf)

	t.Logf("User: %+v", user)

	s.UserAdd(rec, request)

	resp := rec.Result()
	t.Log("httptest recoerd: ", rec)
	if resp.Status != "201 Created" {
		t.Errorf("Error: Bad status (201 Created) - %s", resp.Status)
	}

	rec = httptest.NewRecorder()
	request = httptest.NewRequest(http.MethodGet, "http://localhost:8080/user/add", nil)

	s.UserAdd(rec, request)
	
	resp = rec.Result()
	t.Log("httptest recoerd: ", rec)
	if resp.Status != "405 Method Not Allowed" {
		t.Errorf("Error: Bad status (405 Method Not Allowed) - %s", resp.Status)
	}

	json.NewEncoder(&buf).Encode(user)
	rec = httptest.NewRecorder()
	request = httptest.NewRequest(http.MethodPost, "http://localhost:8080/user/login", &buf)

	s.LoginUser(rec, request)
	
	resp = rec.Result()
	t.Log("httptest recoerd: ", rec)
	if resp.Status != "200 OK" {
		t.Errorf("Error: Bad status (200 OK) - %s", resp.Status)
	}
}
