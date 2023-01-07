import tweepy
import time
import requests
import pandas as pd 
import numpy as np
from datetime import datetime, timezone
import string
#import emoji

#pd.set_option('display.max_columns', None)
team_tag = {}
team_tag["Hawks"] = "#TrueToAtlanta"
team_tag["Celtics"] = "#BleedGreen"
team_tag["Nets"] = "#NetsWorld"
team_tag["Hornets"] = "#LetsFly"
team_tag["Bulls"] = "#BullsNation"
team_tag["Cavaliers"] = "#LetEmKnow"
team_tag["Mavericks"] = "#MFFL"
team_tag["Nuggets"] = "#MileHighBasketball"
team_tag["Pistons"] = "#Pistons"
team_tag["Warriors"] = "#DubNation"
team_tag["Rockets"] = "#Rockets"
team_tag["Pacers"] = "#BoomBaby"
team_tag["Clippers"] = "#ClipperNation"
team_tag["Lakers"] = "#LakeShow"
team_tag["Grizzlies"] = "#BigMemphis"
team_tag["Heat"] = "#HeatCulture"
team_tag["Bucks"] = "#FeerTheDear"
team_tag["Timberwolves"] = "#RaisedByWolves"
team_tag["Pelicans"] = "#Pelicans"
team_tag["Knicks"] = "#NewYorkForecer"
team_tag["Thunder"] = "#ThunderUp"
team_tag["Magic"] = "#MagicTogether"
team_tag["76ers"] = "#BrotherlyLove"
team_tag["Suns"] = "#WeAreTheValley"
team_tag["Trail Blazers"] = "#RipCity"
team_tag["Kings"] = "#SacramentoProud"
team_tag["Spurs"] = "#PorVida"
team_tag["Raptors"] = "#WeTheNorth"
team_tag["Jazz"] = "#TakeNote"
team_tag["Wizards"] = "DCAboveAll"

url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'

CONSUMER_KEY = 'I9PELf13z6AWfthSz8PvkpLZ5'
CONSUMER_SECRET = 'JslQWV6C4CdLtMJtBX06EprNUMefxHQS51rZbmhhUx33sTMpTh'
BEARER_KEY = 'AAAAAAAAAAAAAAAAAAAAAIUYlAEAAAAAE4hXxpFE5v9LUqetoY1e%2BWytn%2Fw%3Df1x76bMUxKdVQZrGlfKUmDSx7ziwqAWU99165hQIU5KLrO3ju3'
ACCESS_KEY = '3310071740-PhJaLKRnMOYziqG9mqmOw7mITap6GDiYYnszqSA'
ACCESS_SECRET = 'x1WzFtKL2OMv5Pj2nx78B4BApEFMtGk9MtEZLHyRewpm7'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth) 
date = str(datetime.now(timezone.utc))
month_year = date[5:7] + '/' + date[8:10]
date = date[0:10] + 'T' + date[11:19]
game_date = ''


finals = []
schedule = []

def remove(string):
    return "".join(string.split())

