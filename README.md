# ⚠️ Warning: Execute with Caution ⚠️

**Do not execute unverified commands in your terminal. Executing unknown or untrusted commands can potentially damage your computer, destroy files, and result in data loss. Always ensure that the commands you run are safe and verified.**

## Disclaimer

We are not responsible for any mishaps or damages that may occur from using this software. It is highly recommended that you fully understand how this software works before using it.

### How It Works

InitialTerm is a terminal application that leverages the Ollama API to convert user queries into command-line commands. When you input a query, the software sends it to the Ollama API, which processes the query using a specified model and returns a terminal command. This command is then displayed to you for execution. You have the option to confirm or cancel the execution of the generated command.

**Please ensure that you review and understand the commands before executing them to prevent any unintended consequences.**

---

# InitialTerm
[![PyPI version](https://badge.fury.io/py/initialterm.svg)](https://badge.fury.io/py/initialterm)

InitialTerm is a terminal application that uses the Ollama API to convert user queries into command-line commands. It supports both Windows and macOS operating systems.

## Installation

To install InitialTerm in editable mode, use the following command:

```bash
pip install -e .
```

Ensure you have the necessary dependencies installed. You can find them in the `requirements.txt` file or install them manually using:

```bash
pip install ollama requests
```

## PyPI Installation

InitialTerm is available on PyPI. You can install it using pip:

```bash
pip install initialterm
```

For more details, visit the [PyPI project page](https://pypi.org/project/initialterm/).

## Usage

To use InitialTerm, simply run the following command in your terminal:

```bash
initialterm
```

You can also specify a model to use by adding the `--model` option:

```bash
initialterm --model llama-3.2:3b
```

This will start the custom command prompt where you can enter your queries. The application will convert your queries into terminal commands using the specified model.

Type `exit` or `quit` to leave the command prompt.

## For Linux Users

Specially for Ubuntu 22 and above those needs to use `python env` add below line into your `~/.bashrc` file. Please modify the path to `initialterm/start.sh` based on your file location.

```bash
alias aiterminal='/PATH/TO/HOME/initialterm/start.sh'
```

After adding the alias, reload your `~/.bashrc` file to apply the changes: 

```bash
source ~/.bashrc
```

Now open your terminal and Just type the command: 

```bash
aiterminal
```

## Contributing

We welcome contributions to InitialTerm! If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create your branch from `main`.
2. Make your changes and test them thoroughly.
3. Submit a pull request with a clear description of your changes.

Feel free to open issues for bug reports or feature requests. We appreciate your feedback and contributions!

## Requirements

- Python 3.6+
- Ollama API

## License

This project is open-source and available under a permissive license. You are free to do whatever you want with this software, but please be safe and ensure that your actions do not cause harm to yourself, your data, or your computer.

This project is licensed under the MIT License. See the LICENSE file for details.