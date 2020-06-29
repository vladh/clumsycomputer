# A regex engine as seen on clumsycomputer 2020/06/29

VOD: Coming soon!

This is a regex engine we coded live on the
[clumsycomputer stream](https://twitch.tv/clumsycomputer). It's around 240 lines of Python and is
a regex-directed engine based on backtracking. It uses no libraries or imports of any kind.

It supports:

* Literals (`abc`)
* Sets (`[abc]`)
* Star/question mark/plus (`a*b?c+`)
* Alternates (`a|b`)
* Start and end (`^abc$`)
* Matching in the middle of a string an returning the match
* Custom escape sequences (`\a \d`)

It includes a simple test, so you can just run it with Python 3.
