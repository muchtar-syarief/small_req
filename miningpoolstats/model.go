package main

import "strconv"

type Stat struct {
	MarketCap         string `csv:"market_cap"`         // #stats_marketcap
	Volume            string `csv:"volume"`             // #stats_volume
	CirculatingSupply string `csv:"circulating_supply"` // #stats_supply_circulating
	Emission          string `csv:"emission"`           // #stats_supply_emission
}

type CoinResult struct {
	Name          string `csv:"name"`
	IsDepends     bool   `csv:"is_depends"`
	Algorithm     string `csv:"algorithm"`
	AlgorithmType string `csv:"algorithm_type"`
	CoinUrl       string `csv:"coin_url"`
	GithubLink    string `csv:"github_link"`
	Miners        string `csv:"miners"`
	Stat
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
