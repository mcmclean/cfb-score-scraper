import pandas as pd
import re
import csv
import os
from numpy.linalg import inv
import numpy as np

############################################################################################################################################

# Specify week and year ranges

week_range = [1, 2, 3, 4, 5]
# week_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
year_range = [2016]

############################################################################################################################################

# Synonym Mapping

inpath = os.path.join(os.getcwd(), 'teams.csv')
fbs = []
with open(inpath, 'r') as f:
    for row in f:
        fbs.append(str(row).strip())

def team_map(name):
    lower = name.lower()
    
    if lower in ['akr', 'akron']:
        lower = 'akron'
    elif lower in ['arizona st.', 'arizona state']:
        lower = 'arizona state'
    elif lower in ['arkansas st.', 'arkansas state']:
        lower = 'arkansas state'
    elif lower in ['aub', 'auburn']:
        lower = 'auburn'
    elif lower in ['ball st.', 'ball state', 'ball']:
        lower = 'ball state'
    elif lower in ['bgsu', 'bowling green']:
        lower = 'bowling green'
    elif lower in ['brigham young', 'byu']:
        lower = 'brigham young'
    elif lower in ['buff', 'buffalo']:
        lower = 'buffalo'
    elif lower in ['char', 'charlotte']:
        lower = 'charlotte'
    elif lower in ['cmu', 'c. michigan', 'central michigan']:
        lower = 'central michigan'
    elif lower in ['clem', 'clemson']:
        lower = 'clemson'
    elif lower in ['colorado state', 'csu']:
        lower = 'colorado state'
    elif lower in ['e. michigan', 'emu', 'eastern michigan']:
        lower = 'eastern michigan'
    elif lower in ['fresno st.', 'fresno state']:
        lower = 'fresno state'
    elif lower in ['ga. southern', 'gaso']:
        lower = 'georgia southern'
    elif lower in ['georgia state', 'gast']:
        lower = 'georgia state'
    elif lower in ['idho', 'idaho']:
        lower = 'idaho'
    elif lower in ['ill', 'illinois']:
        lower = 'illinois'
    elif lower in ['kansas state', 'ksu', 'kansas st.']:
        lower = 'kansas state'
    elif lower in ['kentucky', 'ky']:
        lower = 'kentucky'
    elif lower in ['m. tenn. st.', 'mtsu']:
        lower = 'middle tennessee state'
    elif lower in ['mass', 'massachusetts']:
        lower = 'massachusetts'
    elif lower in ['umoh', 'miami (ohio)']:
        lower = 'miami (ohio)'
    elif lower in ['michigan', 'um']:
        lower = 'michigan'
    elif lower in ['mississippi state', 'msst']:
        lower = 'mississippi state'
    elif lower in ['new mexico st.', 'nmsu', 'nmst']:
        lower = 'new mexico state'
    elif lower in ['san diego state', 'san diego st.', 'sdsu']:
        lower = 'san diego state'
    elif lower in ['san jose state', 'san jose st.', 'sjsu']:
        lower = 'san jose state'
    elif lower in ['south alabama', 'usm']:
        lower = 'south alabama'
    elif lower in ['ul lafayette', 'ull', 'laf']:
        lower = 'ul lafayette'
    elif lower in ['ul monroe', 'ulm', 'la.-monroe']:
        lower = 'ul monroe'
    elif lower in ['unt', 'north texas']:
        lower = 'north texas'
    elif lower in ['stan', 'stanford']:
        lower = 'stanford'
    elif lower in ['tulsa', 'tlsa']:
        lower = 'tulsa'
    elif lower in ['tul', 'tulane']:
        lower = 'tulane'
    elif lower in ['texas-el paso', 'utep']:
        lower = 'utep'
    elif lower in ['w. kentucky', 'wky']:
        lower = 'western kentucky'
    elif lower in ['washington st.', 'wsu']:
        lower = 'washington state'
    elif lower in ['w. michigan', 'wmu']:
        lower = 'western michigan'
    elif lower not in fbs:
        # function to return all fcs teams (to ensure that they're in fact fcs)
        lower = "fcs_team"

    return lower


############################################################################################################################################

# Collect URLs to scrape

urls = []

for year in year_range:
    for week in week_range:
        urls.append('http://www.cbssports.com/college-football/scoreboard/FBS/' + str(year) + '/regular/' + str(week))

############################################################################################################################################

# Scrape and compile scores

weeks = []

