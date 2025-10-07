import random
import json 

# load database
with open("nba_players_database.json", "r") as f:
    nba_players = json.load(f)


"""
A score class to make a score object to output and add score
"""
class Score:
    def __init__(self):
        self.user_score = 0

    def add_point(self):
        self.user_score += 1

    def get_score(self):
        return self.user_score


def guess_jersey(player_by_decade=None, player_by_team=None, score=None):
    """
    This function will randomly pick a player in the database base on the parameters
    and asks the user to guess the jersey number of the player.
    The user has a limited number of attempts. After winning or using all attempts,
    the user can choose to play again or exit.
    """

    while True:
    # Select a random player in the database and get name and jersey numbers
        if player_by_decade and not player_by_team:
            random_player = random.choice(player_by_decade)

        elif player_by_team and not player_by_decade:
            random_player = random.choice(player_by_team)

        else:
            random_player = random.choice(nba_players)

        player_name = random_player.get("name")
        player_number = random_player.get("number")

        max_attempts = 5

        # Convert the list of numbers in to strings
        number_string = ", ".join(str(num) for num in player_number)

        # If list is more than 1 it will print are 
        verb = "are" if len(player_number) > 1 else "is"  

        # Output the name of the player and show the attemps the user can make
        print(f"Guess the jersey number of {player_name}")
        print(f"You have {max_attempts} tries")
        attempts = 0

    
    #The user will type in a number and it will check the players jersey number
        while attempts < max_attempts:
            user_input = input(">")
            if user_input == "q":
                print("Exiting jersey number")
                return
            try:
                user_guess = int(user_input)
                attempts += 1
                if user_guess in player_number:  
                    print(
                        f"Congrats {player_name} jersey number{'' if len(player_number) == 1 else 's'} {verb} {number_string}")
                    score.add_point()
                    break
                
                elif user_guess not in player_number and attempts < max_attempts:  # The message will not be outputed in the last try because there would be no try again at that point
                    print("Wrong try again")
                # Instead of try again the output will be different on the last attemp
                #  and if the player didnt guess it right it will show them the asnwer
                if user_guess not in player_number and attempts == max_attempts:  
                    print(f"You lost {player_name}'s number{'' if len(player_number) == 1 else 's'} {verb} {number_string}")
            except ValueError:
                print("Please enter a valid number")

        retry = input("Do you want to play again? (yes/no): ").strip().lower()
        if retry != "yes":
            print("Thanks for playing!")
            break


def game_menu():
    """
    This output will give the user choice to play, filter teams or decades and quit the game
    """
    print("Guess the jersey number")
    print("Press")
    print("1. to guess nba jersey")
    print("2. to filter team")
    print("3. to filter decade")
    print("4. to view score")
    print("'q' to quit")


def decade_filter():
    """
    This function will take a decade from the user and it will look at the decades in the list of nba players
    if the nba player have a value of that decade they will be added on a list in the function that will be pass on
    to the guess_jersey function
    """
    while True:
        user_input = input("What decade do you want to go? For example 1980, 2010: ")

        if user_input == "q":
            print("Exiting decade filter")
            break
        try:
            decade = int(user_input)
            found = False
            players_in_decade = []
           
            for player in nba_players:  #Loop to the entire list to look if the decade is inside the database
                if decade in player["decade"]:  # If the player has that decade input they will be added to the list
                    players_in_decade.append(player)
                    found = True
            if found:
                print(f"yes {decade} is here")
                return players_in_decade

            
            else:
                print(f"{decade} not found")
        except:
             print("Please enter a valid decade")


def team_filter():
    """
    This function will take a team from the user and it will look at the decades in the list of nba players
    if the nba player have a value of that team they will be added on a list in the function that will be pass on
    to the guess_jersey function
    """
    while True:
        team = input("What team do you want to go? For example Lakers, Celtics: ")
        team_title = team.title()
        found = False
        players_in_team = []
        if team == "q":
            print("Exiting team menu")
            break
        for player in nba_players: #Loop to the entire list to look if the team is inside the database
            if team_title in player["team"]: #If the player is on the team  they will be added to the list
                players_in_team.append(player)
                found = True
        
        if found :
            print(f"yes {team_title} is here")
            return players_in_team

            
        else:
            print(f"{team_title} not found")
    
# This will handle user choices
def main():
    score = Score() 
    while True:
        game_menu()
        user_char = input(">")
        # If the user type in 1 it will run the game without any filter
        if user_char == "1":
            guess_jersey(score=score)
                
        # This will run the team filter function and it will pass the return value to the guess jersey function
        elif user_char == "2":
            team_player = team_filter()
            if team_player:
                guess_jersey(player_by_team=team_player, score = score)
                    
        # This will run the decade filter function and it will pass the return value to the guess jersey function
        elif user_char == "3":
            decade_player = decade_filter()
            if decade_player:
                guess_jersey(player_by_decade=decade_player, score = score)
        
        # This option is to view the score
        elif user_char == "4":
            print(f"Your score is {score.get_score()}")
            
        # Whenever the player press q it quit anytime.
        elif user_char == "q":
            print("thank you for playing!")
            print(f"Your score is {score.get_score()}")
            break
        else:
            print("Invalid, please select between 1, 2, 3, 4 or 'q'")


main()