# DTbot Announcements

General announcements regarding DTbot. Current announcements are accessible with the `/announcements` Slash Command. It
is always a good idea to check that command, as not all announcements are of high enough importance to warrant an entry
on this document.

* *Newest* announcement is placed at the *top*.
* Announcements are dated in the `YYYY-MM-DD` format to avoid date confusions.
* Where applicable, a "TL;DR" (Too Long; Didn't Read) section is placed before the main announcement text.

---

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

---

## Announcement Re: Discord restricting Message Content for Bots

(Announcement made: 2022-06-22)

### TL;DR

* DTbot will stay online and work as usual until **September 1st, 2022**.
* DTbot v3 with Slash Commands is up and running *in parallel* to v2
* **v2 has been retired, see above**
    * ~~**Past September 1st**, v2 commands will only work with `@DTbot info`, `@DTbot hug @someone`, etc.~~
        * ~~*ALL* prefixes (`+` and custom ones) will cease to work.~~
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