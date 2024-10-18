import socket
import threading
import random
import time
from transformers import pipeline

# Initialize the text generation pipeline using a small large language model (haha, that sounds funny)
# Note, this model is pretty stupid, but it's free to use and I'm broke.
llm = pipeline('text-generation', model='distilgpt2')

# Game state variables
players = []
player_names = []
is_game_started = False
lock = threading.Lock()
start_requests = 0  # Counter for players requesting to start the game

# Prompts for the game (graciously generated by Chat GPT)
prompts = [
    "A dragon is approaching your position!",
    "A wild beast charges at you from the forest!",
    "A mysterious figure offers you a deal!",
    "A spaceship is crashing towards the ground!",
    "A giant boulder is rolling in your direction!",
    "You hear eerie footsteps behind you!",
    "A mysterious portal opens before you!",
    "You find an ancient artifact glowing in the dark!",
    "A loud explosion shakes the ground nearby!",
    "A ghostly apparition warns you of danger!",
    "You stumble upon a hidden treasure map!",
    "A storm begins to brew overhead!",
    "A swarm of angry bees chases you!",
    "You discover a secret passageway!",
    "An earthquake rattles the area!",
    "A group of bandits demands your valuables!",
    "A strange creature emerges from the shadows!",
    "You hear a distant howl echo through the night!",
    "A majestic phoenix lands nearby!",
    "You find a magical tome that grants wishes!",
    "A spell gone wrong creates a giant monster!",
    "A wise old sage offers you a riddle!",
    "You encounter a talking animal with a message!",
    "A fallen star crashes to the earth!",
    "A thief attempts to pick your pocket!",
    "You hear a melodic tune that lures you in!",
    "A stormy sea threatens to capsize your ship!",
    "You discover a hidden village in the woods!",
    "A witch appears and offers a potion!",
    "You find a mystical crystal that pulses with energy!",
    "A fierce wind blows, obscuring your path!",
    "You receive a letter from an old friend asking for help!",
    "A fog rolls in, making it hard to see!",
    "You hear the sound of chains rattling nearby!",
    "A dragon's roar echoes in the distance!",
    "You come across an abandoned campsite!",
    "A statue comes to life and challenges you!",
    "A village elder asks for your assistance!",
    "You find a cursed object that brings bad luck!",
    "A bridge collapses behind you!",
    "You stumble upon a mystical fountain!",
    "A group of adventurers seeks your aid!",
    "A mysterious illness spreads among the locals!",
    "You find a broken-down carriage in the woods!",
    "A storm reveals an underwater cave!",
    "A friendly ghost offers to guide you!",
    "You discover a rare flower with healing properties!",
    "A fire starts in the forest nearby!",
    "You encounter a rival adventurer!",
    "A prophecy foretells your arrival!",
    "You find a portal to another dimension!",
    "An old friend turns out to be a spy!",
    "You hear whispers of a hidden treasure!",
    "A spirit challenges you to a duel!",
    "You receive a mysterious phone call!",
    "A giant spider descends from the ceiling!",
    "You find a strange key that fits no lock!",
    "A blizzard begins to sweep the land!",
    "You hear the cries of a baby in the woods!",
    "A dark storm cloud follows you!",
    "A merchant offers to sell you magical items!",
    "You discover a secret society meeting in the woods!",
    "A loud voice beckons you to come closer!",
    "A wise old man gives you cryptic advice!",
    "You find a long-lost heirloom!",
    "A time traveler appears and warns you!",
    "You find a map leading to a hidden kingdom!",
    "A mysterious light guides your path!",
    "A dragon offers you a choice: fight or negotiate!",
    "A fierce wind picks up, threatening to throw you off balance!",
    "You find a letter detailing a conspiracy!",
    "A trap is set off, and you must escape!",
    "A healer offers to help you recover from your wounds!",
    "You find a treasure chest buried in the sand!",
    "A festival is happening in a nearby town!",
    "You overhear a secret conversation!",
    "A riddle is inscribed on a stone tablet!",
    "A warrior seeks your assistance in a battle!",
    "You find a hidden door in an ancient ruin!",
    "A creature demands a toll for passage!",
    "You hear a soft voice calling your name!",
    "You discover a magical item that grants you a wish!",
    "An avalanche blocks your escape route!",
    "A portal to the past opens up!",
    "A giant appears and demands tribute!",
    "You receive an urgent message from a distant land!",
    "A painting comes to life and speaks!",
    "You stumble upon an ancient temple!",
    "A friendly giant offers to help you!",
    "A rival faction challenges you to a duel!",
    "You encounter an old enemy in disguise!",
    "A spy tries to steal your secrets!",
    "A phoenix offers you a chance at resurrection!",
    "A curse turns you into a creature of the night!",
    "A treasure hunter seeks to partner with you!",
    "You find a strange crystal that shows the future!",
    "A local villager requests your help with a problem!",
    "A storm washes ashore strange artifacts!",
    "You meet a creature from your dreams!",
    "A dark figure lurks in the shadows, watching you!",
    "You find a set of enchanted armor!",
    "A creature offers to trade you information for a favor!",
    "A magical storm reveals hidden paths!",
    "You hear the laughter of children in the woods!",
    "A powerful sorcerer appears and challenges you!",
    "A message in a bottle washes ashore!",
    "A secret admirer leaves gifts at your doorstep!",
    "You find a missing person’s belongings!",
    "A series of mysterious events leads you to an ancient prophecy!",
    "A monstrous creature demands you solve a puzzle to pass!",
    "You discover an abandoned laboratory filled with experiments!",
]

