package usecase

import (
	"entity"
	"log"
)

//LaunchJanus : UseCase To Execute Janus Controller
func LaunchJanus(data *entity.Data) string {
	log.Println(data)

	return "I GOT IT"
}
