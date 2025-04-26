package http

import (
	"net/http"
)

func Serve(addr string, h http.Handler) error {
	h = loggingMiddlware(jsonMiddleware(h))
	return http.ListenAndServe(addr, h)
}
