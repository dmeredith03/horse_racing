import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.cm as cm
import streamlit as st
import pandas as pd
import numpy as np


import re
import math
from datetime import date, timedelta

st.set_page_config(page_title='Race Info', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    pp = pd.read_csv(uploaded_file, header=None)

    races = pp[[0, 1, 2, 5, 6, 8, 9, 22, 12, 11, 213, 214, 215, 217, 216]]
    races.columns = ['Track', 'Date', 'Race', 'Distance', 'Surface', 'Type', 'Restrictions', 'Breed Type', 'Claiming', 'Purse', '2fP', '4fP', '6fP', 'LP', 'SpeedPar']
    races['Surface'] = races['Surface'].str.upper()
    races['Distance'] = races['Distance'].apply(lambda x: f'{round(x/220,2)} f' if x < 1760 else f'{round(x/1760,2)} M')
    races = races.drop_duplicates().reset_index(drop = True)

    horses = pp[[2, 3, 44, 43, 209, 210, 250, 1177, 1178, 1179, 1180, 1327, 1328, 1329, 1330, 1263, 1264, 1265, 1266, 45, 48, 61, 50, 61, 63, 223, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 230, 231, 232, 233, 234, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 
                96, 97, 98, 99, 100, 27, 28, 29, 30, 31, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 32, 34, 35, 36, 37, 1156, 1157, 1158, 1159, 1160 ,1161, 1162, 1163, 1164, 1165, 1367, 1368, 1369, 1370, 1371, 218, 219, 220, 221, 222, 1412, 1413, 1414, 1415, 1416, 
                1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351,1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1370, 1371]]

    horses.columns = ['Race', 'PP', 'Name', 'ML', 
                    'Style', 'ES', 'PrimePower', 
                    'FstSpdB', 'TrfSpdB', 'WetSpdB', 'DistSpdB', 'LTSpdB', 'CYSpdB', 'PYSpdB', 'TrkSpdB',
                    'FstPed', 'TrfPed', 'WetPed', 'DistPed',
                    'YR', 'Sex', 'L', 'Weight', 'Medication', 'Equipment Change', 'Days Since', 
                    'DistT', 'DistW', 'DistP', 'DistS', 'DistE', 
                    'TrkT', 'TrkW', 'TrkP', 'TrkS', 'TrkE', 
                    'TrfT', 'TrfW', 'TrfP', 'TrfS', 'TrfE',
                    'AwT', 'AwW', 'AwP', 'AwS', 'AwE', 
                    'WetT', 'WetW', 'WetP', 'WetS', 'WetE', 
                    'Yr1', 'Yr1T', 'Yr1W', 'Yr1P', 'Yr1S', 'Yr1E', 
                    'Yr2', 'Yr2T', 'Yr2W', 'Yr2P', 'Yr2S', 'Yr2E', 
                    'LtT', ' LtW', 'LtP', 'LtS', 'LtE',
                    'Trainer', 'TR', 'TW', 'TP', 'TS', 'TCYR', 'TCYW', 'TCYP', 'TCYS', 'TCYRoi', 'TPYR', 'TPYW', 'TPYP', 'TPYS', 'TPYRoi',
                    'Jockey', 'JR', 'JW', 'JP', 'JS', 'JCYR', 'JCYW', 'JCYP', 'JCYS', 'JCYRoi', 'JPYR', 'JPYW', 'JPYP', 'JPYS', 'JPYRoi', 'JDR', 'JDW', 'JDP', 'JDS', 'JDRoi',
                    'JwTR', 'JwTW', 'JwTP', 'JwTS', 'JwTRoi', 'JwTMR', 'JwTMW', 'JwTMP', 'JwTMS', 'JwTMRoi',
                    'KTS1', 'KT1R', 'KT1W', 'KT1S', 'KT1Roi', 'KTS2', 'KT2R', 'KT2W', 'KT2S', 'KT2Roi', 'KTS3', 'KT3R', 'KT3W', 'KT3S', 'KT3Roi', 'KTS4', 'KT4R', 'KT4W', 'KT4S', 'KT4Roi', 'KTS5', 'KT5R', 'KT5W', 'KT5S', 'KT5Roi', 'KTS6', 'KT6R', 'KT6W', 'KT6S', 'KT6Roi',
                    'KJS1', 'KJ1R', 'KJ1W', 'KJ1S', 'KJ1Roi']
    horses['Trainer'] = horses['Trainer'].str.title()
    horses['Jockey'] = horses['Jockey'].str.title()
    
    jt_info = pd.DataFrame(columns=['Race', 'PP', 'T/J', 'Category', 'Starts', 'Wins', 'Win %', 'ROI'])
    for index, row in horses.iterrows():
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Trainer'], 'Category': 'Current Year', 'Starts': row['TCYR'], 'Wins': row['TCYW'], 'Win %': row['TCYW']/row['TCYR'] if row['TCYR'] > 0 else 0, 'ROI': row['TCYRoi']}])], ignore_index=True)
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Trainer'], 'Category': 'Previous Year', 'Starts': row['TPYR'], 'Wins': row['TPYW'], 'Win %': row['TPYP']/row['TPYR'] if row['TPYR'] > 0 else 0, 'ROI': row['TPYRoi']}])], ignore_index=True)
        for i in range(1, 7):
            jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Trainer'], 'Category': row['KTS' + str(i)], 'Starts': row['KT' + str(i) + 'R'], 'Wins': row['KT' + str(i) + 'W']/100 * row['KT' + str(i) + 'R'], 'Win %': row['KT' + str(i) + 'W']/100, 'ROI': row['KT' + str(i) + 'Roi']}])], ignore_index=True)

        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Jockey'], 'Category': 'Current Year', 'Starts': row['JCYR'], 'Wins': row['JCYW'], 'Win %': row['JCYW']/row['JCYR'] if row['JCYR'] > 0 else 0, 'ROI': row['JCYRoi']}])], ignore_index=True)
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Jockey'], 'Category': 'Previous Year', 'Starts': row['JPYR'], 'Wins': row['JPYW'], 'Win %': row['JCYW']/row['JPYR'] if row['JPYR'] > 0 else 0, 'ROI': row['JPYRoi']}])], ignore_index=True)
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Jockey'], 'Category': 'Distance', 'Starts': row['JDR'], 'Wins': row['JDW'], 'Win %': row['JDW']/row['JDR'] if row['JDR'] > 0 else 0, 'ROI': row['JDRoi']}])], ignore_index=True)
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': row['Jockey'], 'Category': row['KJS1'], 'Starts': row['KJ1R'], 'Wins': row['KJ1W'], 'Win %': row['KJ1W']/row['KJ1R'] if row['KJ1R'] > 0 else 0, 'ROI': row['KJ1Roi']}])], ignore_index=True)
        
        jt_info = pd.concat([jt_info, pd.DataFrame([{'Race': row['Race'], 'PP': row['PP'], 'T/J': 'Combined', 'Category': 'Meet', 'Starts': row['JwTMR'], 'Wins': row['JwTMW'], 'Win %': row['JwTMW']/row['JwTMR'] if row['JwTMR'] > 0 else 0, 'ROI': row['JwTMRoi']}])], ignore_index=True)
        
        jt_info = jt_info.dropna().reset_index(drop = True)
        jt_info['T/J'] = jt_info['T/J'].str.title()
        jt_info['Wins'] = jt_info['Wins'].apply(lambda x: round(x))
        jt_info['Win %'] = jt_info['Win %'].apply(lambda x: round(x, 2))

    works = pd.DataFrame(columns=['Race', 'PP', 'Work', 'Date', 'Track', 'SubTrack', 'Condition', 'Distance', 'Work Type', 'Time', 'Rank', 'Horses'])
    for index, row in pp.iterrows():
        dates = row[101:112]
        works_ct = sum(1 for x in dates if x is not None and not math.isnan(x))
        for i in range(works_ct):
            new_work = {
                'Race': row[2],
                'PP': row[3],
                'Work': i + 1,
                'Date': row[101 + i],
                'Track': row[125 + i],
                'SubTrack': row[173 + i],
                'Condition': row[149 + i],
                'Distance': row[137 + i],
                'Work Type': row[161 + i],
                'Time': row[113 + i],
                'Rank': row[197 + i],
                'Horses': row[185 + i]
            }

            works = pd.concat([works, pd.DataFrame([new_work])], ignore_index=True)
    works['WorkScore'] = works.apply(lambda row: 100 + 100 * (0.5 - row['Rank']/row['Horses']) * min(row['Horses'] ** 0.5/15, 1), axis=1)
    works['Date'] = pd.to_datetime(works['Date'].astype(str).str[:8], format='%Y%m%d').dt.date
    works['Distance'] = works['Distance'].apply(lambda x: f'{round(x/220,2)} f' if x < 1760 else f'{round(x/1760,2)} M')


    praces = pd.DataFrame()
    for index, row in pp.iterrows():
        dates = row[255:264]
        race_ct = sum(1 for x in dates if x is not None and not math.isnan(x))
        for i in range(race_ct):
            new_race = {
                # DB Info
                'Race': row[2],
                'PP': row[3],
                'Race No': i + 1,
                'Days Since': row[265 + i],

                # Race Info
                'Date': row[255 + i],
                'Track': row[275 + i],
                'Surface': row[325 + i],
                'Distance': row[315 + i],
                'Condition': row[305 + i],

                # Entry Info
                'Race Type': row[535 + i],
                'Race Cat': row[1085 + i],
                'Restrictions': row[1095 + i],
                'Claiming': row[545 + i],
                'Purse': row[555 + i],
                'Starters': row[345 + i],
                'Speed Par': row[1166 + i],

                # Horse Entry Info
                'RPP': row[355 + i],
                'Trainer': row[1055 + i],
                'Jockey': row[1065 + i],
                'Blinkers': row[365 + i],
                'Medication': row[385 + i],
                'Weight': row[505 + i],
                'Odds': row[515 + i],
                'Fav': row[1125 + i], 

                # Horse Finish Info
                'ST': float(re.sub('[^0-9.]', '0', str(row[565 + i]))),
                'STBy': float(re.sub('[^0-9.]', '0', str(row[635 + i]))),
                '1C': float(re.sub('[^0-9.]', '0', str(row[575 + i]))),
                '1CBy': float(re.sub('[^0-9.]', '0', str(row[655 + i]))),
                '2C': float(re.sub('[^0-9.]', '0', str(row[585 + i]))),
                '2CBy': float(re.sub('[^0-9.]', '0', str(row[675 + i]))),
                'STR': float(re.sub('[^0-9.]', '0', str(row[605 + i]))),
                'STRBy': float(re.sub('[^0-9.]', '0', str(row[715 + i]))),
                'FIN': float(re.sub('[^0-9.]', '0', str(row[615 + i]))),
                'FINBy': float(re.sub('[^0-9.]', '0', str(row[735 + i]))),

                # Race Shape Info
                '1cP': row[695 + i],
                '2cP': row[755 + i],

                # Horse Speed Info
                '2fP': row[765 + i],
                '4fP': row[775 + i],
                '6fP': row[785 + i],
                '8fP': row[795 + i],
                '10fP': row[805 + i],
                'LP': row[815 + i],
                'BSpd': row[845 + i],

                # Horse Fractions Info
                'F1': row[985 + i],
                'F2': row[995 + i],
                'F3': row[1005 + i],
                'FT': row[1035 + i],

                # Race Finish Info 
                'Win': row[405 + i],
                'WinBy': row[465 + i],
                'Place': row[415 + i],
                'PlaceBy': row[475 + i],
                'Show': row[425 + i],
                'ShowBy': row[485 + i],

                # Other Horse Info
                'Comment': row[395 + i],
                'Claimed': row[1045 + i],
            }

            praces = pd.concat([praces, pd.DataFrame([new_race])], ignore_index=True)
            praces['Surface'] = praces['Surface'].str.upper()
            praces['FIN'] = praces.apply(lambda row: (row['Starters'] if (isinstance(row['FIN'], str) or (np.isnan(row['FIN Adj']))) else row['FIN Adj']) if isinstance(row['FIN'], str) else row['FIN'], axis=1)
            praces['RaceScore'] = praces.apply(lambda row: 100 + 100 * (0.5 - float(row['FIN'])/row['Starters']) * min(row['Starters'] ** 0.5/5, 1), axis=1)
            praces['Date'] = praces['Date'].apply(
                lambda x: pd.to_datetime(str(int(x)) if isinstance(x, (float,int)) else x, 
                format='%Y%m%d', errors='coerce')).dt.date

    # Initialize a list to store the data
    race_shape_data = []

    calls = ['2fP', '4fP', '6fP', 'LP']

    # Iterate over each race
    for race in praces['Race'].unique():
        race_df = praces[praces['Race'] == race]
        
        # Iterate over each horse
        for horse in race_df['PP'].unique():
            horse_df = race_df[race_df['PP'] == horse]
            
            # Iterate over each call
            for call in calls:
                # Calculate the average position and pace at this call
                avg_pace = horse_df[call].mean()
                
                # Append the data to the list
                race_shape_data.append({'Race': race, 'PP': horse, 'Call': call, 'Avg Pace': avg_pace})

    # Convert the list to a DataFrame
    race_shape = pd.DataFrame(race_shape_data)

    @st.cache_data
    def get_call_data(race_shape, races, race, call):
        # Get the data
        call_data = race_shape[(race_shape['Race'] == race) & (race_shape['Call'] == call)]
        
        # Order call data by average pace
        call_data = call_data.sort_values('Avg Pace', ascending=True).reset_index(drop=True)

        x = call_data.index + 1 
        x_labels = call_data['PP']
        y = call_data['Avg Pace']
        colors_dict = {
            1: "red", 2: "white", 3: "blue", 4: "yellow", 5: "green",
            6: "black", 7: "orange", 8: "pink", 9: "turquoise", 10: "purple",
            11: "grey", 12: "lime", 13: "brown", 14: "maroon", 15: "dimgrey",
            16: "skyblue", 17: "navy", 18: "forestgreen", 19: "cornflowerblue"
        }

        outline_colors_dict = {
            1: "white", 2: "black", 3: "white", 4: "black", 5: "white",
            6: "yellow", 7: "black", 8: "black", 9: "black", 10: "white",
            11: "red", 12: "white", 13: "white", 14: "yellow", 15: "black",
            16: "red", 17: "white", 18: "yellow", 19: "red"
        }

        # Get the race speed par
        race_speed_par = races[(races['Race'] == race)][call].iloc[0]

        # Create a new figure
        fig, ax = plt.subplots(figsize = (10,4))

        # Create a list of colors for the stems
        outline_colors = [outline_colors_dict[i] for i in x_labels]
        colors = [colors_dict[i] for i in x_labels]

        # Create the stem plot with colored stems
        lines = ax.hlines(x, [0]*len(y), y, colors=outline_colors, linewidth=2) 
        lines = ax.hlines(x, [0]*len(y), y, colors=colors, linewidth=1.5) 

        # Add the race speed par as a horizontal line
        ax.axvline(x=race_speed_par, color='r', linestyle='-')

        # Rotate the x-axis labels
        plt.xticks(rotation='vertical')

        # Add numbers at the end of each stem
        for i, value in enumerate(y):
            ax.text(value + 4, x[i], str(x_labels.iloc[i]), ha='right', va='center')

        ax.axis('off')
        plt.savefig('data.png') 

    @st.cache_data
    def get_hs(race, races, horses, is_wet, off_turf, running_horses):
        horse_scores = pd.DataFrame()
        race_row = races.loc[races['Race'] == race].reset_index(drop=True).iloc[0].to_dict()
        race_row['Surface'] = race_row['Surface'].upper()
        if off_turf == True:
            surface = 'D'
        else: 
            surface = race_row['Surface']
        if ((surface == 'D') & (is_wet == True)):
            surf_code = 'W'
        else:
            surf_code = surface

        par2f = race_row['2fP']
        par4f = race_row['4fP']
        par6f = race_row['6fP']
        parLP = race_row['LP']
        parSpd = race_row['SpeedPar']
        if np.isnan(parSpd):
            parSpd = 60
        horses_in_race = horses.loc[horses['Race'] == race]
        horses_in_race = horses_in_race.loc[horses_in_race['PP'].isin(running_horses)]

        for index1, row1 in horses_in_race.iterrows():
            hw = works.loc[(works['Race'] == row1['Race']) & (works['PP'] == row1['PP'])]
            hjt = jt_info.loc[(jt_info['Race'] == row1['Race']) & (jt_info['PP'] == row1['PP'])]
            if surf_code == 'D':
                surfpar = row1['FstSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['FstPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['FstPed']))[0])
                hw = hw.loc[(hw['SubTrack'] == 'MT') & (hw['Condition'].isin(['ft', 'gd']))].reset_index(drop=True)
            elif surf_code == 'T':
                surfpar = row1['TrfSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['TrfPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['TrfPed']))[0])
                hw = hw.loc[hw['SubTrack'] == 'TT'].reset_index(drop=True)
            elif surf_code == 'W':
                surfpar = row1['WetSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['WetPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['WetPed']))[0])
                hw = hw.loc[(hw['SubTrack'] == 'MT') & (hw['Condition'].isin(['my', 'sy']))].reset_index(drop=True)
            else:
                surfpar = np.nan
                surfped = np.nan

            hw['Work'] = range(1, len(hw['Work'])+1)

            distpar = 0 if np.isnan(row1['DistSpdB']/parSpd) else row1['DistSpdB']/parSpd
            distped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['DistPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['DistPed']))[0])
            ltpar = 0 if np.isnan(row1['LTSpdB']/parSpd) else row1['LTSpdB']/parSpd
            cypar = 0 if np.isnan(row1['CYSpdB']/parSpd) else row1['CYSpdB']/parSpd
            pypar = 0 if np.isnan(row1['PYSpdB']/parSpd) else row1['PYSpdB']/parSpd
            trackpar = 0 if np.isnan(row1['TrkSpdB']/parSpd) else row1['TrkSpdB']/parSpd
            try:
                parscore = (surfpar * 3 + distpar * 3 + cypar * 2 + pypar + trackpar * 2) / (np.sum(3 if surfpar > 0 else 0) + np.sum(3 if distpar > 0 else 0) + np.sum(2 if cypar  > 0 else 0) + np.sum(1 if pypar  > 0 else 0)+ np.sum(2 if trackpar > 0 else 0))
            except:
                parscore = np.nan
            try:
                pedscore = (surfped + distped) / (np.sum(1 if surfped > 0 else 0) + np.sum(1 if distped > 0 else 0))
            except:
                pedscore = np.nan
            hjt['Score'] = hjt.apply(lambda row: 100 + 100 * ((row['ROI'] + 0.36)/2) * min((row['Starts'] ** 0.5)/20, 1), axis = 1)
            tscore = hjt.loc[(hjt['T/J'] == row1['Trainer']) | (hjt['T/J'] == 'Combined')]['Score'].mean()
            jscore = hjt.loc[(hjt['T/J'] == row1['Jockey']) | (hjt['T/J'] == 'Combined')]['Score'].mean()

            works1 = hw.loc[hw['Work'] <= 3]['WorkScore'].max()
            works3 = hw.loc[hw['Work'] <= 3]['WorkScore'].mean()
            works5 = hw.loc[hw['Work'] <= 5]['WorkScore'].mean()
            workscore = (works1 + works3 + works5)/3
            hr = praces.loc[(praces['Race'] == row1['Race']) & (praces['PP'] == row1['PP'])]
            cl1 = hr.loc[hr['Race No'] <= 1]['Speed Par'].max()
            cl3 = hr.loc[hr['Race No'] <= 3]['Speed Par'].mean()
            cl5 = hr.loc[hr['Race No'] <= 5]['Speed Par'].mean()
            classscore = (cl1 + cl3 + cl5)/3
            chr = hr.loc[(hr['BSpd'] > 40) & (hr['Date'] >= date.today() - timedelta(days=180))]
            chr['Race No'] = list(range(len(chr)))
            chr['Race No'] = chr['Race No'] + 1
            races1 = chr.loc[chr['Race No'] <= 1]['RaceScore'].max()
            races3 = chr.loc[chr['Race No'] <= 3]['RaceScore'].mean()
            races5 = chr.loc[chr['Race No'] <= 5]['RaceScore'].mean()
            racescore = (races1 + races3 + races5)/3
            bspd1 = chr.loc[chr['Race No'] <= 1]['BSpd'].max()
            bspd3 = chr.loc[chr['Race No'] <= 3]['BSpd'].mean()
            bspd5 = chr.loc[chr['Race No'] <= 5]['BSpd'].mean()
            bspdscore = ((bspd1 + bspd3 + bspd5)/3)/parSpd
            f21 = chr.loc[chr['Race No'] <= 3]['2fP'].max()
            f23 = chr.loc[chr['Race No'] <= 3]['2fP'].mean()
            f25 = chr.loc[chr['Race No'] <= 5]['2fP'].mean()
            if par2f != np.nan:
                f2score = ((f21 + f23 + f25)/3)/par2f
            else:
                f2score = np.nan
            f41 = chr.loc[chr['Race No'] <= 3]['4fP'].max()
            f43 = chr.loc[chr['Race No'] <= 3]['4fP'].mean()
            f45 = chr.loc[chr['Race No'] <= 5]['4fP'].mean()
            if par4f != np.nan:
                f4score = ((f41 + f43 + f45)/3)/par4f
            else:
                f4score = np.nan
            f61 = chr.loc[chr['Race No'] <= 3]['6fP'].max()
            f63 = chr.loc[chr['Race No'] <= 3]['6fP'].mean()
            f65 = chr.loc[chr['Race No'] <= 5]['6fP'].mean()
            if par6f != np.nan:
                f6score = ((f61 + f63 + f65)/3)/par6f
            else:
                f6score = np.nan

            ep_figs = np.array([f2score,f4score,f6score])
            lp1 = chr.loc[chr['Race No'] <= 3]['LP'].max()
            lp3 = chr.loc[chr['Race No'] <= 3]['LP'].mean()
            lp5 = chr.loc[chr['Race No'] <= 5]['LP'].mean()
            if parLP != np.nan:
                lpscore = ((lp1 + lp3 + lp5)/3)/parLP
            else:
                lpscore = np.nan
            new_horse_score = {
                'Race': race,
                'Horse': row1['Name'],
                'PP': row1['PP'],
                'ML': row1['ML'],
                'Style': row1['Style'],
                'PowerScore': row1['PrimePower'],
                'ParScore': parscore,
                'Par': parscore * parSpd,
                'PedScore': pedscore,
                'Ped': pedscore,
                'TScore': tscore,
                'JScore': jscore,
                'WorksScore': workscore,
                'ClassScore': classscore,
                'RaceScore': racescore,
                'BSpeedScore': bspdscore,
                'BSpeed': bspdscore * parSpd,
                'EPScore': ep_figs[~np.isnan(ep_figs)].mean(),
                'EP': ep_figs[~np.isnan(ep_figs)].mean() * np.nanmean(np.array([par2f,par4f,par6f])),
                'LPScore': lpscore,
                'LP': lpscore * parLP
            }

            horse_scores = pd.concat([horse_scores, pd.DataFrame([new_horse_score])], ignore_index=True)
        return horse_scores

    @st.cache_data
    def get_fs(horse_scores, race):
        race_scores = horse_scores[horse_scores['Race'] == race]
        race_constants = race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'PowerScore', 'Par', 'Ped', 'TScore', 'JScore', 'WorksScore', 'ClassScore', 'RaceScore', 'BSpeed', 'EP', 'LP']]
        race_scores = race_scores[['PowerScore', 'ParScore','PedScore', 'TScore', 'JScore', 'WorksScore', 'ClassScore', 
        'RaceScore', 'BSpeedScore', 'EPScore', 'LPScore']]
        # calculate z scores for all race_score columns
        race_scores = race_scores.apply(lambda x: (x - x.mean()) / x.std(), axis=0)
        # Calculate weighted mean
        race_scores = race_scores.fillna(0)
        race_scores['Final Score'] = (race_scores['ParScore'] * 3 + race_scores['TScore'] * 2 + race_scores['BSpeedScore'] * 3 + race_scores['LPScore'] * 2 + race_scores['PedScore'] * 2 + race_scores.drop(['ParScore', 'PedScore', 'TScore', 'BSpeedScore', 'LPScore'], axis=1).mean(axis=1, skipna=True)) / 12
        race_scores['Final Score'] = race_scores.mean(axis=1, skipna=True)

        race_scores['Odds'] = race_scores.apply(lambda x: 0.5 + stats.norm.cdf(x['Final Score']), axis=1)
        race_scores['Odds'] = race_scores['Odds'] ** 7
        total_odds = race_scores['Odds'].sum()
        race_scores['Odds'] = 1/(race_scores['Odds']/total_odds) - 1
        race_scores['Odds'] = race_scores['Odds'].clip(upper = 75, axis=0)


        race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'PowerScore', 'Par', 'Ped', 'TScore', 'JScore', 'WorksScore', 'ClassScore', 'RaceScore','BSpeed', 'EP', 'LP']] = race_constants
        race_scores['Value'] = ((race_scores['ML']) * (1/(race_scores['Odds'] + 1))) - (1 - (1/(race_scores['Odds'] +1)))
        final_scores = race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'Par', 'Ped', 'TScore', 'JScore', 'WorksScore', 'ClassScore', 'RaceScore', 'BSpeed', 'EP', 'LP', 'Final Score', 'Odds', 'Value']].sort_values(by = 'Value', ascending = False)

        return final_scores

    @st.cache_data
    def get_data(dataframe):
        return dataframe
        
    def highlight_cells_condition(row):
        background_colors = {
            1: "red", 2: "white", 3: "blue", 4: "yellow", 5: "green",
            6: "black", 7: "orange", 8: "pink", 9: "turquoise", 10: "purple",
            11: "grey", 12: "lime", 13: "brown", 14: "maroon", 15: "dimgrey",
            16: "skyblue", 17: "navy", 18: "forestgreen", 19: "cornflowerblue"
        }

        text_colors = {
            1: "white", 2: "black", 3: "white", 4: "black", 5: "white",
            6: "yellow", 7: "black", 8: "black", 9: "black", 10: "white",
            11: "red", 12: "white", 13: "white", 14: "yellow", 15: "black",
            16: "red", 17: "white", 18: "yellow", 19: "red"
        }
        
        background_color = background_colors.get(row["PP"], 'fuchsia')
        text_color = text_colors.get(row["PP"], 'yellow')
        return [f"background-color: {background_color}; color: {text_color}" for _ in row]

    
    # Load and prepare data

    rdf = get_data(races)

    # Format dates
    rdf['Date'] = pd.to_datetime(rdf['Date'], format='%Y%m%d').dt.date
    #pdf['Date'] = pd.to_datetime(pdf['Date'], format='%Y%m%d').dt.date
    #wdf['Date'] = pd.to_datetime(wdf['Date'].astype(str).str[:8], format='%Y%m%d').dt.date
    
    # Sidebar inputs
    races = rdf['Race'].drop_duplicates()
    show_options = ['Yes', 'No']
    show_options_rev = ['No', 'Yes']
    race_choice = st.sidebar.selectbox('Select your race', races)
    overview_show = st.sidebar.selectbox('Show Overviews?', show_options)
    pp_show = st.sidebar.selectbox('Show PPs?', show_options)
    works_show = st.sidebar.selectbox('Show Works?', show_options_rev)
    tj_show = st.sidebar.selectbox('Show T/J Stats?', show_options)
    is_wet = st.sidebar.checkbox("Wet?")
    off_turf = st.sidebar.checkbox("Off Turf?") if rdf[rdf['Race'] == race_choice]['Surface'].iloc[0] == 'T' else False

    hdf = get_data(horses)
    possible_horses = hdf[hdf['Race'] == race_choice]['PP'].unique()
    running_horses = st.sidebar.multiselect("What horses are in the race?", possible_horses, default=possible_horses)
    hdf = hdf[hdf['PP'].isin(running_horses)]
    pdf = get_data(praces)[['Race', 'PP', 'Date', 'Track', 'Condition', 'Distance', 'Surface', 
                           '1cP', '2cP', 'Race Type', 'Speed Par',  'BSpd',  'Starters', 
                            '1C', '2C', 'STR', 'FIN', 'FINBy',
                           '2fP','4fP','6fP','LP','Comment', 'RaceScore',  'Jockey', 'Odds']]
    pdf = pdf[pdf['PP'].isin(running_horses)]
    pdf['Distance'] = pdf['Distance'].apply(lambda x: f'{round(x/220,2)} f' if x < 1760 else f'{round(x/1760,2)} M')
    rsdf = get_data(race_shape)
    rsdf = rsdf[rsdf['PP'].isin(running_horses)]
    wdf = get_data(works)
    wdf = wdf[wdf['PP'].isin(running_horses)]
    tjdf = get_data(jt_info)
    tjdf = tjdf[tjdf['PP'].isin(running_horses)]
    

    
    # Main logic
    horse_scores = get_hs(race_choice, rdf, hdf, is_wet, off_turf, running_horses)
    df = get_fs(horse_scores, race_choice)
    
    # Display Race Overview
    st.write('Race Overview')
    st.dataframe(rdf[rdf['Race'] == race_choice], hide_index=True)
    
    # Dataframe Styling
    cmap = plt.get_cmap('Reds')
    reversed_cmap = plt.get_cmap('Reds_r')
    df = df[df['Race'] == race_choice]
    df.columns = ['Race', 'Horse', 'PP', 'ML', 'Style', 'Par', 'Pedigree', 'Trainer', 'Jockey', 'Works', 'Class', 'Results', 'Speed', 'EP', 'LP', 'Final Score', 'Odds', 'Value']
    standard_columns = ['Par', 'Pedigree', 'Trainer', 'Jockey', 'Works', 'Class', 'Results', 'Speed', 'EP', 'LP', 'Final Score', 'Value']
    reversed_columns = ['ML', 'Odds']
    styled_df = df.style \
        .background_gradient(cmap=cmap, subset=standard_columns) \
        .background_gradient(cmap=reversed_cmap, subset=reversed_columns) \
        .format('{:.2f}', subset=['ML',  'Par', 'Pedigree', 'Trainer', 'Jockey', 'Works', 'Class', 'Results', 'Speed', 'EP', 'LP', 'Final Score', 'Odds', 'Value']) \
        .apply(highlight_cells_condition, subset=['PP'], axis = 1)
    
    
    st.dataframe(styled_df, hide_index=True)

    st.write('Race Shape')
    call = st.selectbox('Race Shape at Call', ['2fP', '4fP', '6fP', 'LP'])
    get_call_data(rsdf, rdf, race_choice, call)
    st.image('data.png')
    

    horse_options = hdf[hdf['Race'] == race_choice]['PP'].unique()

    def color_negative_red(series):
        # make a darker color for lower negative values and lighter color for lower positive values
        color = series.apply(lambda val: 'rgba(0,0,0,0)' if np.isnan(val) else f'rgba(0, 0, 255, {abs(val/50)})' if val < 0 else f'rgba(255, 0, 0, {abs(val/50)})')
        return [f"background-color: {color_val}" for color_val in color]

    def color_finish(series):
        # make a darker color for lower negative values and lighter color for lower positive values
        color = series.apply(lambda val: 'yellow' if val == 1 else 'silver' if val == 2 else 'peru' if val == 3 else 'white')
        return [f"background-color: {color_val}" for color_val in color]
    
    def color_bspd(series):
        speedpar = rdf[rdf['Race'] == race_choice]['SpeedPar'].iloc[0]

        color = series.apply(lambda val: 'rgba(0,0,0,0)' if np.isnan(val) else f"rgba(255, 0, 0, {(20 - (speedpar - val))/50})" 
                        if val < speedpar else f"rgba(255, 0, 0, 0.8)")
        return [f"background-color: {color_val}" for color_val in color]

    def color_2fP(series):
        speedpar = rdf[rdf['Race'] == race_choice]['2fP'].iloc[0]
        # check if speedpar is null
        color = series.apply(lambda val: f"rgba(0,0,0,0)" if (np.isnan(speedpar) or np.isnan(val)) else f"rgba(255, 0, 0, {(20 - (speedpar - val))/50})" 
                        if val < speedpar else f"rgba(255, 0, 0, 0.8)")
        return [f"background-color: {color_val}" for color_val in color]

    def color_4fP(series):
        speedpar = rdf[rdf['Race'] == race_choice]['4fP'].iloc[0]
        # check if speedpar is null
        color = series.apply(lambda val: f"rgba(0,0,0,0)" if (np.isnan(speedpar) or np.isnan(val)) else f"rgba(255, 0, 0, {(20 - (speedpar - val))/50})" 
                        if val < speedpar else f"rgba(255, 0, 0, 0.8)")
        return [f"background-color: {color_val}" for color_val in color]

    def color_6fP(series):
        speedpar = rdf[rdf['Race'] == race_choice]['6fP'].iloc[0]
        # check if speedpar is null
        color = series.apply(lambda val: f"rgba(0,0,0,0)" if (np.isnan(speedpar) or np.isnan(val)) else f"rgba(255, 0, 0, {(20 - (speedpar - val))/50})" 
                        if val < speedpar else f"rgba(255, 0, 0, 0.8)")
        return [f"background-color: {color_val}" for color_val in color]

    def color_LP(series):
        speedpar = rdf[rdf['Race'] == race_choice]['LP'].iloc[0]
        # check if speedpar is null
        color = series.apply(lambda val: f"rgba(0,0,0,0)" if (np.isnan(speedpar) or np.isnan(val)) else f"rgba(255, 0, 0, {(20 - (speedpar - val))/50})" 
                        if val < speedpar else f"rgba(255, 0, 0, 0.8)")
        return [f"background-color: {color_val}" for color_val in color]

    
    for horse in horse_options:
        horse_data = hdf[(hdf['Race'] == race_choice) & (hdf['PP'] == horse)].reset_index(drop=True)
        horse_name = horse_data['Name'][0].title()
        if overview_show == 'Yes':
            st.write(f'{horse_name} Overview:')
            st.dataframe(df[(df['Race'] == race_choice) & (df['PP'] == horse)], hide_index = True)
        if pp_show == 'Yes':
            st.write(f'{horse_name} PPs:')
            pdfh = pdf[(pdf['Race'] == race_choice) & (pdf['PP'] == horse)]
            pdfh = pdfh[['Date', 'Track', 'Condition', 'Distance', 'Surface', 
                           '1cP', '2cP', 'Race Type', 'Speed Par',  'BSpd', 'Odds',  'Starters', 
                            '1C', '2C', 'STR', 'FIN', 'FINBy',
                           '2fP','4fP','6fP','LP','Comment']]
            pdfh = pdfh.style \
                .apply(color_negative_red, subset=['1cP', '2cP'], axis = 1) \
                .apply(color_bspd, subset=['BSpd'], axis = 1) \
                .apply(color_2fP, subset=['2fP'], axis = 1) \
                .apply(color_4fP, subset=['4fP'], axis = 1) \
                .apply(color_6fP, subset=['6fP'], axis = 1) \
                .apply(color_LP, subset=['LP'], axis = 1) \
                .apply(color_finish, subset=['FIN'], axis = 1) \
                .format('{:.1f}', subset=['Odds']) \
                .format('{:.0f}', subset=['1cP', '2cP', 'BSpd', '1cP', '2cP', 'Speed Par','Starters', 
                            '1C', '2C', 'STR', 'FIN', 'FINBy','2fP','4fP','6fP','LP'])
            
            st.dataframe(pdfh, hide_index = True)
        if works_show == 'Yes': 
            st.write(f'{horse_name} Works:')
            st.dataframe(wdf[(wdf['Race'] == race_choice) & (wdf['PP'] == horse)], hide_index = True)
        if tj_show == 'Yes': 
            st.write(f'{horse_name} T/J Stats:')
            st.dataframe(tjdf[(tjdf['Race'] == race_choice) & (tjdf['PP'] == horse)], hide_index = True)


