package handlers

import (
	"dep-go-catalog/internal/services"
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
		encode(w,http.StatusMethodNotAllowed,&errorJSON{Error: err.Error()})
	case ErrInvalidData:
		encode(w,http.StatusBadRequest,&errorJSON{Error: err.Error()})
	case services.ErrNotFound:
		encode(w,http.StatusNotFound,&errorJSON{Error: err.Error()})
	case services.ErrInvalidInput:
		encode(w,http.StatusBadRequest,&errorJSON{Error: err.Error()})
	case services.ErrConflict:
		encode(w,http.StatusConflict,&errorJSON{Error: err.Error()})
	default:
		encode(w,http.StatusInternalServerError,&errorJSON{Error: fmt.Sprintf("Internal server error: %s", err.Error())})
	}
}
