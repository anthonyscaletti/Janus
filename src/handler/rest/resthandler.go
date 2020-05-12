package rest

import (
	"fmt"
	"log"
	"net/http"
	"os"
)

//LaunchRestHandler : REST Handler Initialization
func LaunchRestHandler() {
	const defaultPort string = "5000"
	router := http.NewServeMux()

	//Post Data Handler
	postDataHandler := &PostDataHandler{}

	//Routes
	router.Handle("/", entryHandler("/"))
	router.Handle("/entry/", entryHandler("/entry/"))
	router.Handle("/api/janus/post/", postDataHandler)

	//Server
	port := os.Getenv("PORT")

	if port == "" {
		port = defaultPort
	}

	log.Println(fmt.Sprintf("Listening at port: %v", port))
	http.ListenAndServe(fmt.Sprintf(":%v", port), router)
}

//API Entry Page
func entryHandler(prefix string) http.Handler {
	fs := http.StripPrefix(prefix, http.FileServer(http.Dir("../static"))) //DEV PATH

	return fs
}
