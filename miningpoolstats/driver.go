package main

import (
	"context"
	"log"
	"sync"
	"time"

	"github.com/chromedp/cdproto/cdp"
	"github.com/chromedp/cdproto/emulation"
	"github.com/chromedp/cdproto/input"
	"github.com/chromedp/cdproto/runtime"
	"github.com/chromedp/chromedp"
)

type DriverSession struct {
	Url    string
	dCtx   context.Context
	Cancel func()

	guard   sync.WaitGroup
	limit   chan int64
	counter int32
}

func NewDriver() *DriverSession {
	baseUri := "https://miningpoolstats.stream/"

	opts := append(chromedp.DefaultExecAllocatorOptions[:],
		chromedp.Flag("headless", false),
		chromedp.Flag("disable-gpu", false),
		chromedp.Flag("enable-automation", false),
		chromedp.Flag("disable-extensions", false),
		chromedp.Flag("detach", true),
		chromedp.Flag("start-maximize", true),
	)

	allocatorContext, cancelAloc := chromedp.NewExecAllocator(context.Background(), opts...)

	ctx, cancel := chromedp.NewContext(allocatorContext)

	return &DriverSession{
		Url:  baseUri,
		dCtx: ctx,
		Cancel: func() {
			cancel()
			cancelAloc()
		},
		guard:   sync.WaitGroup{},
		limit:   make(chan int64, 3),
		counter: 0,
	}
}

func (d *DriverSession) next(node *cdp.Node) {
	chromedp.Run(d.dCtx,
		chromedp.MouseClickNode(node),
		chromedp.Sleep(time.Second*3),
	)
}

func (d *DriverSession) OpenCoin(node *cdp.Node, hasil *CoinResult) error {

	err := chromedp.Run(
		d.dCtx,
		chromedp.QueryAfter(node.FullXPath(), func(ctx context.Context, eci runtime.ExecutionContextID, n ...*cdp.Node) error {
			return chromedp.MouseClickNode(node, chromedp.ButtonModifiers(input.ModifierCtrl, input.ModifierShift)).Do(ctx)
		}),
	)
	if err != nil {
		return err
	}

	targets, err := chromedp.Targets(d.dCtx)
	if err != nil {
		return err
	}

	githubs := []*cdp.Node{}

	target := targets[0]

	newTabCtx, newTabCancel := chromedp.NewContext(d.dCtx, chromedp.WithTargetID(target.TargetID))
	timeOutCtx, cancel := context.WithTimeout(newTabCtx, time.Second*15)
	defer func() {
		cancel()
		newTabCancel()

	}()

	stat := Stat{}

	err = chromedp.Run(
		timeOutCtx,
		setViewportAndScale(2560, 1423, 0.75),
		chromedp.WaitVisible("#mainpage"),
		chromedp.WaitVisible("#myAlgo"),
		chromedp.WaitVisible("#stats_marketcap"),
		chromedp.WaitVisible("#stats_volume"),
		chromedp.WaitVisible("#stats_supply_circulating"),
		chromedp.WaitVisible("#stats_supply_emission"),
		chromedp.WaitVisible("#poolsminers"),
		chromedp.Evaluate(`document.querySelectorAll("#myAlgo")[0].innerText`, &hasil.AlgorithmType),
		chromedp.Evaluate(`document.querySelectorAll("#poolsminers")[0].innerText`, &hasil.Miners),
		chromedp.Evaluate(`document.querySelectorAll("#stats_marketcap")[0].innerText`, &stat.MarketCap),
		chromedp.Evaluate(`document.querySelectorAll("#stats_volume")[0].innerText`, &stat.Volume),
		chromedp.Evaluate(`document.querySelectorAll("#stats_supply_circulating")[0].innerText`, &stat.CirculatingSupply),
		chromedp.Evaluate(`document.querySelectorAll("#stats_supply_emission")[0].innerText`, &stat.Emission),
		chromedp.WaitVisible("#zona_market"),
		chromedp.Sleep(time.Second),
		chromedp.Location(&hasil.CoinUrl),
		chromedp.WaitVisible("#source_name"),
		chromedp.Nodes("#source_name", &githubs, chromedp.ByQueryAll),
	)
	if err != nil {
		log.Println("[ Zona Market ] ", err)
		return err
	}

	tCtx, cancel := context.WithTimeout(newTabCtx, time.Second*8)
	defer cancel()

	depends := []*cdp.Node{}

	for _, github := range githubs {
		parent := github.Parent
		link, _ := parent.Attribute("href")
		hasil.GithubLink = link
		chromedp.Run(
			tCtx,
			chromedp.Navigate(link),
			chromedp.WaitVisible("#repository-container-header"),
			chromedp.Nodes("a[title='depends']", &depends, chromedp.ByQueryAll),
		)
	}

	hasil.IsDepends = len(depends) != 0
	hasil.Stat = stat
	return nil
}

func setViewportAndScale(w, h int64, scale float64) chromedp.ActionFunc {
	return func(ctx context.Context) error {
		sw, sh := int64(float64(w)/scale), int64(float64(h)/scale)
		err := emulation.SetDeviceMetricsOverride(sw, sh, scale, false).WithScale(scale).Do(ctx)
		if err != nil {
			return err
		}

		return nil
	}
}
