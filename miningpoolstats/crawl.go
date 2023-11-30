package main

import (
	"context"
	"log"
	"strings"
	"sync/atomic"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/chromedp"
)

type Crawl struct {
	Driver *DriverSession
}

func NewCrawl(d *DriverSession) *Crawl {
	return &Crawl{
		Driver: d,
	}
}

func (c *Crawl) Run() (<-chan *CoinResult, error) {
	chromedp.Run(
		c.Driver.dCtx,
		chromedp.Navigate(c.Driver.Url),
	)

	return c.process()
}

func (c *Crawl) process() (<-chan *CoinResult, error) {
	coinChan := make(chan *CoinResult, 100)

	go func() {
		defer close(coinChan)

		coinElements := []*cdp.Node{}
		algorithms := []string{}
		chromedp.Run(
			c.Driver.dCtx,
			chromedp.WaitVisible(".homeurl"),
			chromedp.Nodes(".homeurl", &coinElements, chromedp.ByQueryAll),
			chromedp.Evaluate(`[...document.querySelectorAll("tbody > tr[role='row'] > td:nth-child(3) > div")].map((e) => e.innerText)`, &algorithms),
		)

		for i, coinElement := range coinElements {
			atomic.AddInt32(&c.Driver.counter, 1)

			coin := []*cdp.Node{}
			link := []*cdp.Node{}
			chromedp.Run(
				c.Driver.dCtx,
				chromedp.Nodes(".homeicon", &link, chromedp.ByQueryAll, chromedp.FromNode(coinElement)),
				chromedp.Nodes("b", &coin, chromedp.ByQueryAll, chromedp.FromNode(coinElement)),
			)

			name := coin[0].Children[0].NodeValue
			algorithm := algorithms[i]
			item := CoinResult{
				Name:      name,
				Algorithm: algorithm,
			}

			err := c.Driver.OpenCoin(link[0], &item)
			if err != nil {
				coinChan <- &item
				if err != context.Canceled {
					if i != len(coinElements) {
						continue
					}
				}
			}

			coinChan <- &item

			log.Printf("[ Process %d ] %s %s %s", c.Driver.counter, name, algorithm, item.CoinUrl)

			time.Sleep(time.Second)
		}

		tCtx, cancel := context.WithTimeout(c.Driver.dCtx, time.Second*5)
		defer cancel()

		nexts := []*cdp.Node{}
		chromedp.Run(
			tCtx,
			chromedp.Nodes("#coins_next", &nexts, chromedp.ByQueryAll),
		)

		for _, next := range nexts {
			class, _ := next.Attribute("class")
			log.Println(class)
			if !strings.Contains(class, "disabled") {
				c.Driver.next(next)
				resps, err := c.process()
				if err != nil {
					log.Println(err)
					return
				}
				for resp := range resps {
					coinChan <- resp
				}
			}
		}

	}()

	return coinChan, nil
}
