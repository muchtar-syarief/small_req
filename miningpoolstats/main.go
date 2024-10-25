package main

import (
	"github.com/muchtar/miningpoolstats/crawl"
	"github.com/muchtar/miningpoolstats/driver"
	"github.com/muchtar/miningpoolstats/model"
)

func main() {
	w, err := Writer()
	if err != nil {
		panic(err)
	}

	item := model.CoinResult{}
	err = w.Write(item.Keys())
	if err != nil {
		panic(err)
	}
	w.Flush()

	driver := driver.NewDriver()
	defer driver.Cancel()

	c := crawl.NewCrawl(driver)

	results, err := c.Run()
	if err != nil {
		panic(err)
	}

	for result := range results {
		values := result.ValuesV2()
		for _, val := range values {
			w.Write(val)
			w.Flush()
		}
	}

}
