# flexaphoto

Flexaphoto - hexatetraflexagon photo album generator

## Introduction

A flexagon is a piece of a paper folded so that it can be "flexed"
to show more than just the usual front and back faces. One of them
is a hexatetraflexagon, which has six faces and four edges.

This script takes six images as input and produce two output images
which, if printed back-to-back, can be folded into a hexatetraflexagon
photo album.

## Requirements

* Python 3
* PIL (Python Imaging Library)

## Usage

There's not much at the command line right now. Just run:

`python3 flexaphoto.py 1.jpg 2.jpg 3.jpg 4.jpg 5.jpg 6.jpg`

and it will output `front.jpg` and `back.jpg`. Print them
back-to-back, making sure to centre it on the page so they
line up. Cut and fold as per Matt Parker's instructions on
Numberphile: https://youtu.be/7H4lDi79YY8
