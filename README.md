# bravo-emails

Sending automated emails for the University of Birmingham Theory Group PhD seminar, Bravo.

## Configuration

To set up the script, you must fill out a `config.json` with relevant data.

```jsonc
{
  "talks_id": "",  // The numbers after http://talks.bham.ac.uk/show/index/
  "smtp": {
    "host": "",
    "port": "",
    "user": "",
    "password": ""
  },
  "sender_email": "",
  "recipient_email": "", 
  "zoom": {
    "link": "",
    "id": "",
    "password": ""
  },
  "room": "",
  "admin": {
      "name": "",
      "email": ""
  },
  // The day the talk takes place on: 0 is Monday ... 4 is Friday
  "talk_day": "",
  // OPTIONAL: Announcement emails are sent to let people know the talk is happening
  "announce": {
    "day": 0,
    "time": "10:00"
  },
  // OPTIONAL: Reminder emails are sent shortly before the talk takes place
  "reminder": {
    // How many days before the talk to send the reminder
    "offset": 0,
    "time": "10:00"
  },
  // OPTIONAL: Before the announcement is made, check for the abstract and title
  "abstract": {
    // How many days before the announcement to make the check
    "offset": 1, 
    "time": "10:00"
  }
}
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

Setting up the script in this way will send an email at `config["announce_time"]` on Monday with the details of that week's talk (if one is happening), and again at `config["reminder_time"]` on the day of the talk.

### Supplementary scripts

To test the scripts, or simply run them at an arbitrary time, some supplementary scripts are also provided.

```sh
python3 src/announce.py config logfile
python3 src/reminder.py config logfile
```
