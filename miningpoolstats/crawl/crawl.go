package crawl

import (
	"context"
	"errors"
	"log"
	"strings"
	"sync/atomic"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/chromedp"
	"github.com/muchtar/miningpoolstats/driver"
	"github.com/muchtar/miningpoolstats/model"
	"github.com/pdcgo/common_conf/pdc_common"
)

type Crawl struct {
	Driver *driver.DriverSession

	tabCtx    context.Context
	cancelTab func()
}

func NewCrawl(d *driver.DriverSession) *Crawl {
	return &Crawl{
		Driver: d,
	}
}

func (c *Crawl) OpenMiningpoolStats() error {
	ctx := c.Driver.GetCtx()

	return chromedp.Run(
		ctx,
		chromedp.Navigate(c.Driver.Url),
	)
}

func (c *Crawl) Run() (<-chan *model.CoinResult, error) {

	c.OpenMiningpoolStats()

	return c.process()
}

func coinsElements(ctx context.Context) ([]*cdp.Node, error) {
	coinElements := []*cdp.Node{}
	err := chromedp.Run(
		ctx,
		chromedp.WaitVisible(".homeurl"),
		chromedp.Nodes(".homeurl", &coinElements, chromedp.ByQueryAll),
	)

	return coinElements, err
}

func getAlgo(ctx context.Context) string {
	algo := []string{}

	script := `[...document.querySelectorAll("#myAlgo")].map((e) => e.innerText)`
	chromedp.Run(
		ctx,
		chromedp.WaitReady("#myAlgo"),
		chromedp.Evaluate(script, &algo),
	)

	if len(algo) == 0 {
		return ""
	}

	return algo[0]
}

func getGithubs(ctx context.Context) ([]*cdp.Node, error) {
	githubs := []*cdp.Node{}
	err := chromedp.Run(
		ctx,
		chromedp.Nodes("#source_name", &githubs, chromedp.ByQueryAll),
	)

	return githubs, err
}

func githubData(ctx context.Context, githubs []*cdp.Node) (string, bool, error) {

	tCtx, cancel := context.WithTimeout(ctx, time.Second*8)
	defer cancel()

	githubLink := ""

	depends := []*cdp.Node{}
	for _, github := range githubs {
		parent := github.Parent
		link, _ := parent.Attribute("href")
		githubLink = link
		err := chromedp.Run(
			tCtx,
			chromedp.Navigate(link),
			chromedp.WaitVisible("#repository-container-header"),
			chromedp.Nodes("a[title='depends']", &depends, chromedp.ByQueryAll),
		)
		if err != nil {
			return "", false, err
		}
	}

	isDepend := len(depends) != 0

	return githubLink, isDepend, nil
}

func (c *Crawl) GetStatsCoin(hasil *model.CoinResult) (*model.Stat, error) {
	ctx, cancel := context.WithTimeout(c.tabCtx, time.Second*15)
	defer cancel()

	stat := model.Stat{}
	err := chromedp.Run(
		ctx,
		c.Driver.SetViewportAndScale(1920, 1080, 0.75),
		chromedp.WaitVisible("#mainpage"),
		chromedp.WaitVisible("#myAlgo"),
		chromedp.WaitVisible("#stats_marketcap"),
		chromedp.WaitVisible("#stats_volume"),
		chromedp.WaitVisible("#stats_supply_circulating"),
		chromedp.WaitVisible("#stats_supply_emission"),
		chromedp.WaitVisible("#poolsminers"),
		chromedp.Evaluate(`document.querySelectorAll("#myAlgo")[0].innerText`, &hasil.AlgorithmType),
		chromedp.Evaluate(`document.querySelectorAll("#poolsminers")[0].innerText`, &hasil.Miners),
		chromedp.Evaluate(`document.querySelectorAll("#logo_page")[0].getAttribute("alt")`, &hasil.Name),
		chromedp.Evaluate(`document.querySelectorAll("#stats_marketcap")[0].innerText`, &stat.MarketCap),
		chromedp.Evaluate(`document.querySelectorAll("#stats_volume")[0].innerText`, &stat.Volume),
		chromedp.Evaluate(`document.querySelectorAll("#stats_supply_circulating")[0].innerText`, &stat.CirculatingSupply),
		chromedp.Evaluate(`document.querySelectorAll("#stats_supply_emission")[0].innerText`, &stat.Emission),
		chromedp.WaitVisible("#zona_market"),
		chromedp.Sleep(time.Second),
		chromedp.Location(&hasil.CoinUrl),
		chromedp.WaitVisible("#source_name"),
	)

	return &stat, err
}

