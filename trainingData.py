from nba_api.stats.endpoints import commonallplayers, playercareerstats
import json
import pandas as pd
import time

# collecting and parsing all player data to collect player IDs
rawPlayerData = commonallplayers.CommonAllPlayers()
playerJsonData = rawPlayerData.get_json()
parsedPlayerJson = json.loads(playerJsonData)

allPlayerData = parsedPlayerJson.get("resultSets")[0]['rowSet']
playerDataHeader = parsedPlayerJson.get("resultSets")[0]['headers']

playerIDs = []

for playerInfo in allPlayerData:
    # playerInfo[4] is year started playing    
    if playerInfo[4] != '2018':
        # set key in dict equal to player ID, value to rest of player info
        playerIDs.append(playerInfo[0])
    
rawPlayerStats = []
playerStatJson = []
playerStatParsed = []

stats = []

# parsing and collecting training data
for idx in enumerate(playerIDs):
    # collecting data from API for every player's career game avg stats, based on the given player's id in playerIDs
    rawPlayerStats.append(playercareerstats.PlayerCareerStats(playerIDs[idx[0]], per_mode36="PerGame"))
    # sleep to prevent spamming api
    time.sleep(1)
    # extracting json from api call
    playerStatJson.append(rawPlayerStats[idx[0]].get_json())
    # loads json data
    playerStatParsed.append(json.loads(playerStatJson[idx[0]]))

    # some players have empty data, so dummy data is entered for said players to keep the order of players 
    # consistant in both the playerIDs list and the stats list because player IDs are removed from the stats 
    # list in the future, meaning the only thing identifying a given player's stats is their index in the 
    # stats list, which lines up with their index in the playerIDs list
    if (len(playerStatParsed[idx[0]].get("resultSets")[0]['rowSet']) < 1):
        stats.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    # else, the given player's stats are appended to the stats list
    elif (len(playerStatParsed[idx[0]].get("resultSets")[0]['rowSet']) >= 1):
        stats.append(playerStatParsed[idx[0]].get("resultSets")[0]['rowSet'][0])
    print(stats[idx[0]])

    # there are thousands of players and grabbing all their data takes a long time,
    # so for now only 500 players are grabbed for the purpose of training data
    if idx[0] > 500:
        break
    print(playerIDs[idx[0]])    

# gets the header names for the dataframe from the parsed json
statHeader = playerStatParsed[idx[0]].get("resultSets")[0]['headers']

# enters all data into a dataframe
playerStatsDataFrame = pd.DataFrame(data=stats, columns=statHeader) 

# drops columns that will not be used in the regression model
playerStatsDataFrame = playerStatsDataFrame.drop(['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 
'GS', 'FGA', 'FG3A', 'FTA', 'OREB', 'DREB', 'TOV', 'PF'], axis=1)
print(playerStatsDataFrame)

# outputs the data to a csv for quick use in main
playerStatsDataFrame.to_csv("TrainingData.csv", encoding='utf-8')