import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import collections as cl
from scipy import stats

#This function is for reading the three excel files
def Load_data(x):
    return pd.read_csv(x)
File = "C:/Users/96279/Downloads/Players_WorldCup_Wins.csv"
File1 = "C:/Users/96279/Downloads/WorldCupMatches.csv"
File2 = "C:/Users/96279/Downloads/RecentProfessionalPlayers.csv"
wins = Load_data(File)
matches = Load_data(File1)
recent = Load_data(File2)

#This code is to show the number of columns and rows each data set has
print("Shape")
print("df_matches",matches.shape,"df_recent",recent.shape,"df_wins",wins.shape)

#This function is for giving general information about each dataset
def Tabulation(x):
    table = pd.DataFrame(x.dtypes,columns=['dtypes'])
    table1 =pd.DataFrame(x.columns,columns=['Names'])
    table = table.reset_index()
    table= table.rename(columns={'index':'Name'})
    table['No of Missing'] = x.isnull().sum().values
    table['No of Uniques'] = x.nunique().values
    table['Percent of Missing'] = ((x.isnull().sum().values)/ (x.shape[0])) *100
    table['First Observation'] = x.loc[0].values
    table['Second Observation'] = x.loc[1].values
    table['Third Observation'] = x.loc[2].values
    for name in table['Name'].value_counts().index:
        table.loc[table['Name'] == name, 'Entropy'] = round(stats.entropy(x[name].value_counts(normalize=True), base=2),2)
    print(table)
Tabulation(matches)
Tabulation(recent)
Tabulation(wins)

#code 1:
#This figure shows average attendance per year
att1 = matches.groupby("Year")["Attendance"].sum().reset_index()
att1["Year"] = att1["Year"].astype(int)
plt.figure(figsize=(12,7))
ax = sns.pointplot(att1["Year"],att1["Attendance"],color="k")
ax.set_facecolor("w")
plt.grid()
plt.title("Average attendance by year")
plt.show()

#code 2:
#This figure shows the total goals scored in each year
goals = matches.groupby("Year")["Home Team Goals","Away Team Goals"].sum().reset_index()
goals.drop('Year',inplace=True, axis=1)
goals["sum"]=goals.sum(axis=1)
plt.figure(figsize=(12,7))
sns.barplot(att1["Year"],goals["sum"],linewidth=1)
plt.grid(True)
plt.title("Goals in each year")
plt.show()

#code 3:
#This figure show the top 20 countries that hosted the world cup games(1930-2014)
mat_c = matches["City"].value_counts().reset_index()
plt.figure(figsize=(10,8))
ax = sns.barplot(y=mat_c["index"][:20],x = mat_c["City"][:20],palette="gist_earth",linewidth=1)
plt.xlabel("number of matches")
plt.ylabel("City")
plt.grid(True)
plt.title("Top 20 Cities with maximum world cup matches")
for i,j in enumerate("Matches  :" + mat_c["City"][:20].astype(str)):
    ax.text(.7,i,j,fontsize = 13,color="w")
plt.show()

#code 4:
#This figure shows the nationalities distribution in Real Madrid
rec_player = recent[recent.Club == 'Real Madrid']
p=rec_player.groupby(['Nationality'], as_index = False).count()
fig, ax = plt.subplots()
ax.bar(p.Nationality, p.Name,label=p.Nationality)
plt.xticks(fontsize=7)
ax.set_title('Nationalities numbers in Real Madrid')
plt.show()

#code 5:
#This figure is To show the number of players that have the same club position
p=recent.groupby(['Club_Position'], as_index = False).count()
fig, ax = plt.subplots()
plt.xticks(fontsize=5)
ax.bar(p.Club_Position,p.Name,label=p.Club_Position)
ax.set_title('Club position')
plt.show()

#code 6:
#This figure shows how many times each country won the world cup
final = matches[matches.Stage == 'Final']
c=matches.loc[[74]]
final=final.append(c)
final=final.sort_values('Year')
final["winner"]=''
winner=final["winner"].tolist()
home=final['Home Team Goals'].tolist()
away=final['Away Team Goals'].tolist()
home_c=final['Home Team Name'].tolist()
away_c=final['Away Team Name'].tolist()
a=[]
final["Win conditions"].fillna("", inplace = True)
tie=final['Win conditions'].tolist()
for i in range(0,len(tie)):
    if tie[i]=="":
        a.append(tie[i])
    else:
        a.append(tie[i].split(' ')[0])
