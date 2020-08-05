#!/usr/bin/env python
import socket
import ssl
import datetime
import random
import json
from collections import namedtuple

import config


Message = namedtuple(
    'Message',
    'prefix user channel irc_command irc_args text text_command text_args',
)


def remove_prefix(string, prefix):
    if not string.startswith(prefix):
        return string
    return string[len(prefix):]


class Bot:
    def __init__(self):
        self.irc_server = 'irc.chat.twitch.tv'
        self.irc_port = 6697
        self.oauth_token = config.OAUTH_TOKEN
        self.username = 'squishymcbotty'
        self.channels = ['squishymcbotty', 'vladh']
        self.command_prefix = '!'
        self.state = {}
        self.state_filename = 'state.json'
        self.state_schema = {
            'template_commands': {},
            'doggo_counter': 0,
        }
        self.custom_commands = {
            'date': self.reply_with_date,
            'ping': self.reply_to_ping,
            'randint': self.reply_with_randint,
            'doggo': self.increment_doggo,
            'addcmd': self.add_template_command,
            'editcmd': self.edit_template_command,
            'delcmd': self.delete_template_command,
            'cmds': self.list_commands,
        }

    def init(self):
        self.read_state()
        self.connect()

    def ensure_state_schema(self):
        is_dirty = False
        for key in self.state_schema:
            if key not in self.state:
                is_dirty = True
                self.state[key] = self.state_schema[key]
        return is_dirty

    def read_state(self):
        with open(self.state_filename, 'r') as file:
            self.state = json.load(file)
        is_dirty = self.ensure_state_schema()
        if is_dirty:
            self.write_state()

    def write_state(self):
        with open(self.state_filename, 'w') as file:
            json.dump(self.state, file)

    def send_privmsg(self, channel, text):
        self.send_command(f'PRIVMSG #{channel} :{text}')

    def send_command(self, command):
        if 'PASS' not in command:
            print(f'< {command}')
        self.irc.send((command + '\r\n').encode())

    def connect(self):
        self.irc = ssl.wrap_socket(socket.socket())
        self.irc.connect((self.irc_server, self.irc_port))
        self.send_command(f'PASS {self.oauth_token}')
        self.send_command(f'NICK {self.username}')
        for channel in self.channels:
            self.send_command(f'JOIN #{channel}')
            self.send_privmsg(channel, 'Hey there!')
        self.loop_for_messages()

    def get_user_from_prefix(self, prefix):
        domain = prefix.split('!')[0]
        if domain.endswith('.tmi.twitch.tv'):
            return domain.replace('.tmi.twitch.tv', '')
        if 'tmi.twitch.tv' not in domain:
            return domain
        return None

    def parse_message(self, received_msg):
        parts = received_msg.split(' ')

        prefix = None
        user = None
        channel = None
        text = None
        text_command = None
        text_args = None
        irc_command = None
        irc_args = None

        if parts[0].startswith(':'):
            prefix = remove_prefix(parts[0], ':')
            user = self.get_user_from_prefix(prefix)
            parts = parts[1:]

        text_start = next(
            (idx for idx, part in enumerate(parts) if part.startswith(':')),
            None
        )
        if text_start is not None:
            text_parts = parts[text_start:]
            text_parts[0] = text_parts[0][1:]
            text = ' '.join(text_parts)
            if text_parts[0].startswith(self.command_prefix):
                text_command = remove_prefix(text_parts[0], self.command_prefix)
                text_args = text_parts[1:]
            parts = parts[:text_start]

        irc_command = parts[0]
        irc_args = parts[1:]

        hash_start = next(
            (idx for idx, part in enumerate(irc_args) if part.startswith('#')),
            None
        )
        if hash_start is not None:
            channel = irc_args[hash_start][1:]

        message = Message(
            prefix=prefix,
            user=user,
            channel=channel,
            text=text,
            text_command=text_command,
            text_args=text_args,
            irc_command=irc_command,
            irc_args=irc_args,
        )

        return message

    def handle_template_command(self, message, text_command, template):
        try:
            text = template.format(**{'message': message})
            self.send_privmsg(message.channel, text)
        except IndexError:
            text = f"@{message.user} Your command is missing some arguments!"
            self.send_privmsg(message.channel, text)
        except Exception as e:
            print('Error while handling template command.', message, template)
            print(e)

    def reply_with_date(self, message):
        formatted_date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        text = f'Here you go {message.user}, the date is: {formatted_date}.'
        self.send_privmsg(message.channel, text)

    def reply_to_ping(self, message):
        text = f'Hey {message.user}, nice ping! PONG!'
        self.send_privmsg(message.channel, text)

    def reply_with_randint(self, message):
        text = str(random.randint(0, 1000))
        self.send_privmsg(message.channel, text)

    def add_template_command(self, message, force=False):
        if len(message.text_args) < 2:
            text = f"@{message.user} Usage: !addcmd <name> <template>"
            self.send_privmsg(message.channel, text)
            return

        command_name = remove_prefix(message.text_args[0], self.command_prefix)
        template = ' '.join(message.text_args[1:])

        if command_name in self.state['template_commands'] and not force:
            text = f"@{message.user} Command {command_name} already exists, use {self.command_prefix}editcmd if you'd like to edit it."
            self.send_privmsg(message.channel, text)
            return

        self.state['template_commands'][command_name] = template
        self.write_state()
        text = f"@{message.user} Command {command_name} added!"
        self.send_privmsg(message.channel, text)

    def edit_template_command(self, message):
        return self.add_template_command(message, force=True)

    def delete_template_command(self, message):
        if len(message.text_args) < 1:
            text = f"@{message.user} Usage: !delcmd <name>"
            self.send_privmsg(message.channel, text)
            return

        command_names = [
            remove_prefix(arg, self.command_prefix)
            for arg in message.text_args
        ]

        if not all([
            command_name in self.state['template_commands']
            for command_name in command_names
        ]):
            text = f"@{message.user} One of the commands doesn't exist!"
            self.send_privmsg(message.channel, text)
            return

        for command_name in command_names:
            del self.state['template_commands'][command_name]

        self.write_state()
        text = f'@{message.user} Commands deleted: {" ".join(command_names)}'
        self.send_privmsg(message.channel, text)

    def list_commands(self, message):
        template_cmd_names = list(self.state['template_commands'].keys())
        custom_cmd_names = list(self.custom_commands.keys())
        all_cmd_names = [
            self.command_prefix + cmd
            for cmd in template_cmd_names + custom_cmd_names
        ]
        text = f'@{message.user} ' + ' '.join(all_cmd_names)
        self.send_privmsg(message.channel, text)

    def increment_doggo(self, message):
        self.state['doggo_counter'] += 1
        text = f'Doggos seen: {self.state["doggo_counter"]}'
        self.send_privmsg(message.channel, text)
        self.write_state()

    def handle_message(self, received_msg):
        if len(received_msg) == 0:
            return

        message = self.parse_message(received_msg)
        # print(f'> {message}')
        print(f'> {received_msg}')

        if message.irc_command == 'PING':
            self.send_command('PONG :tmi.twitch.tv')

        if message.irc_command == 'PRIVMSG':
            if message.text_command in self.custom_commands:
                self.custom_commands[message.text_command](message)
            elif message.text_command in self.state['template_commands']:
                self.handle_template_command(
                    message,
                    message.text_command,
                    self.state['template_commands'][message.text_command],
                )

    def loop_for_messages(self):
        while True:
            received_msgs = self.irc.recv(2048).decode()
            for received_msg in received_msgs.split('\r\n'):
                self.handle_message(received_msg)


def main():
    bot = Bot()
    bot.init()


if __name__ == '__main__':
    main()
