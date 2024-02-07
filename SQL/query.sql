create database sports;

CREATE  table sports.match_table (team_a varchar(100),team_b varchar(100),winner varchar(100),margin varchar(100),stadium varchar(100),match_date varchar(100));

CREATE table bowling_details(bowler varchar(100),overs int,maidens int,runs int,wickets int,economy float,zeros int,fours int,sixes int,wides int,noballs int,country varchar(100),match_name varchar(100));

CREATE table batting_details(batsmen varchar(100),wicket varchar(100),runs_scored int,balls_faced int,matches_played int,fours int,sixes int,Strike_rate float,Country varchar(100),match_name varchar(100));

