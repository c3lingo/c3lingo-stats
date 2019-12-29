#!/bin/sh

function getpad {
  curl --cookie-jar cookiejar \
    --output pads/$1.txt \
    --silent \
    --location \
    https://c3translate.pad.foebud.org/ep/pad/export/36c3-$1/latest?\&format=txt
  echo $1
}

getpad day1
getpad day2
getpad day3
getpad day4

getpad wikipaka-day1
getpad wikipaka-day2
getpad wikipaka-day3
getpad wikipaka-day4

rm -f cookiejar
