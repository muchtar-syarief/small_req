package model

import "strconv"

type Stat struct {
	MarketCap         string `csv:"market_cap"`         // #stats_marketcap
	Volume            string `csv:"volume"`             // #stats_volume
	CirculatingSupply string `csv:"circulating_supply"` // #stats_supply_circulating
	Emission          string `csv:"emission"`           // #stats_supply_emission
}

type Exchange struct {
	ExchangeName   string `csv:"exchange_name"`
	ExchangePair   string `csv:"exchange_pair"`
	MarketPrice    string `csv:"marke_price"`
	ExchangeVolume string `csv:"exchange_volume"`
}

func (e *Exchange) Values() []string {
	hasil := []string{
		e.ExchangeName,
		e.ExchangePair,
		e.MarketPrice,
		e.ExchangeVolume,
	}

	return hasil
}

type CoinResult struct {
	Name          string `csv:"name"`
	Algorithm     string `csv:"algorithm"`
	AlgorithmType string `csv:"algorithm_type"`
	IsDepends     bool   `csv:"is_depends"`
	CoinUrl       string `csv:"coin_url"`
	GithubLink    string `csv:"github_link"`
	Miners        string `csv:"miners"`
	Stat
	Exchanges []*Exchange
}

func (c *CoinResult) Keys() []string {
	res := []string{
		"name",
		"algorithm",
		"algorithm_type",
		"is_depends",
		"coin_url",
		"github_link",
		"miners",
		"market_cap",
		"volume",
		"circulating_supply",
		"emission",
		"exchange_name",
		"exchange_pair",
		"marke_price",
		"exchange_volume",
	}
	return res
}

func (c *CoinResult) Values() []string {
	res := []string{
		c.Name,
		c.Algorithm,
		c.AlgorithmType,
		strconv.FormatBool(c.IsDepends),
		c.CoinUrl,
		c.GithubLink,
		c.Miners,
		c.MarketCap,
		c.Volume,
		c.CirculatingSupply,
		c.Emission,
	}
	return res
}

func (c *CoinResult) ValuesV2() [][]string {
	values := [][]string{}
	for _, exchange := range c.Exchanges {
		value := []string{}
		value = append(value, c.Values()...)
		value = append(value, exchange.Values()...)
		values = append(values, value)
	}

	return values
}
