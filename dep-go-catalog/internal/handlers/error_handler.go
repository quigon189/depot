package handlers

import (
	"dep-go-catalog/internal/services"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
)

var (
	ErrInvalidData     = errors.New("invalid data")
	ErrMetodNotAllowed = errors.New("metod not allowed")
)

func handleError(w http.ResponseWriter, err error) {
	type errorJSON struct {
		Error string `json:"error"`
	}
	switch err {
	case ErrMetodNotAllowed:
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(&errorJSON{Error: err.Error()})
	case ErrInvalidData:
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(&errorJSON{Error: err.Error()})
	case services.ErrNotFound:
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(&errorJSON{Error: err.Error()})
	case services.ErrInvalidInput:
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(&errorJSON{Error: err.Error()})
	case services.ErrConflict:
		w.WriteHeader(http.StatusConflict)
		json.NewEncoder(w).Encode(&errorJSON{Error: err.Error()})
	default:
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(&errorJSON{Error: fmt.Sprintf("Internal server error: %s", err.Error())})
	}
}
