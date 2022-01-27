import requests
import json
import time
import csv
import pandas as pd
import numpy as np


class dataFetcher:

    def __init__(self):
        self.general_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        # Contains
        # events: Basic information of every Gameweek such as average score, highest score, top scoring player, most
        # captained, etc.
        # game_settings: The game settings and rules. (not important)
        # phases: Phases of FPL season. (not really important)
        # teams: Basic information of current Premier League clubs.
        # total_players: Total FPL players.
        # elements: Information of all Premier League players including points, status, value, match stats (goals,
        # assists, etc.), ICT index, etc.
        # element_types: Basic information about player’s position (GK, DEF, MID, FWD).
        self.fixture_url = "https://fantasy.premierleague.com/api/fixtures/"
        # Contains
        # event refers to the event id in events section of the bootstrap-static data.
        # team_a and team_h refers to the team id in teams section of the bootstrap-static data. team_a for the away
        # team and team_h for the home team.
        # team_h_difficulty and team_a_difficulty is the FDR value calculated by FPL.
        # stats contains a list of match facts that affect points of a player. It consists of goals_scored, assists,
        # own_goals, penalties_saved, penalties_missed, yellow_cards, red_cards, saves, bonus, and bps data. The JSON
        # structure can be seen in image below.
        # value is the amount and element refers to the element id in elements section of the bootstrap-static data.
        self.player_url = "https://fantasy.premierleague.com/api/element-summary/{}/"   # Need to add .format(player_id)
        # Contains
        # fixtures: A list of player’s remaining fixtures of the season.
        # history: A list of player’s previous fixtures and its match stats.
        # history_past: A list of player’s previous seasons and its seasonal stats.
        self.gw_url = "https://fantasy.premierleague.com/api/event/{}/live/"   # Need to add .format(gw_id)
        self.manager_url = "https://fantasy.premierleague.com/api/entry/{}/"    # Need to add .format(manager_id)
        self.managerHistory_url = "https://fantasy.premierleague.com/api/entry/{}/history/"  # Need to add .format(manager_id)

        # Get initial data
        self.base_data = self.get_base_data()
        self.fixture_data = self.get_fixture_data()
        self.team_data = self.create_team_data()

    def get_base_data(self):
        return self.get_data(self.general_url)

    def get_fixture_data(self):
        return self.get_data(self.fixture_url)

    def get_player_data(self, player_id):
        return self.get_data(self.player_url.format(player_id))

    def get_gw_data(self, gw_id):
        return self.get_data(self.gw_url.format(gw_id))

    def get_manager_data(self, manager_id):
        return self.get_data(self.manager_url.format(manager_id))

    def get_managerHistory_data(self, manager_id):
        return self.get_data(self.managerHistory_url.format(manager_id))

    def get_data(self, url, saveData=False, path=False, name_dump=False):
        """
        Retrieve fpl stats from url
        returns requested data
        """
        response = ''
        while response == '':
            try:
                response = requests.get(url)
            except:
                time.sleep(5)
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        response_text = response.text
        data = json.loads(response_text)
        if saveData:
            with open(path + name_dump + '.json', 'w') as out:
                json.dump(data, out)
        return data

    def create_team_data(self):
        row_names = ['short_name', 'code', 'pulse_id', 'strength_overall_home', 'strength_overall_away',
                     'strength_attack_home', 'strength_attack_away', 'strength_defence_home', 'strength_defence_away']
        teams_in_id_order = sorted(self.base_data['teams'], key=lambda d: d['id'])
        id_col_names = []
        for team in teams_in_id_order:
            id_col_names.append(team['id'])
        temp_df = pd.DataFrame(teams_in_id_order)
        team_df = temp_df.T
        team_df.columns = id_col_names

        return team_df

    def create_advanced_team_data(self):

        # This is bas atm, but idea is to concat all away & home fixtures and add to team
        for team_id in self.team_data:
            temp_a = np.where((self.fixture_data.loc['team_a'] == team_id).to_list())[0]
            temp_h = np.where((self.fixture_data.loc['team_h'] == team_id).to_list())[0]
            fixture_data[np.where(temp_lst)[0]]



        self.team_data

    def create_fixture_data(self):

        temp_df = pd.DataFrame(self.fixture_data)
        fixture_df = temp_df.T

        # For future adding fixtures properly (here we would like all data from away team (team_a) with id 1
        # (i.e. all arsenal away games)
        # arsenal_away = temp_df.loc[temp_df['team_a'] == 1]
        return fixture_df

    def create_players_data(self):
        # Columns are player id
        players_in_id_order = sorted(self.base_data['elements'], key=lambda d: d['id'])
        id_col_names = []
        for player in players_in_id_order:
            id_col_names.append(player['id'])
        temp_df = pd.DataFrame(players_in_id_order)
        players_df = temp_df.T
        players_df.columns = id_col_names # Name the columns by sorted id rather than iterable
        return players_df


if __name__ == '__main__':
    testDataFetcher = dataFetcher()

    # Testing Manager Data
    eliasID = 2481730
    eliasData = testDataFetcher.get_manager_data(eliasID)

    # Testing Player Data
    lucasMoura_id = 362
    lucasMoura_data = testDataFetcher.get_player_data(lucasMoura_id)

    # Testing GW Data
    gw_id = 20
    gw20_data = testDataFetcher.get_gw_data(gw_id)

    # Testing Fixture Data
    basic_fixture_data = testDataFetcher.get_fixture_data()

    # Testing Base Data
    base_data = testDataFetcher.get_base_data()

    # Testing Team Data
    team_data = testDataFetcher.create_team_data()

    # Testing Fixture Data
    fixture_data = testDataFetcher.create_fixture_data()

    # Testing Players Data
    players_data = testDataFetcher.create_players_data()


    # team_id = "3022773"
    # gameweek = "1"
    # url_all_players = "https://fantasy.premierleague.com/api/bootstrap-static/"
    # # All players but also teams, elements and gameweeks
    # url_specific_player = "https://fantasy.premierleague.com/api/element-summary/"  # needs + str(player_id) + str('/').
    # # Only for future
    # url_team = "https://fantasy.premierleague.com/api/entry/" + team_id + "/"   # + str(entry_id) my own team!
    # url_team_history = "https://fantasy.premierleague.com/api/entry/" + team_id + "/history/"
    # url_team_picks = "https://fantasy.premierleague.com/api/entry/" + team_id + "/event/" + gameweek + "/picks/"
    # url_team_transfers = "https://fantasy.premierleague.com/api/entry/" + team_id + "/transfers/"
    # url_fixtures = "https://fantasy.premierleague.com/api/fixtures/"    # all fixtures
    #
    # data_path = 'C:/Users/elias/mainFolder/fantasy-premier-league/data/'
    # player_headers = ['first_name', 'second_name', 'id', 'web_name', 'now_cost', 'cost_change_start', 'element_type',
    #                'selected_by_percent', 'team', 'team_code', 'total_points', 'minutes', 'goals_scored', 'assists',
    #                'clean_sheets', 'goals_conceded', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps']
    # team_headers = ['code', 'draw', 'form', 'id', 'loss', 'name', 'played', 'points', 'position', 'short_name',
    #                 'strength', 'team_division', 'unavailable', 'win', 'strength_overall_home', 'strength_overall_away',
    #                 'strength_attack_home', 'strength_attack_away', 'strength_defence_home', 'strength_defence_away']
    # type_players = "elements"   # players
    # type_teams = "teams"    # teams
    # type_positions = "element_types"    # position specifications for FPL
    # type_gw = "events"  # gw summary (light)
