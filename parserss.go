package main

import (
	"encoding/xml"
	"log"
	"net/http"
)

// Based on:
// https://stackoverflow.com/questions/34975837/parsing-rss-feed-in-go

type Enclosure struct {
	Url    string `xml:"url,attr"`
	Length int64  `xml:"length,attr"`
	Type   string `xml:"type,attr"`
}

type RSSItem struct {
	Title     string    `xml:"title"`
	Link      string    `xml:"link"`
	Desc      string    `xml:"description"`
	Guid      string    `xml:"guid"`
	Enclosure Enclosure `xml:"enclosure"`
	PubDate   string    `xml:"pubDate"`
}

type Channel struct {
	Title string    `xml:"title"`
	Link  string    `xml:"link"`
	Desc  string    `xml:"description"`
	Items []RSSItem `xml:"item"`
}

type RSS struct {
	Channel Channel `xml:"channel"`
}

func ReadRSS(Url string) RSS {
	// Set Agent Type HTTP header
	// https://stackoverflow.com/questions/13263492/set-user-agent-in-http-request

	client := &http.Client{}

	req, err := http.NewRequest("GET", Url, nil)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("User-Agent", "Argos Finance")

	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	rss := RSS{}

	decoder := xml.NewDecoder(resp.Body)
	err = decoder.Decode(&rss)
	if err != nil {
		log.Fatal(err)
	}

	return rss

	/*
		fmt.Printf("Channel title: %v\n", rss.Channel.Title)
		fmt.Printf("Channel link: %v\n", rss.Channel.Link)

		for i, item := range rss.Channel.Items {
			fmt.Printf("%v. item title: %v\n", i, item.Title)
		}
	*/
}
