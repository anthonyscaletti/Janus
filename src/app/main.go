package main

import (
	//resthandler "handler/rest"
	januscontroller "controller"
)

func main() {
	initializeJanus()
}

//Janus Initialization
func initializeJanus() {
	//Initialize REST Handler
	//resthandler.LaunchRestHandler()

	januscontroller.LaunchJanusEngine()
}
