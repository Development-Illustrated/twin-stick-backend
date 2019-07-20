package main

import (
	"encoding/json"
	"fmt"
	_ "github.com/lafriks/go-tiled"
	"os"
	_ "os"

)

var tilemap struct {
	Height       int     `json:"height"`
	Width        int     `json:"width"`
	Infinite     bool    `json:"infinite"`
	Nextlayerid  int     `json:"nextlayerid"`
	Nextobjectid int     `json:"nextobjectid"`
	Orientation  string  `json:"orientation"`
	Renderorder  string  `json:"renderorder"`
	Tileheight   int     `json:"tileheight"`
	Tilewidth    int     `json:"tilewidth"`
	Type         string  `json:"type"`
	Version      float64 `json:"version"`
	Layers       []struct {
		Data    []int  `json:"data"`
		Height  int    `json:"height"`
		ID      int    `json:"id"`
		Name    string `json:"name"`
		Opacity int    `json:"opacity"`
		Type    string `json:"type"`
		Visible bool   `json:"visible"`
		Width   int    `json:"width"`
		X       int    `json:"x"`
		Y       int    `json:"y"`
	} `json:"layers"`
	Tilesets []struct {
		Columns     int    `json:"columns"`
		Firstgid    int    `json:"firstgid"`
		Image       string `json:"image"`
		Imageheight int    `json:"imageheight"`
		Imagewidth  int    `json:"imagewidth"`
		Margin      int    `json:"margin"`
		Name        string `json:"name"`
		Spacing     int    `json:"spacing"`
		Tilecount   int    `json:"tilecount"`
		Tileheight  int    `json:"tileheight"`
		Tilewidth   int    `json:"tilewidth"`
	} `json:"tilesets"`
}

const mapPath = "assets/base-map-file.json" // path to your map


func main() {

	// then config file settings

	jsonFile, err := os.Open(mapPath)
	if err != nil {
		fmt.Printf("opening config file", err.Error())
	}

	jsonParser := json.NewDecoder(jsonFile)
	if err = jsonParser.Decode(&tilemap); err != nil {
		fmt.Printf("parsing config file", err.Error())
	}

	fmt.Printf("%v %s %s", tilemap.Height, tilemap.Width)
	return
}

//func main() {
//	// parse tmx file
//	gameMap, err := tiled.LoadFromFile(mapPath)
//
//	if err != nil {
//		fmt.Println("Error parsing map")
//		os.Exit(2)
//	}
//
//	fmt.Print(gameMap)
//}

//func main() {
//
//	const height, width int = 400, 500
//	var layer1 [width][height]int
//
//	var i, j int
//
//	for i = 0; i < width; i++ {
//		for j = 0; j < height; j++ {
//			layer1[i][j] = 0
//		}
//	}
//
//	fmt.Println("Numbers:", layer1)
//
//}
