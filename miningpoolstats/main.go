package main

import (
	"log"
)

func main() {
	w, err := Writer()
	if err != nil {
		log.Println(err)
		panic(err)
	}

	item := CoinResult{}
	err = w.Write(item.Keys())
	if err != nil {
		log.Println(err)
		panic(err)
	}
	w.Flush()

	driver := NewDriver()
	defer driver.Cancel()

	c := NewCrawl(driver)

	results, err := c.Run()
	if err != nil {
		log.Println(err)
		panic(err)
	}

	for result := range results {
		w.Write(result.Values())
		w.Flush()
	}

	// for res := range results {
	// 	w.Write(res.ToCsv())
	// 	w.Flush()
	// }

}
