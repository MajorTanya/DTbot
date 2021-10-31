# DTbot
A versatile Discord bot for your server, written with discord.py.

## Features
We aim to provide a vast variety of commands for our users with simplicity of commands being one of our top priorities.
With our array of command modules, DTbot provides:
* Customizable prefixes on a per-server basis (`+help changeprefix` for more info)
* Measurement conversions, especially between Metric and US units (`+help Conversion`)
* Interaction commands with expressive gifs to enhance user interaction (`+help Interaction`)
* Simple math commands (`+help Maths`)
* RNG-based commands like rolling dice (`+help roll`) or spinning the roulette wheel (`+help roulette`)
* Overview and info commands (`+help General`)
* Anime/Manga lookup via AniList (`+help anime` / `+help manga`)
* and more!

## Permissions
DTbot requires certain permissions in order to function as intended. The invite link includes:
- **Change Nickname**: (DTbot is *planned* to change its nickname to show the prefix in future.)

- **View Channels/Read Messages**: DTbot needs to be able to read messages to watch for command calls. We **do not** store any messages.

- **Send Messages**: DTbot needs to be able to send messages itself so it can show the command results.

- **Embed Links**: Many of DTbot's commands use Discord's rich embeds to make nice-looking messages. If this is not provided, those commands will fail with an error message.

- **Use External Emoji**: DTbot uses some emotes from its support server in messages.

- **Add Reactions**: Several commands have users interact with DTbot through the reactions on DTbot's message. These commands won't work if DTbot is denied this permission. (These include the `+help` command)

## Hosting
We would appreciate it if you didn't host your own instances of DTbot. The code is provided here for transparency and potential educational uses.<br>
We also won't provide the (convoluted) `config.ini`.

DTbot can be invited via [this link](https://discord.com/api/oauth2/authorize?client_id=472730689599569921&permissions=67390528&scope=bot). Alternatively, use the `+info` command and click where it says "Invite me".
## Requirements
* Python 3.8+
* nextcord 2.0.0+
* MariaDB 10.4+ (server-side)
* (other) Dependencies listed in `requirements.txt`
