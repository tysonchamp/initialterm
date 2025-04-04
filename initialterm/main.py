# Import necessary libraries
import subprocess
import threading
import ollama
import os
import sys
import logging
import json
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Define color codes for terminal output
class Color:
    """
    A class to define ANSI color codes for terminal output.
    """
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    PINK = '\033[95m'


def get_session_file(os_name):
    """
    Gets the path to the session file.

    Parameters:
    os_name (str): The operating system name.

    Returns:
    str: The path to the session file.
    """
    session_dir = os.path.join(os.path.expanduser("~"), ".conversation")
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    session_id = uuid.uuid4().hex
    return os.path.join(session_dir, f"session_{os_name.lower()}_{session_id}.json")

def load_session(session_file):
    """
    Loads the session data from a JSON file.

    Parameters:
    session_file (str): The path to the session file.

    Returns:
    list: The session data.
    """
    if os.path.exists(session_file):
        with open(session_file, 'r') as file:
            return json.load(file)
    return []

def save_session(session_file, session_data):
    """
    Saves the session data to a JSON file.

    Parameters:
    session_file (str): The path to the session file.
    session_data (list): The session data to save.
    """
    with open(session_file, 'w') as file:
        json.dump(session_data, file, indent=4)

def ollama_api_call(os_name, command, model_name, session_data):
    """
    Calls the Ollama API to convert user queries into command-line commands.

    Parameters:
    os_name (str): The operating system name.
    command (str): The user query to convert.
    model_name (str): The model name to use for the API call.
    session_data (list): The session data to include in the API call.

    Returns:
    str: The generated command-line command.
    """
    logging.debug(f"Calling Ollama API with OS: {os_name}, command: {command}, and model: {model_name}")
    messages = session_data + [{'role': 'user', 'content': f'I am using {os_name} operating system which does not have any extentions instaalled and I want to Convert the user query: {command} to commandline / terminal code. Only output one line of terminal command please. Do not add any other text as the intention is to copy paste this generated output directly in terminal and run.'}]
    stream = ollama.chat(
        model=model_name,
        options={'temperature': 0.1},
        messages=messages,
        stream=True,
    )
    logging.debug("Ollama API call completed")
    
    stream_data = []
    for chunk in stream:
        stream_data.append(chunk['message']['content'])
        print(f"{Color.BLUE}{chunk['message']['content']}{Color.RESET}", end='', flush=True)
    
    strdata = ''.join([chunk for chunk in stream_data]).replace("`", "").replace("```sh", "").replace("\n", "").replace("```bash", "")
    print(f"\n{Color.BLUE}Finished.\nGenerated: {strdata}\n{Color.RESET}")
    
    session_data.append({'role': 'assistant', 'content': strdata.strip().replace('`', '')})
    return strdata.strip().replace('`', '')

def ollama_api_correct_error(os_name, error_message, model_name, session_data):
    """
    Calls the Ollama API to correct errors in the command.

    Parameters:
    os_name (str): The operating system name.
    error_message (str): The error message to correct.
    model_name (str): The model name to use for the API call.
    session_data (list): The session data to include in the API call.

    Returns:
    str: The corrected command-line command.
    """
    logging.debug(f"Calling Ollama API to correct error with OS: {os_name}, error: {error_message}, and model: {model_name}")
    messages = session_data + [{'role': 'user', 'content': f'I am using {os_name} operating system and encountered the following error while executing a command: {error_message}. Please provide a corrected command to resolve this error.'}]
    stream = ollama.chat(
        model=model_name,
        options={'temperature': 0.1},
        messages=messages,
        stream=True,
    )
    logging.debug("Ollama API error correction call completed")
    
    stream_data = []
    for chunk in stream:
        stream_data.append(chunk['message']['content'])
        print(f"{Color.BLUE}{chunk['message']['content']}{Color.RESET}", end='', flush=True)
    
    strdata = ''.join([chunk for chunk in stream_data]).replace("`", "").replace("```sh", "").replace("\n", "").replace("```bash", "")
    print(f"\n{Color.BLUE}Finished.\nCorrected: {strdata}\n{Color.RESET}")
    
    session_data.append({'role': 'assistant', 'content': strdata.strip().replace('`', '')})
    return strdata.strip().replace('`', '')

