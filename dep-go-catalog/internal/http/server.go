package http

import (
	"net/http"
)

func Serve(addr string, h http.Handler) error {
	return http.ListenAndServe(addr, h)
}
