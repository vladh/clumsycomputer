# From Scratch #1: A full-featured regex engine from scratch (Python, no imports)

video.clumsy.computer VOD: https://video.clumsy.computer/w/ptV4jwvwzWgwmTftzBika2

YouTube VOD: https://www.youtube.com/watch?v=fgp0tKWYQWY

Made [live on stream](https://twitch.tv/clumsycomputer) on 2020/06/29.

This is a regex engine we coded live on the
[clumsy computer stream](https://twitch.tv/clumsycomputer). It's around 240 lines of Python and is
a regex-directed engine based on backtracking. Because of this, and because of the way it's
written, it's not the fastest. However, it's written to be clear rather than fast.
It uses no libraries or imports of any kind.

It supports:

* Literals (`abc`)
* Sets (`[abc]`)
* Star/question mark/plus (`a*b?c+`)
* Alternates (`a|b`)
* Start and end (`^abc$`)
* Matching in the middle of a string an returning the match
* Custom escape sequences (`\a \d`)

It includes a simple test, so you can just run it with Python 3.
