package controller

import (
	"encoding/json"
	"entity"
	"fmt"
	"log"
	"os/exec"
)

//ExecuteJanusEngine : Launching Janus Python Model
func ExecuteJanusEngine(data *entity.Data) {

	dataJSON, err := json.Marshal(data)
	if err != nil {
		log.Println("Error Encoding Data", err)
		return
	}

	cmd := exec.Command("python", "../controller/ai/janus-entry.py", string(dataJSON))
	out, err := cmd.Output()

	if err != nil {
		println(err.Error())
		return
	}

	fmt.Println(string(out))
}
