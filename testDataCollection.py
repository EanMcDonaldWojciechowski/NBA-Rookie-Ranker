from nba_api.stats.endpoints import commonallplayers, playercareerstats
import json
import pandas as pd
import time

rawPlayerData = commonallplayers.CommonAllPlayers()
playerJsonData = rawPlayerData.get_json()
parsedPlayerJson = json.loads(playerJsonData)

allPlayerData = parsedPlayerJson.get("resultSets")[0]['rowSet']
playerDataHeader = parsedPlayerJson.get("resultSets")[0]['headers']


playerIDs = []

for playerInfo in allPlayerData:
    # playerInfo[4] is year started playing
    if playerInfo[4] == '2018':
        # set key in dict equal to player ID, value to rest of player info
        playerIDs.append(playerInfo[0])        

listOfRookieStatsObj = []
player_stat_json = []
player_stat_parsed = []

RookieStats2018 = []
listOfRookieStatHeader = []

# parsing and collecting test data
for idx in enumerate(listOfRookieID):
    listOfRookieStatsObj.append(playercareerstats.PlayerCareerStats(listOfRookieID[idx[0]], per_mode36="PerGame"))
    time.sleep(1)
    player_stat_json.append(listOfRookieStatsObj[idx[0]].get_json())
    player_stat_parsed.append(json.loads(player_stat_json[idx[0]]))
    if (len(player_stat_parsed[idx[0]].get("resultSets")[0]['rowSet']) < 1):
        RookieStats2018.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    elif (len(player_stat_parsed[idx[0]].get("resultSets")[0]['rowSet']) >= 1):
        RookieStats2018.append(player_stat_parsed[idx[0]].get("resultSets")[0]['rowSet'][0])
    print(RookieStats2018[idx[0]])

listOfRookieStatHeader = player_stat_parsed[idx[0]].get("resultSets")[0]['headers']
df_rookiesTestData = pd.DataFrame(data=RookieStats2018, columns=listOfRookieStatHeader) 
df_rookiesTestData = df_rookiesTestData.drop(['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 
'GS', 'FGA', 'FG3A', 'FTA', 'OREB', 'DREB', 'TOV', 'PF'], axis=1)
print(df_rookiesTestData)
df_rookiesTestData.to_csv("rookieTestData.csv", encoding='utf-8')