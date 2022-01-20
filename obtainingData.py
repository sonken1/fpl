import requests
import json
import time
import csv


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

    def get_player_data(self, player_id):
        return self.get_data(self.player_url.format(player_id))

    def get_base_data(self):
        return self.get_data(self.general_url)

    def get_fixture_data(self):
        return self.get_data(self.fixture_url)

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



def parse_data(path, url, name_dump, headers_of_interest, types=''):
    data = get_data(path, url, name_dump)
    headers, raw_path = build_statistic_header(data, path + 'raw_' + name_dump + '.csv', types)
    # int_headers = ['first_name', 'second_name', 'id', 'web_name', 'now_cost', 'cost_change_start', 'element_type',
    #                'selected_by_percent', 'team', 'team_code', 'total_points', 'minutes', 'goals_scored', 'assists',
    #                'clean_sheets', 'goals_conceded', 'yellow_cards', 'red_cards', 'saves', 'bonus', 'bps']
    clean_path = clean_data(raw_path, path + 'cleaned_' + name_dump + '.csv', headers_of_interest)
    return headers, raw_path, clean_path


def build_statistic_header(statistics_dict_full, path, entry_type):
    """
    Right now, the passed stats_dict is assumed to be player data. To make this more generic/general, remove "elements"
    and pass the type (elements/events/teams...) as an argument to the function and this could clean all data.
    """
    # Empty variable to fill
    statistics_dict = statistics_dict_full[entry_type][0]
    headers = []

    # Save all keys into one massive header
    for key, val in statistics_dict.items():
        headers += [key]

    # Save all headers into a .csv file
    with open(path, 'w+', encoding='utf8', newline='') as file:
        w = csv.DictWriter(file, sorted(headers))
        w.writeheader()
        for player in statistics_dict_full[entry_type]:
            w.writerow({k: str(v).encode('utf-8').decode('utf-8') for k, v in player.items()})
    return headers, path


def clean_data(path, clean_path, headers_of_interest):
    """
    This cleaner should be able to be used as a generic cleaner, not only for player data but also gw etc.
    """
    raw_file = open(path, 'r+', encoding='utf-8')
    r = csv.DictReader(raw_file)

    with open(clean_path, 'w+', encoding='utf8', newline='') as file:
        w = csv.DictWriter(file, headers_of_interest, extrasaction='ignore')
        w.writeheader()
        for line in r:
            w.writerow(line)
    return clean_path


if __name__ == '__main__':
    testDataFetcher = dataFetcher()

    # Testing Manager Data
    eliasData = testDataFetcher.get_manager_data(2481730)
    print("Elias Säsongsdata: ")
    for key in eliasData:
        print(key, ": ", eliasData[key])

    # Testing Player Data
    print("\nLucas Moura: ")
    lucasMoura_id = 362
    lucasMoura_data = testDataFetcher.get_player_data(lucasMoura_id)
    for key in lucasMoura_data:
        print(key, ": ", lucasMoura_data[key])



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
