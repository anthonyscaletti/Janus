package entity

//Data : Data Entity Used in Request and Response
type Data struct {
	X        []string  `json:"x"`
	Y        []float64 `json:"y"`
	DayCount int       `json:"dayCount"`
}
