package rest

import (
	"net/http"
)

//PostDataHandler : Handle Incoming Data To Be Predicted
type PostDataHandler struct {
}

func (postDataHandler *PostDataHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Post Data Handler"))
}