# Results storage for each player
results = {}

def handle_client(conn, addr):
    global is_game_started, start_requests
    with lock:
        player_id = len(players) + 1  # Ensure each player has a unique player ID
        players.append(conn)

    conn.send(f"Welcome, you are player {player_id}.\n".encode())
    conn.send(b"Please input your name: ")
    name = conn.recv(1024).decode().strip()

    with lock:
        player_names.append(name)
        results[name] = 0  # Track survival

    conn.send(b"To start the game, type start. To see players, type players.\nWaiting for players to start the game.\n")

    while not is_game_started:
        data = conn.recv(1024).decode().strip()
        if data == "players":
            conn.send(f"Current players: {len(players)}/6\nNames: {', '.join(player_names)}\n".encode())
        elif data == "start":
            with lock:
                start_requests += 1
                broadcast(f"Start: {start_requests}/{len(players)}\n")
                
                # If all players have requested to start, then start the game
                if start_requests == len(players) - 1:
                    is_game_started = True
                    broadcast(b"Starting the game!\n")
                    time.sleep(1)  # Short delay before starting the game
            continue
        else:
            conn.send(b"Unknown command!\n")

    # Now that the game has started, start the game loop
    run_game()

def run_game():
    global prompts, results

    # Set number of rounds based on the number of players (up to 6 rounds)
    num_rounds = 6

    for _ in range(num_rounds):
        prompt = random.choice(prompts)
        broadcast(f"{prompt}\n")  # Broadcast the prompt to all players

        actions = {}
        threads = []

        # Create a separate thread for each player to collect input
        for i, player_conn in enumerate(players):
            player_name = player_names[i]
            thread = threading.Thread(target=collect_input, args=(player_conn, player_name, actions))
            threads.append(thread)
            thread.start()

        # Wait for all player responses
        for thread in threads:
            thread.join()  # Wait for each thread to finish

        # Process the results using the LLM
        for player_name in player_names:
            action = actions.get(player_name, "no response")  # Default to "no response" if no input
            outcome = generate_outcome(prompt, action)

            if "lives" in outcome:
                results[player_name] += 1

            broadcast(f"{player_name}: {action} Outcome: {outcome}\n")

        # Wait between rounds
        time.sleep(2)

    # Game over, show scores
    broadcast("Game over!\n")
    for player_name, score in results.items():
        broadcast(f"{player_name}: {score} points\n")

def collect_input(player_conn, player_name, actions):
    try:
        player_conn.send(b"What do you do: ")
        action = player_conn.recv(1024).decode().strip()

        if action:  # Ensure the action is valid and non-empty
            actions[player_name] = action
        else:
            actions[player_name] = "no response"

    except Exception as e:
        print(f"Error while collecting input from {player_name}: {e}")
        actions[player_name] = "no response"

def broadcast(message):
    for player_conn in players:
        player_conn.send(message.encode())

def generate_outcome(prompt, action):
    """Generate a dynamic outcome based on the prompt and action using LLM."""
    input_text = f"{prompt} Player action: {action}. What happens next?"
    response = llm(input_text, max_length=100, num_return_sequences=1)
    return response[0]['generated_text'].split('\n')[0]  # Return the generated outcome

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(6)
    print("Server started, waiting for players...")

    while True:
        conn, addr = server.accept()
        print(f"New connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
