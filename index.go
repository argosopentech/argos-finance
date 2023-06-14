package main

import (
	"fmt"
	"html/template"
	"net/http"
)

type Article struct {
	Title string
	Link  string
}

type PageData struct {
	PageTitle string
	Articles  []Article
}

func main() {
	RSSFeeds := GetRSSFeeds()

	Articles := []Article{}
	for _, RSSFeed := range RSSFeeds {
		for _, item := range RSSFeed.Channel.Items {
			Article := Article{
				Title: item.Title,
				Link:  item.Link,
			}
			Articles = append(Articles, Article)
			fmt.Println(Article)
		}
	}

	tmpl := template.Must(template.ParseFiles("index.html"))
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		data := PageData{
			PageTitle: "Argos Finance",
			Articles:  Articles,
		}

		// Execute template and check for errors
		err := tmpl.Execute(w, data)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}

	})
	http.ListenAndServe(":8080", nil)
}