for i in range(0,len(final['Year'])):
    if(home[i]>away[i]):
        winner[i]=home_c[i]
    elif(home[i]<away[i]):
        winner[i]=away_c[i]
    elif home[i]==away[i]:
        winner[i]=a[i]
final = final.drop(labels=[851], axis=0)
winners=[]
for i in winner:
    winners.append(i.split(' ')[0])
winners.pop()
cnt = cl.Counter()
for word in winners:
    cnt[word] += 1
labels = []
sizes = []
for x, y in cnt.items():
    labels.append(x)
    sizes.append(y)
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format
explode=[0, 0, 0, 0.1, 0, 0, 0, 0]
plt.pie(sizes, labels=labels,autopct=autopct_format(sizes),startangle=90,explode=explode)
plt.legend(loc=3,prop={'size':9})
plt.axis('equal')
plt.title('Number of world cups for each country (1930-2014)', loc='center', pad=50)
plt.show()

#code 7:
#This figure shows referee's with most matches
ref = matches["Referee"].value_counts().reset_index()
ref = ref.sort_values(by="Referee",ascending=False)
plt.figure(figsize=(10,10))
sns.barplot("Referee","index",data=ref[:20],linewidth=1)
plt.xlabel("count")
plt.ylabel("Refree name")
plt.grid(True)
plt.title("Referee's with most matches")
plt.show()

#code 8:
#This figure shows the Number of world cups that every player from each nation has
teams = wins.groupby("Team")["Number"].sum()
u=wins.Team
u=u.unique()
u=u.tolist() #teams label
w=teams[:].tolist()
plt.figure(figsize=(12,7))
sns.barplot(u,w,linewidth=1)
plt.grid(True)
plt.title("Number of world cups that every player from each nation has")
plt.show()

#code 9:
#These figures compares between two countries based on wins,loses, number of matches played and number of goals each team has
matches["Home Team Name"] = matches["Home Team Name"].str.replace('rn">United Arab Emirates',"United Arab Emirates")
matches["Home Team Name"] = matches["Home Team Name"].str.replace("C�te d'Ivoire","Côte d’Ivoire")
matches["Home Team Name"] = matches["Home Team Name"].str.replace('rn">Republic of Ireland',"Republic of Ireland")
matches["Home Team Name"] = matches["Home Team Name"].str.replace('rn">Bosnia and Herzegovina',"Bosnia and Herzegovina")
matches["Home Team Name"] = matches["Home Team Name"].str.replace('rn">Serbia and Montenegro',"Serbia and Montenegro")
matches["Home Team Name"] = matches["Home Team Name"].str.replace('rn">Trinidad and Tobago',"Trinidad and Tobago")
matches["Away Team Name"] = matches["Away Team Name"].str.replace('rn">United Arab Emirates',"United Arab Emirates")
matches["Away Team Name"] = matches["Away Team Name"].str.replace("C�te d'Ivoire","Côte d’Ivoire")
matches["Away Team Name"] = matches["Away Team Name"].str.replace('rn">Republic of Ireland',"Republic of Ireland")
matches["Away Team Name"] = matches["Away Team Name"].str.replace('rn">Bosnia and Herzegovina',"Bosnia and Herzegovina")
matches["Away Team Name"] = matches["Away Team Name"].str.replace('rn">Serbia and Montenegro',"Serbia and Montenegro")
matches["Away Team Name"] = matches["Away Team Name"].str.replace('rn">Trinidad and Tobago',"Trinidad and Tobago")
matches["Home Team Name"] = matches["Home Team Name"].str.replace("Germany FR","Germany")
matches["Away Team Name"] = matches["Away Team Name"].str.replace("Germany FR","Germany")
ht = matches["Home Team Name"].value_counts().reset_index()
ht.columns = ["team","matches"]
at = matches["Away Team Name"].value_counts().reset_index()
at.columns = ["team","matches"]
mt = pd.concat([ht,at],axis=0)
mt = mt.groupby("team")["matches"].sum().reset_index().sort_values(by="matches",ascending=False)
def label(matches):
    if matches["Home Team Goals"] > matches["Away Team Goals"]:
        return "Home team win"
    if matches["Away Team Goals"] > matches["Home Team Goals"]:
        return "Away team win"
    if matches["Home Team Goals"] == matches["Away Team Goals"]:
        return "DRAW"
