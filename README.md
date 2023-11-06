# NeonCore Framework

![image](https://user-images.githubusercontent.com/109377/211684849-7c9ffe0a-898c-4f84-bb96-642e179b29b2.jpeg)

Welcome to the NeonCore Framework, the ultimate modular toolkit for building immersive role-playing experiences, that is not only easy to use, but also easy to expand upon for future projects.

Whether you're building a game set in the gritty world of Night City, or creating an entirely new world of your own, the NeonCore Framework has everything you need to bring your vision to life. From the story manager with modular story elements, to the map class and skill check commander, every aspect of the framework has been designed with ease of use and expansion in mind.

The character and lifepath class allows for deep customization of player characters, while the NPC behavior class ensures that the non-player characters in the world feel truly alive. The Characters Manager and Action Manager work seamlessly together to provide a smooth and immersive gameplay experience.

The command registrar class allows for easy registration and management of in-game commands, making it simple to add new features and functionality as your game grows.

Built in Python, the **NeonCore Framework** is a terminal-based game that fits into 80x24, has graphic fidelity with animated ASCII art, and even has the potential to be a mod for Cyberpunk 2077, playable on a VT52.

### Usage

To use the **NeonCore Framework**, follow these steps:

1. Clone the repository to your local machine.
2. Run the game by running the following command:
   ```bash
   python run_game.py
   ```
   This will start the game and display the main menu.
3. Follow the on-screen instructions to navigate the game and play through the story.

### Running the llama-cpp-python server
To run the llama-cpp-python server with the example model, use the following command:
```bash
python -m llama_cpp.server --model models/utopia-13b.Q4_K_M.gguf --n_gpu_layers -1 --tensor_split 2 --chat_format alpaca
```
This command starts the server with the `utopia-13b.Q4_K_M.gguf` model, using all GPU layers and splitting tensors across 2 GPUs. The server is set to use the Alpaca chat format.

### Talking to the AI

Once the server is running, you can talk to the AI using the `talk` command in the `cmd.Cmd()` command line. Simply type `talk` followed by your message. For example:

```bash
talk Hello, how are you?
```
This will send the message "Hello, how are you?" to the AI, and the AI's response will be printed out in the command line.
These instructions explain how to start the llama-cpp-python server and how to talk to the AI using the `talk` command.