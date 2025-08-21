package auth

import (
	"api-gateway-service/internal/handlers/submux"
	"net/http"
)

func SetupAuth(mux *submux.SubMux) {
	mux.HandleFunc("/login", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Login"))
	})
}
