package rest

import (
	"encoding/json"
	"entity"
	"fmt"
	"log"
	"net/http"
	"usecase"
)

//PostDataHandler : Handle Incoming Data To Be Predicted
type PostDataHandler struct {
}

func (postDataHandler *PostDataHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		fmt.Fprintf(w, "**Must be a POST request**")
		return
	}

	var data entity.Data

	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	//Send Data To Janus Engine
	response := usecase.LaunchJanus(&data)

	//Return Predicted Data as Response
	dataJSON, err := json.Marshal(response)
	if err != nil {
		log.Println("Error Decoding Data: ", err.Error())
		return
	}

	fmt.Fprintf(w, string(dataJSON))
}
