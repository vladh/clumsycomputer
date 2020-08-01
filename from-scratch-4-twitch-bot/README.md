# From Scratch #4: An extensible Twitch bot (Python, no libraries)

VOD: https://youtu.be/pT45y04wEZg

Made [live on stream](https://twitch.tv/clumsycomputer) on 2020/07/27.

This is a simple Twitch bot, which is structured such that it can be extended in
the future to support all kinds of functionality. If you liked this video, let
me know and I'll create a second part explaining how to extend the bot such
that you can add and remove commands from the chat, and create more complex
functionality such as a list of quotes.

The bot supports two basic kinds of commands. Template commands are commands
such as "Welcome to the channel, {user}!". Custom commands are commands with
more advanced functionality — you can make them whatever you'd like.

To run the bot, create a `config.py` file that follows the format in `config_example.py`.