def echo_and_execute(command, os_name, model_name, session_data):
    """
    Executes a command generated by the Ollama API and handles user confirmation.

    Parameters:
    command (str): The command to execute.
    os_name (str): The operating system name.
    model_name (str): The model name used for the API call.
    session_data (list): The session data to include in the API call.
    """
    logging.info(f"Executing command: {command} on OS: {os_name}")
    try:
        command_to_execue = ollama_api_call(os_name, command, model_name, session_data)
        confirm = input(f"Generated command is: {Color.CYAN}'{command_to_execue}', shall we continue? (Y/N):{Color.RESET}# ").strip().lower()
        if confirm.lower() in ['y', 'yes', 'yup']:
            result = subprocess.run(command_to_execue, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info(f"Command executed: {command_to_execue}")
        else:
            logging.warning("Command execution canceled by user")
            return
        output = result.stdout.decode().strip()
        error = result.stderr.decode().strip()
        if output:
            logging.debug(f"Command output: {output}")
            print(f"\n{Color.GREEN}# Output:{Color.RESET}\n{Color.PINK}{output}{Color.RESET}")
        if error:
            logging.error(f"Command error: {error}")
            print(f"\n{Color.RED}Error: {error}{Color.RESET}")
            corrected_command = ollama_api_correct_error(os_name, error, model_name, session_data)
            confirm = input(f"Corrected command is: {Color.CYAN}'{corrected_command}', shall we continue? (Y/N):{Color.RESET}# ").strip().lower()
            if confirm.lower() in ['y', 'yes', 'yup']:
                result = subprocess.run(corrected_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logging.info(f"Corrected command executed: {corrected_command}")
                output = result.stdout.decode().strip()
                error = result.stderr.decode().strip()
                if output:
                    logging.debug(f"Corrected command output: {output}")
                    print(f"\n{Color.GREEN}# Output:{Color.RESET}\n{Color.PINK}{output}{Color.RESET}")
                if error:
                    logging.error(f"Corrected command error: {error}")
                    print(f"\n{Color.RED}Error: {error}{Color.RESET}")
    except Exception as e:
        logging.exception(f"An exception occurred: {e}")
        print(f"{Color.RED}An exception occurred while executing the command: {e}{Color.RESET}", file=sys.stderr)


def custom_cmd(os_name, model_name):
    """
    Starts a custom command prompt for executing user queries.

    Parameters:
    os_name (str): The operating system name.
    model_name (str): The model name to use for the API call.
    """
    logging.info(f"Starting custom command prompt for {os_name} with model {model_name}")
    print(f"{Color.CYAN}Welcome to the Initial Terminal command prompt for {os_name} with model {model_name}!\n Ollama with {model_name} LLM running locally for inference\n{Color.RESET}\n Type quit/exit to exit")

    session_file = get_session_file(os_name)
    session_data = load_session(session_file)

    while True:
        try:
            input_str = input(f"{Color.GREEN}_____________\nCommand to execute :\n{Color.RESET}# ")
            
            if "exit" in input_str.lower() or "quit" in input_str.lower():
                logging.info("Exiting custom command prompt")
                print(f"{Color.GREEN}Exiting the custom command prompt.{Color.RESET}")
                break

            session_data.append({'role': 'user', 'content': input_str})
            echo_and_execute(input_str, os_name, model_name, session_data)
            save_session(session_file, session_data)

        except KeyboardInterrupt:
            logging.info("Exiting custom command prompt due to keyboard interrupt")
            print("Exiting the custom command prompt.")
            break


def start_custom_cmd(model_name='gemma3:4b'):
    """
    Initializes the application and starts the custom command prompt.

    Parameters:
    model_name (str): The model name to use for the API call. Defaults to 'llama3.2:3b'.
    """
    import platform
    os_name = platform.system()
    
    if os_name not in ['Windows', 'Darwin', 'Linux']:
        logging.error("Unsupported OS. This script is designed for Windows, macOS, and Linux.")
        print("Unsupported OS. This script is designed for Windows, macOS, and Linux.")
        return
    
    os_name_mapping = {
        'Darwin': 'MacOS',
        'Linux': 'Linux',
        'Windows': 'Windows'
    }
    
    os_name = os_name_mapping.get(os_name, 'Unsupported OS')
    
    custom_cmd(os_name, model_name)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--spawn', action='store_true')
    parser.add_argument('--model', type=str, default='gemma3:4b', help='Specify the model name to use')
    args = parser.parse_args()

    if not args.spawn:
        start_custom_cmd(args.model)