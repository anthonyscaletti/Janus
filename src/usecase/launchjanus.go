package usecase

import (
	januscontroller "controller"
	"entity"
	"log"
)

//LaunchJanus : UseCase To Execute Janus Controller
func LaunchJanus(data *entity.Data) string {
	log.Println(data)

	januscontroller.ExecuteJanusEngine(data)

	return "I GOT IT"
}
