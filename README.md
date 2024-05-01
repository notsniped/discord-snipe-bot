# Discord Snipe Bot
![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=You+can+snipe+message+content;You+can+editsnipe+message+content)

This is a bot made with the same message content sniping API from isobot and Arch bot. The bot uses built-in Discord slash commands (`/`), so all commands start with the `/` prefix.

When you run the bot for the first time, you will go through the client's initial setup process, which allows you to enter the bot token and the owner's username. No fiddling required.

# Features
- `/snipe` command to show the most recently deleted message in a channel.

- `/editsnipe` command to show the most recently edited message in a channel.

- Deleted and edited message audit logging channel features for server mods. (`/set_audit_channel`)

# How to Use
### Installation
No pre-run installation is required, as all the libraries that the bot needs are already packaged into Discord Snipe Bot. Just to make it easier for you 👍

### Running
Run this code in command prompt/terminal:

```
$ cd path/to/folder/
$ python Main.py
```

When you run this, the client will ask you to input a **Discord bot token** and your **Discord username**. Simply paste them into the prompts during the setup process.

(you can get a bot token from making a new application at https://discord.com/developers)

***WARNING!!* DO NOT PASTE YOUR DISCORD BOT TOKEN IN `Main.py`!** Please put it either in `config.json` or paste it in the bot setup process during startup. __This is to prevent your Discord bot token from being accidentally leaked.__

**NOTE:** Before running the program, remember to enable the `Message Content Intent` in your Application's Bot Settings. Otherwise the bot won't be able to read any messages and it will not work.

![image](https://github.com/notsniped/discord-snipe-bot/assets/72265661/0b614f53-7626-459b-a727-d192a000565b)

![image](https://github.com/notsniped/discord-snipe-bot/assets/72265661/db034c75-2ac6-458e-a67b-72456f3a8bbf)

# Bug Reporting, Ideas, and Contribution
### If you have any new ideas for this bot, or want to report a bug, please make an [issue](https://github.com/notsniped/discord-snipe-bot/issues/new) and we'll get to it. If you want to contribute code to our repository, [pull requests](https://github.com/notsniped/discord-snipe-bot/pulls) are appreciated.

:)
<h6>i use arch btw</h6>
