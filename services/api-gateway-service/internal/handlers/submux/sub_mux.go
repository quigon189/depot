package submux

import "net/http"

type SubMux struct {
	parent *http.ServeMux
	prefix string
}

func New(parent *http.ServeMux, prefix string) *SubMux {
	return &SubMux{
		parent: parent,
		prefix: prefix,
	}
}

func (mux *SubMux) HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request)) {
	mux.parent.HandleFunc(mux.prefix+pattern, handler)
}
