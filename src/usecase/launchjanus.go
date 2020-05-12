package usecase

import (
	januscontroller "controller"
	"entity"
)

//LaunchJanus : UseCase To Execute Janus Controller
func LaunchJanus(data *entity.Data) entity.Data {
	result := januscontroller.ExecuteJanusEngine(data)

	return result
}
