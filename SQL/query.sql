create database sports;

CREATE  table sports.match_table (

    team_a varchar(100),team_b varchar(100),scorecard_id varchar(100),description varchar(300),match_result varchar(100),stadium varchar(100),series varchar(100),
    season varchar(100),player_of_the_match varchar(100),player_of_the_series varchar(100),series_result varchar(100),
    match_number varchar(100),tv_umpire varchar(100),reserve_umpire varchar(100),match_referee varchar(100),
    standing_umpire1 varchar(100),standing_umpire2 varchar(100),match_date varchar(100),match_format varchar(100),toss_won varchar(100),toss_decision varchar(100),
    winner varchar(100),match_count varchar(100),match_type varchar(100)   );

CREATE table bowling_details(bowler varchar(100),overs int,maidens int,runs int,wickets int,economy float,zeros int,fours int,sixes int,wides int,noballs int,country varchar(100),match_name varchar(100));

CREATE table batting_details(batsmen varchar(100),wicket varchar(100),runs_scored int,balls_faced int,minutes_played int,fours int,sixes int,Strike_rate float,Country varchar(100),match_name varchar(100));