func (c *Crawl) GetCoinData(node *cdp.Node) (*model.CoinResult, error) {
	hasil := &model.CoinResult{}
	tabCtx, close, err := c.Driver.OpenCoinInNewTab(node)
	if err != nil {
		return nil, err
	}
	c.tabCtx = tabCtx
	c.cancelTab = close

	defer c.cancelTab()

	algo := getAlgo(tabCtx)
	hasil.Algorithm = algo

	stats, err := c.GetStatsCoin(hasil)
	if err != nil {
		return nil, err
	}
	hasil.Stat = *stats

	exchanges, err := c.GetExchange()
	if err != nil {
		return nil, err
	}

	for exchange := range exchanges {
		hasil.Exchanges = append(hasil.Exchanges, exchange)
	}

	githubs, err := getGithubs(tabCtx)
	if err != nil {
		return nil, err
	}

	link, isDepend, err := githubData(tabCtx, githubs)
	if err != nil {
		return nil, err
	}
	hasil.IsDepends = isDepend
	hasil.GithubLink = link

	return hasil, nil
}

func (c *Crawl) GetCoinLinkNode(node *cdp.Node) (*cdp.Node, error) {
	link := []*cdp.Node{}

	ctx := c.Driver.GetCtx()
	chromedp.Run(
		ctx,
		chromedp.Nodes("a", &link, chromedp.ByQueryAll, chromedp.FromNode(node)),
	)

	if len(link) == 0 {
		return nil, errors.New("link coin not found")
	}

	return link[0], nil
}

func getCoinName(ctx context.Context, node *cdp.Node) (string, error) {
	// names := []string{}

	coin := []*cdp.Node{}

	// script := fmt.Sprintf(`[...document.querySelectorAll(".homeurl")[%d].querySelectorAll("b")].map((e) => e.innerText)`, ind)
	chromedp.Run(
		ctx,
		chromedp.Nodes("b", &coin, chromedp.ByQueryAll, chromedp.FromNode(node)),
		// chromedp.Evaluate(script, &names),
	)

	if len(coin) == 0 {
		return "", errors.New("coin name not found")
	}

	return coin[0].Children[0].NodeValue, nil
}

func (c *Crawl) process() (<-chan *model.CoinResult, error) {
	coinChan := make(chan *model.CoinResult, 100)

	go func() {
		defer close(coinChan)

		ctx := c.Driver.GetCtx()
		coinElements, err := coinsElements(ctx)
		if err != nil {
			pdc_common.ReportError(err)
			return
		}

		counter := int32(0)
		for i, coinElement := range coinElements {
			atomic.AddInt32(&counter, 1)

			// name, err := getCoinName(ctx, coinElement)
			// if err != nil {
			// 	pdc_common.ReportError(err)
			// 	continue
			// }

			coin := []*cdp.Node{}
			link := []*cdp.Node{}
			chromedp.Run(
				ctx,
				chromedp.Nodes(".homeicon", &link, chromedp.ByQueryAll, chromedp.FromNode(coinElement)),
				chromedp.Nodes("b", &coin, chromedp.ByQueryAll, chromedp.FromNode(coinElement)),
			)

			name := coin[0].Children[0].NodeValue

			item, err := c.GetCoinData(link[0])
			if err != nil {
				coinChan <- item
				if err != context.Canceled {
					if i != len(coinElements) {
						continue
					}
				}
			}
			item.Name = name
			log.Printf("[ Process %d ] %s", counter, item.Name)

			coinChan <- item

			time.Sleep(time.Second)
		}

		tCtx, cancel := context.WithTimeout(ctx, time.Second*5)
		defer cancel()

		nexts := []*cdp.Node{}
		chromedp.Run(
			tCtx,
			chromedp.Nodes("#coins_next", &nexts, chromedp.ByQueryAll),
		)

		for _, next := range nexts {
			class, _ := next.Attribute("class")
			if !strings.Contains(class, "disabled") {
				c.Driver.Next(next)
				resps, err := c.process()
				if err != nil {
					pdc_common.ReportError(err)
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