def nba_stats():
    url = 'https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json'

    r = requests.get(url)
    data = r.json()
    headers = data["scoreboard"]["games"]

    todays_games = []
    most_points = 0

    for game in headers:

        game_code = game["gameCode"]
        
        home_1 = game["homeTeam"]["teamName"]
        home = team_tag.get(home_1)
        home_wins = game["homeTeam"]["wins"]
        home_losses = game["homeTeam"]["losses"]
        away_1 = game["awayTeam"]["teamName"]
        away = team_tag.get(away_1)
        away_wins = game["awayTeam"]["wins"]
        away_losses = game["awayTeam"]["losses"]
        quarter = str(game["period"])
        score =  str(game["homeTeam"]["score"]) + '-' + str(game["awayTeam"]["score"])
        away_score = str(game["awayTeam"]["score"])
        home_score = str(game["homeTeam"]["score"])
        clock = str(game["gameClock"])[2:4] + ':' + str(game["gameClock"])[5:7]
        matchup = home + ' ' + '(' + str(home_wins) + '-' + str(home_losses) + ')' + ' ' + "vs" + ' ' + away + ' ' + '(' + str(away_wins) + '-' + str(away_losses) + ')'
        mactup_no_record = home + ' ' + "vs" + ' ' + away 
        todays_games.append(matchup)
        game_time = str(game["gameStatusText"])
        home_leader_name = str(game["gameLeaders"]["homeLeaders"]["name"]) + ' '
        home_leader_stat = str(game["gameLeaders"]["homeLeaders"]["points"]) + ' PTS'
        away_leader_name = str(game["gameLeaders"]["awayLeaders"]["name"]) +' '
        away_leader_stat = str(game["gameLeaders"]["awayLeaders"]["points"]) + ' PTS'

        if game["gameLeaders"]["homeLeaders"]["points"] > most_points:
            most_points = game["gameLeaders"]["homeLeaders"]["points"]
            most_points_name = game["gameLeaders"]["homeLeaders"]["name"]
        elif game["gameLeaders"]["awayLeaders"]["points"] > most_points:
            most_points = game["gameLeaders"]["awayLeaders"]["points"]
            most_points_name = game["gameLeaders"]["awayLeaders"]["name"]

        schedule_tweet = matchup + '\n' + '\n' + '@ '+game["homeTeam"]["teamCity"] + '\n' + '\n' + game_time



        #start_tweet = matchup  + '\n' + '\n' + "We are underway in " + game["homeTeam"]["teamCity"] + '!'
        potg = ''

        if(int(game["homeTeam"]["score"])  > int(game["awayTeam"]["score"])):
            potg = home_leader_name + '\n' +  home_leader_stat +' | ' + str(game["gameLeaders"]["homeLeaders"]["rebounds"]) + ' REB' + ' | ' + str(game["gameLeaders"]["homeLeaders"]["assists"]) + ' AST'
        else:
            potg = away_leader_name + '\n' +  away_leader_stat + ' | ' + str(game["gameLeaders"]["awayLeaders"]["rebounds"]) + ' REB' +' | ' + str(game["gameLeaders"]["awayLeaders"]["assists"]) + ' AST'

        if home_score > away_score:
            end_tweet = 'Final from ' + game["homeTeam"]["teamCity"] + '\n' + '\n' + home + ': ' + home_score + '\n'+ away + ': ' + away_score +  '\n' + '\n' + potg
            update_tweet = game["gameStatusText"] + '\n' + home + ': ' + home_score + '\n'+ away + ': ' + away_score + '\n' + '\n' + home_leader_name + '| '+  home_leader_stat + '\n' + away_leader_name + '| '+ away_leader_stat
        else:
            end_tweet = 'Final from ' + game["homeTeam"]["teamCity"] + '.' + '\n' + '\n' + away + ': ' + away_score + '\n' + home + ': ' + home_score + '\n' + '\n' + potg
            update_tweet = game["gameStatusText"] + '\n'  + away + ': ' + away_score + '\n' + home + ': ' + home_score + '\n' + '\n' + home_leader_name + '| '+  home_leader_stat + '\n' + away_leader_name + '| '+ away_leader_stat

        start_tweet = matchup  + '\n' + '\n' + "We are underway in " + game["homeTeam"]["teamCity"] + '!'

        #:round_pushpin:
        #end of quarter
        #"PT00M00.00S"

        if(date == game["gameTimeUTC"]):
            api.update_status(start_tweet)
            #print(start_tweet)
            continue
        elif game["gameStatus"] == 2:
            api.update_status(update_tweet)
            #print(update_tweet)
            continue
        elif game["gameStatus"] == 3:
            if (game_code in finals):
                continue
            api.update_status(end_tweet)
            #print(end_tweet)
            finals.append(game_code)
            continue
        elif (game_code in schedule):
            continue
        elif (game_code not in schedule):
            #print(schedule_tweet)
            api.update_status(schedule_tweet)
            schedule.append(game_code)
        else:
            continue

    return finals



counter = 0

while True:
    nba_stats()
    counter+= 1
    print(counter)
    time.sleep(900)


