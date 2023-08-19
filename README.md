# DTbot

A versatile Discord bot for your server, written with discord.py & nextcord.

Currently running:

* v3 (modern Slash Commands, like `/info`)

**For current announcements regarding DTbot, check the [ANNOUNCEMENTS.md](ANNOUNCEMENTS.md).**

## Features

We aim to provide a vast variety of commands for our users with simplicity of commands being one of our top priorities.
With our array of command modules, DTbot provides:

* Measurement conversions, especially between Metric and US units
    * Examples include
        * `/cmin` for Centimeters to Inches and `/incm` for Inches to Centimeters
        * `/lgal` for Liters to US Gallons and `/gall` for US Gallons to Liters
        * `/cf` for Celsius to Fahrenheit and `/fc` for Fahrenheit to Celsius
    * All Conversion commands are written as `/FromUnitToUnit`
        * We currently support:
            * Kilometers <> Miles (`/kmmi` & `/mikm`), Meters <> Feet (`/mft` & `/ftm`), Meters <> Feet & Inches
              (`/mftin` & `/ftinm`), Centimeters <> Feet (`/cmft` & `/ftcm`), Centimeters <> Inches  (`/cmin` & `/incm`)
            * Celsius <> Fahrenheit (`/cf` & `/fc`)
            * Liters <> US Gallons (`/lgal` & `/gall`), Milliliters <> US Fluid Ounces (`/mlfloz` & `/flozml`)
            * Kilograms <> US Pounds (`/kglbs` & `/lbskg`)
* Interaction commands with expressive GIFs to enhance user interaction
    * Examples include
        * `/handholding [user]`, `/hug [user]`, `/pat [user]`, and many more (currently 20+ kinds of interactions)
* Simple math commands (all begin with `/maths`)
    * `/maths add`, `/maths subtract`, `/maths square`, `/maths multiply`, `/maths divide`
    * `/maths percentage` to figure out what percentage something is (15 apples of 60? It's 25%)
    * `/maths percentof` to figure out what a percentage of something equates to (25% of 60? It's 15)
* RNG-based commands like rolling dice (`/roll`), flipping a coin (`/coinflip`), or a Magic 8 Ball (`/8ball`)
    * `/roll` supports a variety of options and modifiers, like dropping the lowest roll, adding something to the
      result, and more. Check out the options and modifiers available in the command.
* Various utility commands
    * `/avatar [user]`, `/changelog`, `/info`, `/userinfo [user]`, `/whohas [role]`, `/ping`, `/uptime`, `/xp [user]`
* Anime/Manga lookup via AniList (`/anime [title]` and `/manga [title]`)
* and more!

### Suggestions?

If you have an idea for a command for DTbot (or you want a removed command back), you can use the `/request` command to
suggest it.

## Permissions

DTbot requires certain permissions in order to function as intended. The invite link includes:

- **View Channels/Read Messages**: DTbot needs to be able to read messages to watch for command calls. We **do not**
  store any messages.

- **Send Messages**: DTbot needs to be able to send messages itself, so it can show the command results.

- **Embed Links**: Many of DTbot's commands use Discord's rich embeds to make nice-looking messages. If this is not
  provided, those commands will fail with an error message.

- **Use External Emoji**: DTbot uses some emotes from its support and developer servers in messages.

### Obsolete Permissions

If DTbot still has these permissions in your server from earlier versions, you can remove them without issue:

- **Add Reactions** - This was used in v2 and earlier to handle navigation in multi-embed response such as a paged
  `/whohas` output. This was replaced by using buttons instead.

## Hosting & Adding DTbot to your Server

We would appreciate it if you didn't host your own instances of DTbot. The code is provided here for transparency and
potential educational uses.<br>
We also won't provide the (convoluted) `config.ini`.

If you already share a server with DTbot, you can click the "Add to Server" button in DTbot's profile.

Alternatively, use the `/info` command and click where it says "Invite me".

DTbot can be invited
via [this link](https://discord.com/api/oauth2/authorize?client_id=472730689599569921&permissions=281600&scope=applications.commands%20bot)
.

## Questions?

Ask away in the [DTbot Support Server](https://discord.gg/kSPMd2v).

## Requirements

* Python 3.10+
* discord.py 2.0.0+
* MariaDB 10.4+ (server-side)
* MariaDB Connector/C (server-side, for MariaDB Connector/Python)
* (other) Dependencies listed in `requirements.txt`
