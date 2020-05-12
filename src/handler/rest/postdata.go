package rest

import (
	"encoding/json"
	"entity"
	"fmt"
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

	//TODO: Send Data To ML Model
	response := usecase.LaunchJanus(&data)
	//TODO: Return Predicted Data as Response
	fmt.Fprintf(w, "Data: %+v", response)
}