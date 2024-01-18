# Imports
import pandas as pd
import requests
import datetime

client_id = "n4v1Gso81V6MUtbAhnvtfg"
client_secret = "dLfc-SsDDIL4VjIyklqLEA5zergWCw"
user_agent = "Landry Houston"
username = "LandryHouston"
password = "DSI1113LH"

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
data = {"grant_type": "password", "username": username, "password": password}

headers = {"User-Agent": "LandryHouston/0.0.1"}

res = requests.post(
    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers
)

token = res.json()["access_token"]
headers["Authorization"] = f"bearer {token}"


# Function to scrape from subreddit of choice


def scrape(subreddit):
    all_data = pd.DataFrame()
    last_id = None

    while True:
        res = requests.get(
            "https://oauth.reddit.com/r/" + subreddit + "/" + "new",
            headers=headers,
            params={"limit": "100", "after": last_id},
        )

        if not res.json()["data"]["children"]:
            break

        data = [
            {
                "id": post["data"]["id"],
                "subreddit": post["data"]["subreddit"],
                "date": pd.to_datetime(post["data"]["created_utc"], unit="s").date(),
                "title": post["data"]["title"],
                "text": post["data"]["selftext"],
            }
            for post in res.json()["data"]["children"]
        ]

        new_data_df = pd.DataFrame(data)

        all_data = pd.concat([all_data, new_data_df], ignore_index=True)

        last_id = "t3_" + new_data_df["id"].iloc[-1]

    return all_data


# scrape("anxiety").to_csv("../raw_data/raw_reddit_anxiety.csv", index=False)

anxi = pd.read_csv("../raw_data/raw_reddit_anxiety.csv")
anxi_df = pd.concat([scrape("anxiety"), anxi])
anxi_df.drop_duplicates(subset="id", keep="first", inplace=True)
anxi_df.to_csv("../raw_data/raw_reddit_anxiety.csv", index=False)

# scrape('depression').to_csv('../raw_data/raw_reddit_depression.csv', index= False)

depr = pd.read_csv("../raw_data/raw_reddit_depression.csv")
depr_df = pd.concat([scrape("depression"), depr])
depr_df.drop_duplicates(subset="id", keep="first", inplace=True)
depr_df.to_csv("../raw_data/raw_reddit_depression.csv", index=False)


df = len(anxi_df) + len(depr_df)
total = len(anxi) + len(depr)

current_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

with open("../raw_data/scrape_log.txt", "a") as file:
    file.write(
        f"{current_time} - Auto Scrape Successful - {df - total} New Posts - {df} Total Scraped\n"
    )
