package main

import (
	"fmt"
	resthandler "handler/rest"
)

func main() {
	fmt.Println("Janus Initialization")

	resthandler.LaunchRestHandler()
}
