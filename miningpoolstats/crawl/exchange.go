package crawl

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/cdproto/runtime"
	"github.com/chromedp/chromedp"
	"github.com/muchtar/miningpoolstats/model"
	"github.com/pdcgo/common_conf/pdc_common"
)

func getRowTableExchange(ctx context.Context) []*cdp.Node {
	tableRows := []*cdp.Node{}

	c, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	chromedp.Run(
		c,
		chromedp.WaitReady("#Market"),
		chromedp.Nodes("#Market tbody tr", &tableRows, chromedp.ByQueryAll),
	)

	return tableRows
}

func getColumnTableExchange(ctx context.Context, node *cdp.Node) []*cdp.Node {
	columns := []*cdp.Node{}

	c, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	chromedp.Run(
		c,
		chromedp.Nodes("td", &columns, chromedp.ByQueryAll, chromedp.FromNode(node)),
	)

	return columns
}

func getExchangeName(ctx context.Context, node *cdp.Node) string {
	linkExchange := []*cdp.Node{}
	link := ""

	c, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	chromedp.Run(
		c,
		chromedp.Nodes("a", &linkExchange, chromedp.ByQueryAll, chromedp.FromNode(node)),
	)

	for _, l := range linkExchange {
		href, _ := l.Attribute("href")
		link = href
		break
	}

	return link
}

func getPairExchange(ctx context.Context, index int) (string, string, error) {
	pairs := []string{}

	c, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	script := fmt.Sprintf(`[...document.querySelectorAll("#Market tbody tr")[%d].querySelectorAll("td")[2].querySelectorAll("div > div")].map((e) => e.innerText)`, index)
	chromedp.Run(
		c,
		chromedp.Evaluate(script, &pairs),
	)
	if len(pairs) == 0 {
		return "", "", errors.New("pairs not found")
	}

	if len(pairs) == 1 {
		return pairs[0], "", nil
	}

	return pairs[0], pairs[1], nil
}

func getExchangeVolume(ctx context.Context, ind int) string {
	volume := []string{}

	c, cancel := context.WithTimeout(ctx, time.Second*15)
	defer cancel()

	script := fmt.Sprintf(`[...document.querySelectorAll("#Market tbody tr")[%d].querySelectorAll("td")[3].querySelectorAll("span")].map((e) => e.innerText)`, ind)
	chromedp.Run(
		c,
		chromedp.Evaluate(script, &volume),
	)

	return volume[0]
}

func toExchange(ctx context.Context) {
	chromedp.Run(
		ctx,
		chromedp.WaitReady("#Market"),
		chromedp.ActionFunc(func(ctx context.Context) error {
			_, exp, err := runtime.Evaluate(`window.scrollTo(0,document.body.scrollHeight);`).Do(ctx)
			if err != nil {
				return err
			}
			if exp != nil {
				return exp
			}
			return nil
		}),
	)
}

func (c *Crawl) getExchange() <-chan *model.Exchange {
	exchangeChan := make(chan *model.Exchange, 100)

	wg := sync.WaitGroup{}

	wg.Add(1)
	go func() {
		defer func() {
			close(exchangeChan)
			wg.Done()
		}()

		tableRows := getRowTableExchange(c.tabCtx)

		if len(tableRows) == 0 {
			err := errors.New("table exchange market not found")
			pdc_common.ReportError(err)
			return
		}

		for ind, tableRow := range tableRows {

			columns := getColumnTableExchange(c.tabCtx, tableRow)
			if len(columns) != 4 {
				break
			}

			exchangeNameRow := columns[1]

			name := getExchangeName(c.tabCtx, exchangeNameRow)

			pairName, price, err := getPairExchange(c.tabCtx, ind)
			if err != nil {
				pdc_common.ReportError(err)
				return
			}

			volume := getExchangeVolume(c.tabCtx, ind)

			exchange := &model.Exchange{
				ExchangeName:   name,
				ExchangePair:   pairName,
				MarketPrice:    price,
				ExchangeVolume: volume,
			}

			exchangeChan <- exchange
		}

		// nexts := []*cdp.Node{}
		// chromedp.Run(
		// 	c.tabCtx,
		// 	chromedp.Nodes("#Market_next", &nexts, chromedp.ByQueryAll),
		// )

		// for _, next := range nexts {
		// 	class, _ := next.Attribute("class")
		// 	if !strings.Contains(class, "disabled") {
		// 		chromedp.Run(
		// 			c.tabCtx,
		// 			chromedp.MouseClickNode(next),
		// 			chromedp.Sleep(time.Second*3),
		// 		)
		// 		resps := c.getExchange()
		// 		for resp := range resps {
		// 			exchangeChan <- resp
		// 		}
		// 	}
		// }

	}()

	wg.Wait()

	return exchangeChan
}

func (c *Crawl) GetExchange() (<-chan *model.Exchange, error) {
	toExchange(c.tabCtx)

	return c.getExchange(), nil
}
