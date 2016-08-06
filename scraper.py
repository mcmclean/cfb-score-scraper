import pandas as pd
import re
from dateparser import parse

#################################################################################################################

week_range = [1]
year_range = [2015]

#################################################################################################################
urls = []

for year in year_range:
    for week in week_range:
        urls.append('http://www.cbssports.com/collegefootball/scoreboard/FBS/' + str(year) + '/week' + str(week))

weeks = []

for url in urls:
    frame = pd.read_html(url)
    fb_week = url.split('week')[1]
    
    this_year_arr = re.split('\D', url)
    this_year = list(filter(lambda v : len(v) > 0, this_year_arr))
    year = this_year[0]
    
    game_frame = pd.DataFrame({'Date' : [], 'Away Team' : [], 'Home Team' : [], 
    'Away Q1' : [], 'Home Q1' : [], 'Away Q2' : [], 'Home Q2' : [], 
    'Away Q3' : [], 'Home Q3' : [], 'Away Q4' : [], 'Home Q4' : [], 
    'Away Final' : [], 'Home Final' : [], 'Away Record:  After' : [], 'Home Record:  After' : [], 
    'Away Wins' : [], 'Home Wins' : [], 'Away Losses' : [], 'Home Losses' : [], 
    'Away Rank Prior' : [], 'Home Rank Prior' : [] , 'OT' : [], 'Week' : []})

    count = 0
    games1 = map(lambda x : x, filter(lambda y : len(y) > 1, frame))
    games = map(lambda x : x, filter(lambda y : y[0][0].strip() != "Cancelled" and y[0][0].strip() != "Postponed", games1))
    for game in games:
        try:
            try:
                arr = game[0][1].split('#')
                away_team = arr[0]
                record_rank = arr[1].split('(')
                away_rank = record_rank[0]
                away_record = record_rank[1][:len(record_rank[1])-1]
                win_loss = away_record.split('-')
                away_wins = win_loss[0]
                away_losses = win_loss[1]
            except:
                parens = []
                for i in range(0, len(list(game[0][1]))):
                    if bool(re.search('\(', list(game[0][1])[i])) == True:
                        parens.append(i)
                if len(parens) > 1:
                    idx = parens[len(parens)-1]
                    arr = [game[0][1][:idx], game[0][1][idx:]]
                else:
                    arr = str(game[0][1]).split('(')
                away_team = arr[0]
                away_record = arr[1][:len(arr[1])-1]
                win_loss = away_record.split('-')
                away_wins = win_loss[0]
                away_losses = win_loss[1]
                away_rank = "Unranked"
            
            try:
                arr = game[0][2].split('#')
                home_team = arr[0]
                record_rank = arr[1].split('(')
                home_rank = record_rank[0]
                home_record = record_rank[1][:len(record_rank[1])-1]
                win_loss = home_record.split('-')
                home_wins = win_loss[0]
                home_losses = win_loss[1]  
            except:
                parens = []
                for i in range(0, len(list(game[0][2]))):
                    if bool(re.search('\(', list(game[0][2])[i])) == True:
                        parens.append(i)
                if len(parens) > 1:
                    idx = parens[len(parens)-1]
                    arr = [game[0][2][:idx], game[0][2][idx:]]
                else:
                    arr = str(game[0][2]).split('(')
                home_team = arr[0]
                home_record = arr[1][:len(arr[1])-1]
                win_loss = home_record.split('-')
                home_wins = win_loss[0]
                home_losses = win_loss[1]
                home_rank = "Unranked"

            date = str(game[0][0]).strip() + " " + year
            date = date.replace('Thurs', 'Thursday')
            # did not handle "Thurs" well
            date1 = re.split('[^a-zA-Z0-9]+', date)
            date3 = list(filter(lambda v : len(v) > 0, date1))
            date2 = " ".join(date3).strip()
            
            ncols = len(game)
            
            if ncols == 3:            
                game_frame = game_frame.append({'Date' : parse(date2).date(), 'Away Team' : away_team, 'Home Team' : home_team, 
                'Away Q1' : int(game[1][1]), 'Home Q1' : int(game[1][2]), 'Away Q2' : int(game[2][1]), 'Home Q2' : int(game[2][2]), 
                'Away Q3' : int(game[3][1]), 'Home Q3' : int(game[3][2]), 'Away Q4' : int(game[4][1]), 'Home Q4' : int(game[4][2]), 
                'Away Final' : int(game[5][1]), 'Home Final' : int(game[5][2]), 'Away Record:  After' : away_record, 'Home Record:  After' : home_record,
                'Away Wins' : away_wins, 'Home Wins' : home_wins, 'Away Losses' : away_losses, 'Home Losses' : home_losses, 
                'Away Rank Prior' : away_rank, 'Home Rank Prior' : home_rank, 'OT' : 0, 'Week' : fb_week}, ignore_index=True)
            else:
                game_frame = game_frame.append({'Date' : parse(date2).date(), 'Away Team' : away_team, 'Home Team' : home_team, 
                'Away Q1' : int(game[1][2]), 'Home Q1' : int(game[1][3]), 'Away Q2' : int(game[2][2]), 'Home Q2' : int(game[2][3]), 
                'Away Q3' : int(game[3][2]), 'Home Q3' : int(game[3][3]), 'Away Q4' : int(game[4][2]), 'Home Q4' : int(game[4][3]), 
                'Away Final' : int(game[len(game)-1][2]), 'Home Final' : int(game[len(game)-1][3]), 'Away Record:  After' : away_record, 'Home Record:  After' : home_record,
                'Away Wins' : away_wins, 'Home Wins' : home_wins, 'Away Losses' : away_losses, 'Home Losses' : home_losses, 
                'Away Rank Prior' : away_rank, 'Home Rank Prior' : home_rank, 'OT' : 1, 'Week' : fb_week}, ignore_index=True)
                

        except:
            print("Error")
            print(game)
            print()

    game_frame = game_frame[['Date', 'Away Team' , 'Home Team' , 
    'Away Q1' , 'Home Q1' , 'Away Q2' , 'Home Q2' , 
    'Away Q3' , 'Home Q3' , 'Away Q4' , 'Home Q4' , 
    'Away Final' , 'Home Final' , 'Away Record:  After', 'Home Record:  After',
    'Away Wins', 'Home Wins', 'Away Losses', 'Home Losses', 
    'Away Rank Prior', 'Home Rank Prior', 'OT', 'Week']]
    
    weeks.append(game_frame)
    
print(weeks)


# write to CSV

# work on other sites?

# potentially season-long tools and statistics??

# big stretch:  other sports