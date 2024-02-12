-- create db sports
create database sports;

-- Create table for batting statistics
CREATE TABLE IF NOT EXISTS batting_scorecard (
    batsmen VARCHAR(100),
    dismissed VARCHAR(100),
    runs_scored INT,
    balls_faced INT,
    minutes_played INT,
    fours INT,
    sixes INT,
    strike_rate DECIMAL(5,2),
    team VARCHAR(100),
    match_name VARCHAR(100),
    innings VARCHAR(100),
    scorecard_id VARCHAR(100)
);

-- Create table for bowling statistics
CREATE TABLE IF NOT EXISTS bowling_scorecard (
    bowler VARCHAR(100),
    overs DECIMAL(5,2),
    maidens INT,
    runs INT,
    wickets INT,
    economy DECIMAL(5,2),
    zeros INT,
    fours INT,
    sixes INT,
    wides INT,
    noballs INT,
    team VARCHAR(100),
    match_name VARCHAR(100),
    innings VARCHAR(100),
    scorecard_id VARCHAR(100)
);

-- Create table for match details
CREATE TABLE IF NOT EXISTS match_scorecard (
    team_a VARCHAR(100),
    team_b VARCHAR(100),
    scorecard_id VARCHAR(100),
    description VARCHAR(500),
    match_result VARCHAR(100),
    stadium VARCHAR(100),
    series VARCHAR(100),
    series_result VARCHAR(100),
    season VARCHAR(100),
    player_of_the_match VARCHAR(100),
    player_of_the_series VARCHAR(100),
    match_number VARCHAR(100),
    tv_umpire VARCHAR(100),
    reserve_umpire VARCHAR(100),
    match_referee VARCHAR(100),
    standing_umpire1 VARCHAR(100),
    standing_umpire2 VARCHAR(100),
    match_date VARCHAR(100),
    match_format VARCHAR(100),
    toss_won VARCHAR(100),
    toss_decision VARCHAR(100),
    winner VARCHAR(100),
    match_count VARCHAR(100),
    match_type VARCHAR(100)
);

-- Create table for total statistics
CREATE TABLE IF NOT EXISTS total_scorecard (
    over_played DECIMAL(5,2),
    run_rate DECIMAL(5,2),
    total_score INT,
    wickets_fallen INT,
    team VARCHAR(100),
    match_name VARCHAR(100),
    innings VARCHAR(100),
    scorecard_id VARCHAR(100)
);

-- Create table for fall of wickets
CREATE TABLE IF NOT EXISTS fall_of_wickets (
    wicket_number INT,
    fallen_score INT,
    fallen_over DECIMAL(5,2),
    batsmen VARCHAR(100),
    team VARCHAR(100),
    match_name VARCHAR(100),
    innings VARCHAR(100),
    scorecard_id VARCHAR(100)
);