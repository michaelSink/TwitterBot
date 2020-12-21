import TwitterBot as tb
import DBManager as db
import time

def busy_loop(twitter_bot, db_manager):
    while True:
        tweets = twitter_bot.listen()
        if(len(tweets) > 0):
            db_manager.insert_list(tweets)
        to_tweet_records = db_manager.search_and_update()
        time.sleep(5)

def main():

    bearer_token = ""
    user_id = 0

    connection_string = ""
    database_name = ""
    collection_name = ""

    bot = tb.TwitterBot(bearer_token, user_id)
    manager = db.DBManager(connection_string, database_name, collection_name)
    manager.connect()
    busy_loop(bot, manager)

if __name__ == "__main__":
    main()