matches["outcome"] = matches.apply(lambda matches:label(matches),axis=1)
matches[['Home Team Name', 'Home Team Goals', 'Away Team Goals', 'Away Team Name', "outcome"]]
def win_label(matches):
    if matches["Home Team Goals"] > matches["Away Team Goals"]:
        return matches["Home Team Name"]
    if matches["Home Team Goals"] < matches["Away Team Goals"]:
        return matches["Away Team Name"]
    if matches["Home Team Goals"] == matches["Away Team Goals"]:
        return "DRAW"
def lst_label(matches):
    if matches["Home Team Goals"] < matches["Away Team Goals"]:
        return matches["Home Team Name"]
    if matches["Home Team Goals"] > matches["Away Team Goals"]:
        return matches["Away Team Name"]
    if matches["Home Team Goals"] == matches["Away Team Goals"]:
        return "DRAW"
tt_gl_h = matches.groupby("Home Team Name")["Home Team Goals"].sum().reset_index()
tt_gl_h.columns = ["team","goals"]
tt_gl_a = matches.groupby("Away Team Name")["Away Team Goals"].sum().reset_index()
tt_gl_a.columns = ["team","goals"]
total_goals = pd.concat([tt_gl_h,tt_gl_a],axis=0)
total_goals = total_goals.groupby("team")["goals"].sum().reset_index()
total_goals = total_goals.sort_values(by="goals",ascending =False)
matches["win_team"] = matches.apply(lambda matches: win_label(matches), axis=1)
matches["lost_team"] = matches.apply(lambda matches: lst_label(matches), axis=1)
lst = matches["lost_team"].value_counts().reset_index()
win = matches["win_team"].value_counts().reset_index()
matches_played = mt.copy()
mat_new = matches_played.merge(lst, left_on="team", right_on="index", how="left")
mat_new = mat_new.merge(win, left_on="team", right_on="index", how="left")
mat_new = mat_new[["team", "matches", "lost_team", "win_team"]]
mat_new = mat_new.fillna(0)
mat_new["win_team"] = mat_new["win_team"].astype(int)
mat_new["draws"] = (mat_new["matches"]) - (mat_new["lost_team"] + mat_new["win_team"])
mat_new = mat_new.merge(total_goals, left_on="team", right_on="team", how="left")
mat_new = mat_new.rename(columns={"win_team": "wins", "lost_team": "loses"})
ma=mat_new[['team','matches']]
ma.set_index('team',inplace=True)
Ma=ma.to_dict()
go=mat_new[['team','goals']]
go.set_index('team',inplace=True)
Go=go.to_dict()
wi=mat_new[['team','wins']]
wi.set_index('team',inplace=True)
Wi=wi.to_dict()
lo=mat_new[['team','loses']]
lo.set_index('team',inplace=True)
Lo=lo.to_dict()
def team_compare(team1, team2):
    lst = [team1, team2]
    dat = mat_new[mat_new["team"].isin(lst)]
    team=mat_new['team'].tolist()
    oi = []
    oi.append(Ma['matches'][team1])
    oi.append(Ma['matches'][team2])
    plt.figure(figsize=(12, 8))
    sns.barplot(lst, oi, linewidth=1)
    plt.grid(True)
    plt.title("matches")
    plt.show()
    g = []
    g.append(Go['goals'][team1])
    g.append(Go['goals'][team2])
    plt.figure(figsize=(12, 8))
    sns.barplot(lst, g, linewidth=1)
    plt.grid(True)
    plt.title("goals")
    plt.show()
    w = []
    w.append(Wi['wins'][team1])
    w.append(Wi['wins'][team2])
    plt.figure(figsize=(12, 8))
    sns.barplot(lst, w, linewidth=1)
    plt.grid(True)
    plt.title("Wins")
    plt.show()
    l = []
    l.append(Lo['loses'][team1])
    l.append(Lo['loses'][team2])
    plt.figure(figsize=(12, 8))
    sns.barplot(lst,l, linewidth=1)
    plt.grid(True)
    plt.title("loses")
    plt.show()
team_compare("Portugal", "Argentina")
