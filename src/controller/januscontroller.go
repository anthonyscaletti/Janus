package controller

import (
	"encoding/json"
	"entity"
	"log"
	"os/exec"
)

//ExecuteJanusEngine : Launching Janus Python Model
func ExecuteJanusEngine(data *entity.Data) entity.Data {
	response := entity.Data{}

	dataJSON, err := json.Marshal(data)
	if err != nil {
		log.Println("Error Encoding Data: ", err.Error())
		return response
	}

	cmd := exec.Command("python", "../controller/ai/janus-entry.py", string(dataJSON))

	out, err := cmd.Output()
	if err != nil {
		log.Println("Error Executing Janus: ", err.Error())
		return response
	}

	err = json.Unmarshal(out, &response)
	if err != nil {
		log.Println("Error Decoding Data: ", err.Error())
		return response
	}

	return response
}
