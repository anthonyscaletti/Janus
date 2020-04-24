package main

import (
	resthandler "handler/rest"
)

func main() {
	initializeJanus()
}

//Janus Initialization
func initializeJanus() {
	//Initialize REST Handler
	resthandler.LaunchRestHandler()
}
