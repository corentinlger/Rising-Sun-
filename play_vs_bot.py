import os
import argparse

from stable_baselines3 import PPO

from game.game_env import GameEnv
from game.players import Player, HeuristicPlayer, SepukuPoetsPlayer, HumanPlayer, bot_player_dict

# TODO : Add playing against trained agents
    # TODO : Would surely need to change the game_env
    # TODO : Enter a policy as parameter for the other player and choose its action according to it 
    # TODO : Let the scripted behaviors, just add a player class called TrainedPlayer, and it should take more arguments 
    # TODO : For example, the arguments necessary to load its model (action policy) and they would be initialized with None values in the GameEnv class
    # TODO : Lets go peut être stylé et puis plus cool à présenter comme projet 

def get_player_name():
    print("Hello and welcome to this version of the fighting phase of Rising Sun board game !")
    player_name = input("\nEnter your name : ")
    return player_name

def initialize_players(player_name, bot_behavior):
    player = HumanPlayer(name=player_name)
    
    if bot_behavior in bot_player_dict:
        bot_player = bot_player_dict[bot_behavior](name='bot_player')
    elif bot_behavior == "trained":
        try:
            pass
        except:
            raise(ValueError("A trained agent with those parameters hasn't been found"))
    else:
        raise(ValueError("Unknown bot bahavior"))

    return player, bot_player

def ask_displaying_rules():
    print("\nDo you want to read the rules (Y/N) ?")    
    display_rules = None

    while display_rules not in ["Y", "N"]:
        condition = display_rules != "Y" or "N"
        display_rules = input()

    return True if display_rules == "Y" else False
     
def display_rules():
    with open('utils/rules.txt', 'r') as file:
            print("\n ---- RULES ----")
            print(file.read())
            input("Press any key to continue...")

def play_game(player, bot_player, args):
    print(f"\nBeginning of the game")
    # Initialize the environment 
    player_won_fights = bot_won_fights = 0
    env = GameEnv(player=player, bot_player=bot_player, fights_per_game=args.fights_per_game, verbose=True)

    for game in range(args.nb_games):
        print("")
        obs, info = env.reset()
        done = False
        player_ep_nb_points = []
        bot_ep_nb_points = []
        while not done:
            print("")
            action =  player.choose_action()
            obs, reward, done, truncated, info = env.step(action)
            player_ep_nb_points.append(player.nb_points)
            bot_ep_nb_points.append(bot_player.nb_points)
            print(f"player points : {player.nb_points} bot_player points : {bot_player.nb_points}")
        if player.nb_points > bot_player.nb_points:
            player_won_fights += 1
        elif player.nb_points < bot_player.nb_points:
            bot_won_fights += 1

    return player_won_fights, bot_won_fights

def print_game_result(player_won_fights, bot_won_fights):
    print(f"\nFinal result : ")
    if player_won_fights == bot_won_fights:
        print(f"Equailty : you both won {player_won_fights} fights")
    elif player_won_fights > bot_won_fights:
        print(f"Victory ! You won {player_won_fights} fights and your opponent won {bot_won_fights} fights")
    elif player_won_fights < bot_won_fights:
        print(f"Defeat ! You won {player_won_fights} fights and your opponent won {bot_won_fights} fights")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--nb_games", type=int, required=False, default=3)
    parser.add_argument("--fights_per_game", type=int, required=False, default=2)
    parser.add_argument("--bot_behavior", type=str, required=False, default="random")
    parser.add_argument("--training_timesteps", type=int, required=False, default=100000)
    parser.add_argument("--seed", type=int, required=False, default=42)
    parser.add_argument("--algo", type=str, required=False, default="PPO")

    args = parser.parse_args()

    player_name = get_player_name()

    player, bot_player = initialize_players(player_name, args.bot_behavior)

    if ask_displaying_rules():
         display_rules()
        
    player_won_fights, bot_won_fights = play_game(player, bot_player, args)

    print_game_result(player_won_fights, bot_won_fights)


