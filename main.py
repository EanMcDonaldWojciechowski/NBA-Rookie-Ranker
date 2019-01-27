from nba_api.stats.endpoints import commonallplayers, playercareerstats
import json
from sklearn import linear_model
import pandas as pd
import time



player_info = commonallplayers.CommonAllPlayers()

player_json = player_info.get_json()

parsed_player = json.loads(player_json)


playerdata = parsed_player.get("resultSets")[0]['rowSet']
playerDataHeader = parsed_player.get("resultSets")[0]['headers']
print(playerDataHeader)

# SET COLUMNS LATER
listOfRookieID = []

#playerStats = []
for playerInfo in playerdata:
    # playerInfo[4] is year started playing
    if playerInfo[4] == '2018':
        # set key in dict equal to player ID, value to rest of player info
        listOfRookieID.append(playerInfo[0])
        


listOfRookieStatsObj = []
player_stat_json = []
player_stat_parsed = []
listOfRookieStats = []
listOfRookieStatHeader = []

for idx in enumerate(listOfRookieID):
    print(listOfRookieID[idx[0]])
    listOfRookieStatsObj.append(playercareerstats.PlayerCareerStats(listOfRookieID[idx[0]]))
    time.sleep(1)
    player_stat_json.append(listOfRookieStatsObj[idx[0]].get_json())
    player_stat_parsed.append(json.loads(player_stat_json[idx[0]]))
    #print(player_stat_parsed[idx[0]])
    listOfRookieStats.append(player_stat_parsed[idx[0]].get("resultSets")[0]['rowSet'])
    print(listOfRookieStats[idx[0]])


listOfRookieStatHeader.append(player_stat_parsed[idx[0]].get("resultSets")[0]['headers'])
print(listOfRookieStatHeader)

print(listOfRookieStats[0])
print(listOfRookieStatHeader)
#df_rookies = pd.DataFrame(listOfRookieID, columns=['ID'])
df_rookies = pd.DataFrame(listOfRookieStats, columns=listOfRookieStatHeader)
#print(df_rookies)

#################################
#df_rookies.to_csv("output.csv", encoding='utf-8')
#df = df_rookies.read_csv("output.csv")


#rookieStatsForReg = {}
#for id, info  in rookieDict.items():
# rookieStatsForReg[rookieStatsForReg[]]