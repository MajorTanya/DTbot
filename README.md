# DTbot

A versatile Discord bot for your server, written with discord.py

Currently running:

* **v2 has been retired, see below** ~v2 ("classic") (traditional command use, like @DTbot help and +help)~
* v3 (modern Slash Commands, like `/info`) (check the [`v3`](https://github.com/MajorTanya/DTbot/tree/v3) branch)

## Announcement Re: DTbot v2 shutdown
(Announcement made: 2022-12-31)

### TL;DR

* DTbot v2 ('classic', the mention syntax version) will shut down **January 1st, 2023 at 00:00 UTC**
* v3 (Slash Commands based version, like `/info`) will continue to work
* There was little to no use of v2, shutting it down enables full focus on v3 and beyond.

### Shutting down DTbot v2 ('classic')

For quite a while, we've encouraged the use of Slash Commands, and many new users probably didn't even know DTbot
supported the mentioning syntax, or even the prefix-based syntax, as they will have discovered DTbot's Slash 
Commands through Discord's built-in discovery tools.
There have been some slight headaches recently with DTbot's access to the new App Discovery feature, and having only
one version active makes adjusting to policy changes a lot easier, as well as allowing full focus on fixes and new
features.

We thank you for your long-time use of text-based and mention-based DTbot versions, but it is time to look towards
the future, and what better opportunity than the change of the year. With that, we wish you a Happy New Year 2023 and
a lot of fun using DTbot v3!

## Announcement Re: Discord restricting Message Content for Bots
(Announcement made: 2022-06-22)

### TL;DR

* DTbot will stay online and work as usual until **September 1st, 2022**.
* DTbot v3 has been launched with Slash Commands ~(*runs in parallel to the v2*)~
* **v2 has been retired, see above** ~**Past September 1st**, v2 commands will only work with `@DTbot info`, `@DTbot hug @someone`, etc.~
  * ~*ALL* prefixes (`+` and custom ones) will cease to work.~
  * Use Slash Commands instead.

### Message Content

Discord is restricting access to message content starting September 1st, 2022, meaning **the `+` (or any custom)
prefix will stop working** and DTbot will instead **only respond to mentions and Slash Commands (soon™)**. This
functionality is already present, you just need to use e.g. `@DTbot roll 2d20` where you did `+roll 2d20` before.

DTbot v2 has too many commands (150+ with all aliases and such) to be able to transition to Discord's Slash
Commands without losing any functionality while staying true to its focus on ease of use.
Work on a Slash Command-based v3 are ongoing, and once released will be run *in parallel* to v2 ("classic"). This will
enable you to use modern Slash Commands at the same time as the classic `@DTbot <command>` structure.

v2 will be maintained as long as feasible, but new features and commands will be exclusive to v3. Should Discord
kill commands with the mentioning syntax, v2 will be retired for good.

## Features

We aim to provide a vast variety of commands for our users with simplicity of commands being one of our top priorities.
With our array of command modules, DTbot provides:

* Customizable prefixes on a per-server basis (`@DTbot help changeprefix` for more info)
* Measurement conversions, especially between Metric and US units (`@DTbot help Conversion`)
* Interaction commands with expressive gifs to enhance user interaction (`@DTbot help Interaction`)
* Simple math commands (`@DTbot help Maths`)
* RNG-based commands like rolling dice (`@DTbot help roll`) or spinning the roulette wheel (`@DTbot help roulette`)
* Overview and info commands (`@DTbot help General`)
* Anime/Manga lookup via AniList (`@DTbot help anime` / `@DTbot help manga`)
* and more!

## Permissions

DTbot requires certain permissions in order to function as intended. The invite link includes:

- **View Channels/Read Messages**: DTbot needs to be able to read messages to watch for command calls. We **do not**
  store any messages.

- **Send Messages**: DTbot needs to be able to send messages itself, so it can show the command results.

- **Embed Links**: Many of DTbot's commands use Discord's rich embeds to make nice-looking messages. If this is not
  provided, those commands will fail with an error message.

- **Use External Emoji**: DTbot uses some emotes from its support server in messages.

- **Add Reactions**: Several commands have users interact with DTbot through the reactions on DTbot's message. These
  commands won't work if DTbot is denied this permission. (Including the `@DTbot help` command)

## Hosting & Adding DTbot to your Server

We would appreciate it if you didn't host your own instances of DTbot. The code is provided here for transparency and
potential educational uses.<br>
We also won't provide the (convoluted) `config.ini`.

If you already share a server with DTbot, you can click the "Add to Server" button in DTbot's profile.

Alternatively, use the `@DTbot info` command and click where it says "Invite me".

DTbot can be invited
via [this link](https://discord.com/api/oauth2/authorize?client_id=472730689599569921&permissions=281664&scope=applications.commands%20bot)
.

## Questions?

Ask away in the [DTbot Support Server](https://discord.gg/kSPMd2v).

## Requirements

* Python 3.8+
* discord.py 2.0+
* MariaDB 10.4+ (server-side)
* (other) Dependencies listed in `requirements.txt`
