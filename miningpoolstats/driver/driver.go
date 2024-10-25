package driver

import (
	"context"
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

func (d *DriverSession) GetCtx() context.Context {
	return d.dCtx
}

func (d *DriverSession) Next(node *cdp.Node) {
	chromedp.Run(d.dCtx,
		chromedp.MouseClickNode(node),
		chromedp.Sleep(time.Second*3),
	)
}

func (d *DriverSession) OpenCoinInNewTab(node *cdp.Node) (context.Context, func(), error) {
	err := chromedp.Run(
		d.dCtx,
		chromedp.QueryAfter(node.FullXPath(), func(ctx context.Context, eci runtime.ExecutionContextID, n ...*cdp.Node) error {
			return chromedp.MouseClickNode(node, chromedp.ButtonModifiers(input.ModifierCtrl, input.ModifierShift)).Do(ctx)
		}),
	)
	if err != nil {
		return nil, nil, err
	}

	targets, err := chromedp.Targets(d.dCtx)
	if err != nil {
		return nil, nil, err
	}

	target := targets[0]

	newTabCtx, newTabCancel := chromedp.NewContext(d.dCtx, chromedp.WithTargetID(target.TargetID))
	tabCtx, cancel := context.WithCancel(newTabCtx)
	closeTab := func() {
		cancel()
		newTabCancel()
	}

	return tabCtx, closeTab, nil
}

func (d *DriverSession) SetViewportAndScale(w, h int64, scale float64) chromedp.ActionFunc {
	return func(ctx context.Context) error {
		sw, sh := int64(float64(w)/scale), int64(float64(h)/scale)
		err := emulation.SetDeviceMetricsOverride(sw, sh, scale, false).WithScale(scale).Do(ctx)
		if err != nil {
			return err
		}

		return nil
	}
}
