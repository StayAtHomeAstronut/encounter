# Overview

This game is a simple text-based adventure game called "Encounter" that allows players to connect to a server with up to six clients per game. Players will encounter a series of scenarios based on pregenerated prompts. They will write how they respond to the scenarios in order to overcome the situation. Think of it as a choose your own adventure game with a twist. The server connects players to a Large Language Model that will narrarate what happens to the player in real time based on their response. The server functionality will be split into two sections: a lobby section, where players join and prepare to play the game, and the game itself, in which players address prompts and hear how their adventure pans out.

This software is designed to demonstrate a server/client relationship and expand my understanding of networking. It involves communications between a server and clients, and allows multiple clients to access and use the server concurrently. Additionally, it connects to a GPT model and provides data to each client over the course of the game. I wrote this to teach myself how networking between a server and clients works.

To use the software, simply launch the file called "server." When server responds, "waiting for players," you may launch the "client" program up to six times to fill the lobby. In the lobby, each player will type "start" to begin the game. All players must respond to the prompt to continue.

[Encounter Demonstration Video](https://youtu.be/vnuQ9iubKwA)

# Network Communication

Network communication is established using a client/server model. The server can
support up to six clients per game, and processes responses from each concurrently
using threads. The server also broadcasts information to all players during the
game phase.

I am using TCP (Transmission Control Protocol) as the communication protocol in this project.
The server is created using server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
The server is listening on port 5555 over localhost (127.0.0.1)
server.bind(('localhost', 5555))

the messages exchanged between the client and server are simple text strings. Clients send 
commands like "start" or their names, while the server sends text-based prompts and game instructions. 
These messages are encoded to bytes when being sent and decoded back into readable text when received.

# Development Environment

The coding enviroment VS Code was used to develop the software.
ChatGPT was used to generate the encounter prompts. (not the code.)

This program was developed in Python and includes several libraries.
- Socket is used to handle communication between the server and the clients. It is
called for in both the server and client-side code.
- Threading is used to allow the server to communicate with several clients at once.
- Random is used to randomly generate scenarios during the game phase.
- Time is used for timeout functions and to allow for a smoother gameplay experience.
- Transformers is used to connect users to a Large Language Model API from which
real-time responses can be generated.

# Useful Websites

* [Stack Overflow](https://stackoverflow.com/)
* [Github](https://github.com/)
* [Python Official Documentation](https://www.python.org/doc/)
* [Hugging Face Model Hub](https://huggingface.co/docs/hub/en/models-the-hub)

# Future Work

The LLM I am currently using, distilgpt2, is freeware. As a result, it's pretty random
at times and the responses don't usually make much sense. Using a better LLM would greatly improve gameplay, but it would also be expensive.

Currently, the game randomly chooses a prompt from a list of 106, but it might be fun to let players create their own prompts. Also, I should create a function to prevent prompts from reoccuring, though that is a very rare occurance.

Currently, when the game ends, there is no more dialogue. It might be good to return players to the lobby after their game and allow them to play again. Creating notifications when players leave the game might also be helpful.
