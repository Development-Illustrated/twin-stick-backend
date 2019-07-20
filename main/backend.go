package main

import (
	"fmt"
)

func main() {

	var height, width int = 400, 500
	var layer1 [height][width] int

	var i, j int

	for  i = 0; i < width; i++ {
		for j = 0; j < height; j++ {
			layer1[i][j] = 0
		}
	}

	fmt.Println("Numbers:" layer1)


}

