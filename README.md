# auto-delete-tweets

Python bot hosted on Heroku that deletes old tweets of mine. Runs each day at 4am.

## Setup

1. [Install Python 3](https://www.python.org/downloads/)

2. Install Tweepy and APScheduler with pip

3. [Create a Twitter developer account](https://developer.twitter.com/en/apply-for-access)

4. Create an app in the Twitter developer portal and note the provided keys. You'll need these later on

3. [Create a Heroku account](https://signup.heroku.com/)

4. [Install the Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

5. Clone this repository and navigate to the root with the Heroku CLI

8. Log in to the Heroku CLI by calling `heroku login`

9. Initialize the Heroku app by calling `heroku create your-app-name`

10. To set the remote repository, call `heroku git:remote -a your-app-name`

11. In clock.py, set the date and time you want the worker to run

12. In delete.py, set the twitter_user variable to your Twitter account username

13. Using the keys from step 4, go to the Heroku Dashboard and select settings. Reveal the Config Vars and input each of the keys

14. In the Heroku Dashboard Overview tab, make sure to configure your Dynos so the worker and clock are active

15. You can scale the clock using the Heroku CLI with `heroku ps:scale clock=1`