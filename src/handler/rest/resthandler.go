package resthandler

import (
	"fmt"
	"net/http"
)

//LaunchRestHandler : REST Handler Initialization
func LaunchRestHandler() {
	mux := http.NewServeMux()

	//Routes
	mux.Handle("/", entryHandler())
	mux.Handle("/entry", entryHandler())

	fmt.Println("Listening...")
	http.ListenAndServe(":5000", mux)
}

//API Entry Page
func entryHandler() http.Handler {
	fs := http.FileServer(http.Dir("../static"))

	return fs
}
