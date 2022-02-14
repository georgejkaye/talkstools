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
  "day": "", // The day the talk takes place on: 0 is Monday ... 4 is Friday
  "announce_time": "",
  "reminder_time": "",
```
