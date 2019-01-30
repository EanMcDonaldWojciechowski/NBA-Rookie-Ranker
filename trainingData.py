from nba_api.stats.endpoints import commonallplayers, playercareerstats
import json
import pandas as pd
import time

player_info = commonallplayers.CommonAllPlayers()
player_json = player_info.get_json()
parsed_player = json.loads(player_json)

playerdata = parsed_player.get("resultSets")[0]['rowSet']
playerDataHeader = parsed_player.get("resultSets")[0]['headers']

TrainingDataIDs = []

#playerStats = []
for playerInfo in playerdata:
    # playerInfo[4] is year started playing    
    if playerInfo[4] != '2018':
        TrainingDataIDs.append(playerInfo[0])

       
TrainingStatsObj = []
TrainingPlayer_stat_json = []
TrainingPlayer_stat_parsed = []

TrainingStats = []

# parsing and collecting training data
for idx in enumerate(TrainingDataIDs):
    TrainingStatsObj.append(playercareerstats.PlayerCareerStats(TrainingDataIDs[idx[0]], per_mode36="PerGame"))
    time.sleep(1)
    TrainingPlayer_stat_json.append(TrainingStatsObj[idx[0]].get_json())
    TrainingPlayer_stat_parsed.append(json.loads(TrainingPlayer_stat_json[idx[0]]))
    if (len(TrainingPlayer_stat_parsed[idx[0]].get("resultSets")[0]['rowSet']) < 1):
        TrainingStats.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    elif (len(TrainingPlayer_stat_parsed[idx[0]].get("resultSets")[0]['rowSet']) >= 1):
        TrainingStats.append(TrainingPlayer_stat_parsed[idx[0]].get("resultSets")[0]['rowSet'][0])
    print(TrainingStats[idx[0]])
    if idx[0] > 500:
        break
    print(TrainingDataIDs[idx[0]])    


trainingStatHeader = TrainingPlayer_stat_parsed[idx[0]].get("resultSets")[0]['headers']

df_TrainingData = pd.DataFrame(data=TrainingStats, columns=trainingStatHeader) 
df_TrainingData = df_TrainingData.drop(['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 
'GS', 'FGA', 'FG3A', 'FTA', 'OREB', 'DREB', 'TOV', 'PF'], axis=1)
print(df_TrainingData)

df_TrainingData.to_csv("TrainingData.csv", encoding='utf-8')