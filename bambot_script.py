#!/usr/bin/env python

import sys
import twitter
import sqlite3
import argparse
import datetime

try:
    import config
except ImportError:
    print "Cannot find config file. Please reference README.md"
    sys.exit(1)

try:
    api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                      consumer_secret=config.CONSUMER_SECRET,
                      access_token_key=config.ACCESS_TOKEN_KEY,
                      access_token_secret=config.ACCESS_TOKEN_SECRET)
except twitter.TwitterError as e:
    print e.message

conn = sqlite3.connect(config.DB_PATH)


def find_streak():
    """
    Calculates the number of days (streak) between now and the last accident.
    Disregards the time and only finds the differences in dates.
    Returns:
        The difference in a datetime object's dates.
    """
    c = conn.cursor()

    try:
        c.execute('''SELECT *
                     FROM all_accidents
                     WHERE oid = (SELECT max(oid)
                     FROM all_accidents)''')
    except sqlite3.DatabaseError as e:
        print "Cannot fetch data from database."
        print e
        sys.exit(1)

    last_time = c.fetchone()[0]
    last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
    return datetime.date.today() - last_time.date()


def had_accident(location, accident_type="pee"):
    """
    Inserts accident into database and tweets it.
    Args:
        location (string): location of accident
        accident_type (string): type of accident. Default is "pee"
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c = conn.cursor()

    try:
        c.execute('INSERT INTO all_accidents VALUES ("%s", "%s","%s","%s")' %
                 (now, location, accident_type, find_streak()))
        conn.commit()
    except sqlite3.DatabaseError as e:
        print "Cannot insert data into database."
        print e
        conn.rollback()
        sys.exit(1)

    try:
        api.PostUpdate('I had an accident at %s. :(' % location)
    except twitter.TwitterError as e:
        print "Could not post to Twitter."

        try:
            print e.message[0]['message']
        except:
            print e.message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Bambot, a pet accident tracking bot, without the
                       --accident flag this posts the current accident free
                       streak.""",
        usage="%(prog)s [--accident 'location' 'type']")
    parser.add_argument('--accident', nargs='+',
                        help='''Accepts 1-2 arguments. First is location of the
                        accident (required). Second is accident type
                        (optional).''')
    args = parser.parse_args()

    if args.accident:
        had_accident(*args.accident)
    else:
        streak = find_streak()

        try:
            api.PostUpdate('It has been %s %s since my last accident!' %
                          (streak.days, "day" if streak.days == 1 else "days"))
        except twitter.TwitterError as e:
            print "Could not post to Twitter."

            try:
                print e.message[0]['message']
            except:
                print e.message

    conn.close()