for url in urls:
    frame = pd.read_html(url)
    fb_week = url.split('regular/')[1]
    
    this_year_arr = re.split('\D', url)
    this_year = list(filter(lambda v : len(v) > 0, this_year_arr))
    year = this_year[0]
    
    game_frame = pd.DataFrame({'Date' : [], 'Away Team' : [], 'Home Team' : [], 
    'Away Final' : [], 'Home Final' : [], 'Away Record After' : [], 'Home Record After' : [], 
    'Away Rank Prior' : [], 'Home Rank Prior' : []})

    games1 = map(lambda x : x, filter(lambda y : len(y) > 1, frame))

    try:
        games = map(lambda x : x, filter(lambda y : len(y.columns) >= 6, games1))
    except:
        games = games1

    for game in games:
        def collect_info(game, num):
            arr = game.ix[num,0].split('  ')
            if len(arr) == 3:
                team = arr[1]
                rank = arr[0]
                record = arr[2]
            elif len(arr) == 2:
                if bool(re.search('\d', arr[0])) == True:
                    team = arr[1]
                    rank = arr[0]
                    record = "0-0"
                else:
                    team = arr[0]
                    rank = "Unranked"
                    record = arr[1]
            elif len(arr) == 1:
                team = arr[0]
                rank = "Unranked"
                record = "0-0"
            wins = record.split('-')[0]; losses = record.split('-')[1]

            final_margin = game.ix[num,5] - game.ix[(num+1)%2,5]
            team = team_map(team)
            return str(team), str(rank), str(wins), str(losses), int(final_margin)

        try:
            away_team, away_rank_prior, away_wins, away_losses, away_margin = collect_info(game, 0)
            home_team, home_rank_prior, home_wins, home_losses, home_margin = collect_info(game, 1)

            date = "Week " + fb_week + ", " + year

            game_frame = game_frame.append({'Date' : date, 'Away Team' : away_team, 'Home Team' : home_team, 
            'Away Final' : away_margin, 'Home Final' : home_margin, 
            'Away Record After' : "(" + away_wins + "-" + away_losses + ")", 'Home Record After' : "(" + home_wins + "-" + home_losses + ")",
            'Away Rank Prior' : away_rank_prior, 'Home Rank Prior' : home_rank_prior}, ignore_index=True)
        
        except:
            print("Error")
            print(game)
            print()
            pass

    
    game_frame = game_frame[['Date', 'Away Team' , 'Home Team' , 
    'Away Final' , 'Home Final' ,
    'Away Record After', 'Home Record After',
    'Away Rank Prior', 'Home Rank Prior']]

    weeks.append(game_frame)
    
final = pd.DataFrame()
for week in weeks:
    final = pd.concat([final, week], ignore_index = True)

############################################################################################################################################

# Write scores dataframe to file

# outpath = os.path.join(os.getcwd(), 'all_weeks.csv')
# final.to_csv(outpath, index = False, header = True)

############################################################################################################################################

# Read back in the scores

# outpath = os.path.join(os.getcwd(), 'all_weeks.csv')
# final = pd.read_csv(outpath)

############################################################################################################################################

# Create counts/games matrix

listed_teams = []
for team in final['Home Team']:
    listed_teams.append(team)
for team in final['Away Team']:
    listed_teams.append(team)

listed_teams = list(set(listed_teams))
listed_teams.sort()

team_cts = pd.DataFrame(index = listed_teams, columns = listed_teams)
team_cts = team_cts.fillna(0)
for i in range(0, len(final)):
    team_a = final['Home Team'][i]
    team_b = final['Away Team'][i]
    team_cts[team_a][team_b] = team_cts[team_a][team_b] - 1
    team_cts[team_b][team_a] = team_cts[team_b][team_a] - 1
for i in range(0, len(team_cts)):
    team_cts.ix[i,i] = -team_cts.ix[i,:].sum()

############################################################################################################################################

# Make margin totals

def compile_totals(team_list, full_frame):
    margins = pd.DataFrame(index = team_list, columns = ['Margin'])
    margins = margins.fillna(0)

    for team in team_list:
        total = 0
        for i in range(0, len(full_frame)):

            if(team == full_frame['Home Team'][i]):
                add = int(full_frame['Home Final'][i])
                total = total + add
            elif(team == full_frame['Away Team'][i]):
                add = int(full_frame['Away Final'][i])
                total = total + add

        margins['Margin'][team] = total
    return margins

team_margins = compile_totals(listed_teams, final)

############################################################################################################################################

# Make rankings

invA = inv(team_cts.as_matrix())
B = team_margins.as_matrix()
raw = np.dot(invA, B)
raw = raw - np.mean(raw)

rankings = pd.DataFrame(raw, index = listed_teams)
rankings.columns = ['Rank']

# rankings_minus_fcs = rankings.drop(rankings.index['fcs_team'])
# print(rankings_minus_fcs)
# print(rankings)

rankings = rankings.sort(columns = 'Rank', ascending = False)
print(rankings)

outpath3 = os.path.join(os.getcwd(), 'rankings.csv')
rankings.to_csv(outpath3, index = True, header = True)

############################################################################################################################################

# Compiling team name list (only needs to be done once per year)

# teams = []
# for j in range(0, len(final)):
#     teams.append(final['Away Team'][j].lower())
#     teams.append(final['Home Team'][j].lower())

# teams = list(set(teams))
# # print(teams)

# outpath2 = os.path.join(os.getcwd(), 'teams.csv')

# team_list = pd.DataFrame(teams)
# team_list.to_csv(outpath2, index = False, header = False)


############################################################################################################################################

# Older margins stuff

# team_margins = pd.DataFrame(index = listed_teams, columns = ['Margin'])
# team_margins = team_margins.fillna(0)

# for team in listed_teams:
#     total = 0
#     for i in range(0, len(final)):
#         if(team == final['Home Team'][i]):
#             total = total + int(final['Home Final'][i])
#         elif(team == final['Away Team'][i]):
#             total = total + int(final['Away Final'][i])
#     team_margins['Margin'][team] = total