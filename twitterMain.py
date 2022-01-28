import requests
import datetime as dt
import os
bearer_token = os.environ.get("bearer_token")

header = {
    "authorization": f"Bearer {bearer_token}"
}


def getID():

    parameters = {
        "usernames": "sante_qc",
    }

    TWITTER_SEARCH = "https://api.twitter.com/2/users/by"
    response = requests.get(
        url=TWITTER_SEARCH, params=parameters, headers=header)
    response.raise_for_status()
    data = response.json()
    id = data["data"][0]["id"]
    return id


def time():
    now = dt.datetime.now(dt.timezone.utc)
    todayUTC = now.replace(hour=16, minute=0, second=0, microsecond=1)
    if now > todayUTC:
        date = dt.date.today()
        return date
    else:
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        return yesterday


ID = getID()
TIME = time()


def getContent(id=ID, date=str(TIME)):
    TWITTER_SEARCH = f"https://api.twitter.com/2/users/{ID}/tweets"
    startDate = f"{date}T15:00:00Z"
    endDate = f"{date}T17:30:00Z"

    parameters = {
        "media.fields": "url",
        "expansions": "attachments.media_keys",
        "start_time": {startDate},
        "end_time": {endDate}

    }

    response = requests.get(
        url=TWITTER_SEARCH, params=parameters, headers=header)
    response.raise_for_status()
    data = response.json()
    return data


def textContent(id=ID, date=str(TIME)):
    tweetContent = getContent(id, date)
    try:
        tweetData = tweetContent["data"][0]["text"]
    except KeyError:
        return f"No dashboard on {date}"
    return tweetData


def imageUrl(id=ID, date=str(TIME)):
    try:
        tweetContent = getContent(id, date)
        print(TIME)
        print(getContent())
        tweetImg = tweetContent["includes"]["media"][0]["url"]
        return tweetImg
    except KeyError:
        return "due to certain reasons"


# print(TIME)
# print(id)
# print(str(TIME))
# print(textContent())
# print(imageUrl())
