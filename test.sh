#!/bin/bash

function test() {
	if [ ! -f output/variants_12w/$1.txt ]; then
		return
	fi
	echo "file: $1"
	echo "free weekend in the end: $(cat output/variants_12w/$1.txt | grep "oo$" | wc -l)"
	echo "busy weekend in the end: $(cat output/variants_12w/$1.txt | grep "JJ$" | wc -l)"
}

test "1-week"
test "2-weeks"
test "4-weeks"
test "8-weeks"
