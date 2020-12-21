# TwitterRemindBot
- Fun weekend project
- Checks users mentions for tweets and replies to them after a certain time period
- Everything but replying has been implemented
# Twitter Parsing Guide
- Checks all tweets in a users mentions
- If the tweet contains some numeric value + h or m it will extract said tweets.
- Example: '@Bot 14m Hello World'
- The numeric value is the time to be waited, and h or m specifies the unit of time. Where h specifies hours, and m specifies minutes.
- Bot will extract everything after the time specified as the message to be replied with.
- In the above example, the bot would have 'Hello World' as the reply message.
# Database Guide
- I just used a local mongo database.
- The database manager is responsible for inserting, searching, and deleteing database records.
- All times are stored and compared in UTC.
# Credentials
- bearer_token: Token used for Twitter API authentication.
- user_id: Twitter User's ID whose mentions will be polled.
- connection_string: Database connection string.
- database_name: Name of database to be used.
- collection_name: Collection of items within database to store records.
# Control Flow
1. Create an instance of TwitterBot and DBManager
2. Connect DBManager to database
3. Pass said instances to a busy loop
4. Check for new tweets from users mentions
5. If new tweets are found insert them into the database
6. Check database for tweets past deadline, return an instance of them, and remove them from database
7. Tweet the tweets that are past the deadline (Not implemented)
8. Repeat steps 4-7 forever.