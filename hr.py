import matplotlib.pyplot as plt
import matplotlib.cm as cm
import streamlit as st
import pandas as pd
import numpy as np

import re
import math

st.set_page_config(page_title='Race Info', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    pp = pd.read_csv(uploaded_file, header=None)

    races = pp[[0, 1, 2, 5, 6, 8, 9, 22, 12, 11, 213, 214, 215, 217, 216]]
    races.columns = ['Track', 'Date', 'Race', 'Distance', 'Surface', 'Type', 'Restrictions', 'Breed Type', 'Claiming', 'Purse', '2fP', '4fP', '6fP', 'LP', 'SpeedPar']
    races['Surface'] = races['Surface'].str.upper()
    races = races.drop_duplicates().reset_index(drop = True)

    horses = pp[[2, 3, 44, 43, 209, 210, 250, 1177, 1178, 1179, 1180, 1327, 1328, 1329, 1330, 1263, 1264, 1265, 1266, 45, 48, 61, 50, 61, 63, 223, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 230, 231, 232, 233, 234, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 
                96, 97, 98, 99, 100, 27, 28, 29, 30, 31, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 32, 34, 35, 36, 37, 1156, 1157, 1158, 1159, 1160 ,1161, 1162, 1163, 1164, 1165, 1367, 1368, 1369, 1370, 1371, 218, 219, 220, 221, 222, 1412, 1413, 1414, 1415, 1416]]
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
                    'JwTR', 'JwTW', 'JwTP', 'JwTS', 'JwTRoi', 'JwTMR', 'JwTMW', 'JwTMP', 'JwTMS', 'JwTMRoi']


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
                'ST': row[565 + i],
                'STBy': row[635 + i],
                '1C': row[575 + i],
                '1CBy': row[655 + i],
                '2C': row[585 + i],
                '2CBy': row[675 + i],
                'STR': row[605 + i],
                'STRBy': row[715 + i],
                'FIN': row[615 + i],
                'FINBy': row[735 + i],
                'FIN Adj': row[635 + i],

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
                'Spd': row[855 + i],

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

    def get_hs(race, races, horses, is_wet, off_turf, running_horses):
        horse_scores = pd.DataFrame()
        work_scores = pd.DataFrame()
        race_scores = pd.DataFrame()

        race_row = dict(races[races['Race'] == race].reset_index(drop = True))
        race_row['Surface'] = race_row['Surface'].str.upper()
        if off_turf == True:
            surface = 'D'
        else: 
            surface = race_row['Surface'][0]

        if ((surface == 'D') & (is_wet == True)):
            surf_code = 'W'
        else:
            surf_code = surface

        
        par2f = race_row['2fP'][0]
        par4f = race_row['4fP'][0]
        par6f = race_row['6fP'][0]
        parLP = race_row['LP'][0]
        parSpd = race_row['SpeedPar'][0]
        if np.isnan(parSpd):
            parSpd = 60
        horses_in_race = horses[horses['Race'] == race]
        horses_in_race = horses_in_race[horses_in_race['PP'].isin(running_horses)]
        
        for index1, row1 in horses_in_race.iterrows():
            hw = works[(works['Race'] == row1['Race']) & (works['PP'] == row1['PP'])]
            if surf_code == 'D':
                surfpar = row1['FstSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['FstPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['FstPed']))[0])
                hw = hw[(hw['SubTrack'] == 'MT') & (hw['Condition'].isin(['ft', 'gd']))].reset_index(drop = True)
            elif surf_code == 'T':
                surfpar = row1['TrfSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['TrfPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['TrfPed']))[0])
                hw = hw[hw['SubTrack'] == 'TT'].reset_index(drop = True)
            elif surf_code == 'W':
                surfpar = row1['WetSpdB']/parSpd
                surfped = np.nan if len(re.findall('\d+\.\d+|\d+', str(row1['WetPed']))) == 0 else int(re.findall('\d+\.\d+|\d+', str(row1['WetPed']))[0])
                hw = hw[(hw['SubTrack'] == 'MT') & (hw['Condition'].isin(['my', 'sy']))].reset_index(drop = True)
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

            jcys = 100 + 100 * ((row1['TCYRoi'] + 0.18)/2) * min((row1['TCYR'] ** 0.5)/20, 1)
            jpys = 100 + 100 * ((row1['TPYRoi'] + 0.18)/2) * min((row1['TPYR'] ** 0.5)/20, 1)
            jwts = 100 + 100 * ((row1['JwTRoi'] + 0.18)/2) * min((row1['JwTR'] ** 0.5)/20, 1)
            jcys = 100 + 100 * ((row1['JCYRoi'] + 0.18)/2) * min((row1['JCYR'] ** 0.5)/20, 1)
            jcys = 100 + 100 * ((row1['JPYRoi'] + 0.18)/2) * min((row1['JPYR'] ** 0.5)/20, 1)
            jds = 100 + 100 * ((row1['JDRoi'] + 0.18)/2) * min((row1['JDR'] ** 0.5)/20, 1)

            jtscore = (jcys + jpys + jwts + jcys + jpys + jds)/6


            works1 = hw[hw['Work'] <= 1]['WorkScore'].mean()
            works3 = hw[hw['Work'] <= 3]['WorkScore'].mean()
            works5 = hw[hw['Work'] <= 5]['WorkScore'].mean()
            workscore = (works1 + works3 + works5)/3

            hr = praces[(praces['Race'] == row1['Race']) & (praces['PP'] == row1['PP'])]
            cl1 = hr[hr['Race No'] <= 1]['Speed Par'].mean()
            cl3 = hr[hr['Race No'] <= 3]['Speed Par'].mean()
            cl5 = hr[hr['Race No'] <= 5]['Speed Par'].mean()
            classscore = (cl1 + cl3 + cl5)/3

            chr = hr[(hr['BSpd'] > 40) & (hr['Surface'].str.upper() == surface.upper())]
            chr['Race No'] = list(range(len(chr)))
            chr['Race No'] = chr['Race No'] + 1

            races1 = chr[chr['Race No'] <= 1]['RaceScore'].mean()
            races3 = chr[chr['Race No'] <= 3]['RaceScore'].mean()
            races5 = chr[chr['Race No'] <= 5]['RaceScore'].mean()
            racescore = (races1 + races3 + races5)/3


            spd1 = chr[chr['Race No'] <= 1]['Spd'].mean()
            spd3 = chr[chr['Race No'] <= 3]['Spd'].mean()
            spd5 = chr[chr['Race No'] <= 5]['Spd'].mean()
            spdscore = (spd1 + spd3 + spd5)/3

            bspd1 = chr[chr['Race No'] <= 1]['BSpd'].mean()
            bspd3 = chr[chr['Race No'] <= 3]['BSpd'].mean()
            bspd5 = chr[chr['Race No'] <= 5]['BSpd'].mean()
            bspdscore = ((bspd1 + bspd3 + bspd5)/3)/parSpd

            f21 = chr[chr['Race No'] <= 1]['2fP'].mean()
            f23 = chr[chr['Race No'] <= 3]['2fP'].mean()
            f25 = chr[chr['Race No'] <= 5]['2fP'].mean()
            if par2f != np.nan:
                f2score = ((f21 + f23 + f25)/3)/par2f
            else:
                f2score = np.nan

            f41 = chr[chr['Race No'] <= 1]['4fP'].mean()
            f43 = chr[chr['Race No'] <= 3]['4fP'].mean()
            f45 = chr[chr['Race No'] <= 5]['4fP'].mean()
            if par4f != np.nan:
                f4score = ((f41 + f43 + f45)/3)/par4f
            else:
                f4score = np.nan

            f61 = chr[chr['Race No'] <= 1]['6fP'].mean()
            f63 = chr[chr['Race No'] <= 3]['6fP'].mean()
            f65 = chr[chr['Race No'] <= 5]['6fP'].mean()
            if par6f != np.nan:
                f6score = ((f61 + f63 + f65)/3)/par6f
            else:
                f6score = np.nan
            
            ep_figs = np.array([f2score,f4score,f6score])

            lp1 = chr[chr['Race No'] <= 1]['LP'].mean()
            lp3 = chr[chr['Race No'] <= 3]['LP'].mean()
            lp5 = chr[chr['Race No'] <= 5]['LP'].mean()
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
                'PowerScore': round(row1['PrimePower'], 1),
                'ParScore': round(parscore,1),
                'Par': round(parscore * parSpd, 1),
                'PedScore': round(pedscore, 1),
                'Ped': round(pedscore, 1),
                'JTScore': round(jtscore,1),
                'WorksScore': round(workscore,1),
                'ClassScore': round(classscore,1),
                'RaceScore': round(racescore, 1),
                'SpeedScore': round(spdscore,1),
                'Speed': round(spdscore, 1),
                'BSpeedScore': round(bspdscore,1),
                'BSpeed': round(bspdscore * parSpd,1),
                'EPScore': round(ep_figs[~np.isnan(ep_figs)].mean(),1),
                'EP': round(ep_figs[~np.isnan(ep_figs)].mean() * np.nanmean(np.array([par2f,par4f,par6f])),1),
                'LPScore': round(lpscore,1),
                'LP': round(lpscore * parLP,1)
            }

            horse_scores = pd.concat([horse_scores, pd.DataFrame([new_horse_score])], ignore_index=True)
        return horse_scores

    def get_fs(horse_scores, race):
        race_scores = horse_scores[horse_scores['Race'] == race]
        race_constants = race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'PowerScore', 'Par', 'Ped', 'JTScore', 'WorksScore', 'ClassScore', 'RaceScore', 'Speed', 'BSpeed', 'EP', 'LP']]

        race_scores = race_scores[['PowerScore', 'ParScore', 'ParScore','ParScore','PedScore', 'JTScore', 'WorksScore', 'ClassScore', 
        'RaceScore', 'RaceScore', 'RaceScore', 'SpeedScore', 'BSpeedScore', 'BSpeedScore', 'BSpeedScore', 'EPScore', 'EPScore', 'LPScore', 'LPScore']]
        
        # Calculate column averages
        column_means = race_scores.mean()

        # Divide each column by its average
        race_scores = race_scores.apply(lambda x: x / column_means, axis=1)
        average_score_per_row = race_scores.mean(axis=1, skipna=True)
        race_scores['Final Score'] = average_score_per_row
        race_scores = race_scores.loc[:,~race_scores.columns.duplicated()].copy()

        race_scores['Odds'] = race_scores['Final Score'] ** 20
        total_odds = race_scores['Odds'].sum()
        race_scores['Odds'] = 1/(race_scores['Odds']/total_odds) - 1
        race_scores['Odds'] = race_scores['Odds'].clip(upper = 75, axis=0)


        race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'PowerScore', 'Par', 'Ped', 'JTScore', 'WorksScore', 'ClassScore', 'RaceScore', 'Speed', 'BSpeed', 'EP', 'LP']] = race_constants
        race_scores['Value'] = ((race_scores['ML']) * (1/(race_scores['Odds'] + 1))) - (1 - (1/(race_scores['Odds'] +1)))
        final_scores = race_scores[['Race', 'Horse', 'PP', 'ML', 'Style', 'PowerScore', 'Par', 'Ped', 'JTScore', 'WorksScore', 'ClassScore', 'RaceScore', 'Speed', 'BSpeed', 'EP', 'LP', 'Final Score', 'Odds', 'Value']].sort_values(by = 'Value', ascending = False)

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
    hdf = get_data(horses)
    rdf = get_data(races)
    pdf = get_data(praces)[['Race', 'PP', 'Days Since', 'Date', 'Track', 'Surface', 'Distance', 'Condition',
                           'Race Type', 'Speed Par', 'Odds', 'FIN', '2fP','4fP','6fP','LP','BSpd','Spd','Comment', 'RaceScore']]
    wdf = get_data(works)
    
    # Format dates
    rdf['Date'] = pd.to_datetime(rdf['Date'], format='%Y%m%d').dt.date
    pdf['Date'] = pd.to_datetime(pdf['Date'], format='%Y%m%d').dt.date
    wdf['Date'] = pd.to_datetime(wdf['Date'].astype(str), format='%Y%m%d').dt.date
    
    # Sidebar inputs
    races = rdf['Race'].drop_duplicates()
    show_options = ['Yes', 'No']
    race_choice = st.sidebar.selectbox('Select your race', races)
    overview_show = st.sidebar.selectbox('Show Overviews?', show_options)
    pp_show = st.sidebar.selectbox('Show PPs?', show_options)
    works_show = st.sidebar.selectbox('Show Works?', show_options)
    is_wet = st.sidebar.checkbox("Wet?")
    off_turf = st.sidebar.checkbox("Off Turf?") if rdf[rdf['Race'] == race_choice]['Surface'].iloc[0] == 'T' else False
    possible_horses = hdf[hdf['Race'] == race_choice]['PP'].unique()
    running_horses = st.sidebar.multiselect("What horses are in the race?", possible_horses, default=possible_horses)
    
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
    standard_columns = ['PowerScore', 'Par', 'Ped', 'JTScore', 'WorksScore', 'ClassScore', 'RaceScore', 'Speed', 'BSpeed', 'EP', 'LP', 'Final Score', 'Value']
    reversed_columns = ['ML', 'Odds']
    styled_df = df.style \
        .background_gradient(cmap=cmap, subset=standard_columns) \
        .background_gradient(cmap=reversed_cmap, subset=reversed_columns) \
        .format('{:.2f}', subset=['ML', 'PowerScore', 'Par', 'Ped', 'JTScore', 'WorksScore', 'ClassScore', 'RaceScore', 'Speed', 'BSpeed', 'EP', 'LP', 'Final Score', 'Odds', 'Value']) \
        .apply(highlight_cells_condition, subset=['PP'], axis = 1)
    
    st.dataframe(styled_df, hide_index=True)

    

    horse_options = hdf[hdf['Race'] == race_choice]['PP'].unique()


    for horse in horse_options:
        horse_data = hdf[(hdf['Race'] == race_choice) & (hdf['PP'] == horse)].reset_index(drop=True)
        horse_name = horse_data['Name'][0].title()
        if overview_show == 'Yes':
            st.write(f'{horse_name} Overview:')
            st.dataframe(df[(df['Race'] == race_choice) & (df['PP'] == horse)], hide_index = True)
        if pp_show == 'Yes':
            st.write(f'{horse_name} PPs:')
            st.dataframe(pdf[(pdf['Race'] == race_choice) & (pdf['PP'] == horse)], hide_index = True)
        if works_show == 'Yes': 
            st.write(f'{horse_name} Works:')
            st.dataframe(wdf[(wdf['Race'] == race_choice) & (wdf['PP'] == horse)], hide_index = True)
