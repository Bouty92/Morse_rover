#!/bin/bash

cd /tmp
rename -e 's/\d+/sprintf("%04d",$&)/e' -- *.jpg

convert 'morse_screenshot_*.jpg[1024x]' resized_%04d.jpg

#avconv -r 25 -start_number 40 -i morse_screenshot_%04d.jpg crawling.mp4
#avconv -r 25 -start_number 40 -i resized_%04d.jpg crawling_lite.mp4
