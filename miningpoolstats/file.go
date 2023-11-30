package main

import (
	"encoding/csv"
	"os"
)

func Writer() (*csv.Writer, error) {
	f, err := os.OpenFile("coins.csv", os.O_RDWR|os.O_CREATE, os.ModePerm)
	if err != nil {
		return nil, err
	}

	return csv.NewWriter(f), nil
}
