# talks-bot

Sending automated emails and discord messages for various seminar series.

## Prerequisites

You can install the prerequisites with `pip`.

```python
pip install -r requirements.txt
```

## Configuration

Before using the scripts, you must configure them using a `yml` file.

```yml
// The numbers after http://talks.bham.ac.uk/show/index/
admin:
  name: 
  email:
smtp:
  host: 
  port:
  user:
  password:
// Discord token, found at https://discord.com/developers/applications
discord:
seminars:
  - series:
    talks_id:
    // The list to send the emails to
    mailing_list:
    // The channel on the discord server to post the announcements in
    channel:
    zoom:
      link:
      id:
      password:
    room:
    // Announcement emails are sent to let people know the talk is happening
    announce:
      days_before: 2
      time: 10
    // Reminder emails are sent shortly before the talk takes place
    reminder:
      time: 10
```

## Usage

To maximise the effectiveness of this script, it should be run as a `cron` job.
It can be as frequent as you like, but once every hour should be fine.

To access your crontab use

```sh
crontab -e
```

and add this line

```sh
0 * * * * python3 main config logfile
```

where `main`, `config` and `logfile` are replaced with the locations of the `main.py` file, your config file, and where you want the logs to go.

Setting up the script in this way will send an email at `announce.time` on `announce.days_before` before the talk containing the details, and again at `reminder.time` on the day of the talk.

### Supplementary scripts

To test the scripts, or simply run them at an arbitrary time, some supplementary scripts are also provided.

```sh
python3 src/announce.py config logfile
python3 src/reminder.py config logfile
```

You can append `--stdout` to either script to print the emails to standard output rather than sending them or posting messages to discord.