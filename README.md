Bambot
===
Bambot is a twitter bot that keeps track of how long your pet has been accident free.

Setup
---
####Getting the Twitter keys
Before Bambot can run, you need to sign up with a Twitter dev account and
register a new app: <https://dev.twitter.com/apps/new>. 

You'll need:
* Consumer Key
* Consumer Secret
* Access Token Key
* Access Token Secret

Paste the values in the config file. I've included a `sample_config.py` file. Make
sure you rename it to `config.py`.

```sh
?> mv sample_config.py config.py
```

####Installing the python-twitter library
To install the python-twitter library, run:
```sh
?> sudo pip install python-twitter
```
*Note: you can run without `sudo` if you are running via `virtualenv`

####Creating the database
Bambot uses sqlite3. To create your database run:
```sh
?> sqlite3 yourdatabase.db
```

To set up your table run:
```sh
sqlite> .read setup.sql
```
Your database is now ready for all your pet's accidents!

Logging Accidents
---
Every time your pet has an accident, you can update your twitter bot by running this prompt:
```sh
?> python bambot_script.py --accident "location" "accident_type"
```
Location is required, but accident_type is optional and defaults to "pee". Bambot will post to your twitter with the following message: `I had an accident at [location]. :(`

Setting up streak
---
Bambot will also update the twitter feed with how long it has been since the last accident when run without an accident flag. You can set up how often Bambot updates by setting up a cronjob.

```sh
?> crontab -e
```

Mine looks like this:
```sh
#MIN HOUR DOM MON DOW CMD
30   13   *   *   *   /path/to/bambot_script.py
```
Contact
---
If you have any questions, comments, or bug reports, feel free to send me an email at tchoN at gmail.com, replace N with 308+400.

