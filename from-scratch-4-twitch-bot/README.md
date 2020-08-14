# From Scratch #4: An extensible Twitch bot (Python, no libraries)

VOD:

* [Coding an extensible Twitch bot from scratch in Python ! (#1 — Twitch bot from scratch)](https://youtu.be/hmWN41GMVWw)
* [Adding commands from Twitch chat with state (#2 — Twitch bot from scratch)](https://youtu.be/Hb108L1y7oY)

Made [live on stream](https://twitch.tv/clumsycomputer) on 2020/07/27.

This is a simple Twitch bot, which is structured such that it can be extended in
the future to support all kinds of functionality.

In the second part, we fixed some things we left out in the last video, and we added
the !addcmd, !editcmd and !delcmd commands, so that we can add and edit commands from
Twitch chat. We also added a file-based state, which you can use to create persistent
counters and quote trackers!

The bot supports two basic kinds of commands. Template commands are commands
such as "Welcome to the channel, {user}!". Custom commands are commands with
more advanced functionality — you can make them whatever you'd like.

You can get an oauth token by following the [Twitch
documentation](https://dev.twitch.tv/docs/irc), in particular by using the
[Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/).

To run the bot, create a `config.py` file that follows the format in `config_example.py`.
