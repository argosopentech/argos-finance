// Read CSV file

package main

import (
	"encoding/csv"
	"log"
	"os"
)

type RSSFeed struct {
	URL string
}

func GetRSSFeeds() []RSS {
	// Load a csv file.
	f, err := os.Open("RSSFeeds.csv")
	if err != nil {
		log.Fatal(err)
	}

	// Create a new reader.
	r := csv.NewReader(f)
	r.Comma = ','
	r.Comment = '#'
	r.LazyQuotes = true
	r.FieldsPerRecord = -1

	// Read all the records.
	records, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	// Save the records.
	var RSSFeeds []RSS
	for _, record := range records {
		RSSFeeds = append(RSSFeeds, ReadRSS(record[0]))
	}

	return RSSFeeds
}
