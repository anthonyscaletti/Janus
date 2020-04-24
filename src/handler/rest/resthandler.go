package resthandler

import (
	"fmt"
	"net/http"
)

//LaunchRestHandler : REST Handler Initialization
func LaunchRestHandler() {
	mux := http.NewServeMux()

	mux.HandleFunc("/", EntryHandler)

	fmt.Println("Listening...")
	http.ListenAndServe(":5000", mux)
}

//EntryHandler : API Entry Page
func EntryHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "API Entry Page")
}
