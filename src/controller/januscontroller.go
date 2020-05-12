package controller

import (
	"fmt"
	"os/exec"
)

//LaunchJanusEngine : Launching Janus Python Model
func LaunchJanusEngine() {
	cmd := exec.Command("python", "../controller/ai/janus-entry.py", "Test")
	out, err := cmd.Output()

	if err != nil {
		println(err.Error())
		return
	}

	fmt.Println(string(out))
}
