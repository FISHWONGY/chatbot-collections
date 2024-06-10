# chatbot-collections

<p align="left">
  <a href="https://fishwongy.github.io/post/20240423_chatbot" target="_blank"><img src="https://img.shields.io/badge/Blog-Read%20About%20This%20Project-blue.svg" /></a>
  <!--<a href="https://twitter.com/intent/follow?screen_name=fishwongxd" target="_blank"><img src="https://img.shields.io/twitter/follow/fishwongxd?style=social" /></a>-->
</p>

This repository, `chatbot-collections`, contains example chatbot code for various platforms including Discord, LINE Messenger, Slack, Telegram, Webex, and WhatsApp. All the chatbots are implemented using Python.

## ✨ Folder Structure

The repository is organized into separate folders for each chatbot. Each bot folder has a similar structure. Here is an example of the structure using the `slack-bot`:

```
.
├── discord-bot
├── line-bot-fastapi
├── slack-bot
│   ├── app
│   ├── deploy
│   ├── Dockerfile
│   ├── README.md
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── skaffold.yaml
├── telegram-bot
├── webex-bot-app
├── whatsapp-bot
└── README.md
```

## ✨ Chatbot Implementations

- **Discord Bot**: Implemented using the `pycord` library.
- **LINE Bot**: Implemented using `FastAPI` for building the webhook endpoint.
- **Slack Bot**: Implemented using `FastAPI` for building the webhook endpoint.
- **Telegram Bot**: Implemented using the `python-telegram-bot` library.
- **Webex Bot**: Implemented using the python `webex-bot` library.
- **WhatsApp Bot**: Implemented using `FastAPI` for building the webhook endpoint.

## ✨ Getting Started

Each bot folder contains its own `README.md` file with specific instructions on how to set up and run the bot. Please refer to the respective `README.md` file for more details.


# ✨ Features

The `chatbot-collections` repository provides a collection of chatbot implementations for various platforms. Here are some of the key features:

- **Multiple Platforms**: The repository includes chatbot implementations for Discord, LINE Messenger, Slack, Telegram, Webex, and WhatsApp.

- **Python-Based**: All chatbots are implemented using Python, making the code easy to understand and modify.

- **Webhook Communication**: LINE, Slack, and WhatsApp chatbots use a webhook for communication, with FastAPI used to build the endpoint.

- **Library Usage**: The Discord bot uses the `pycord` library, the Telegram bot uses the `python-telegram-bot` library, and the Webex bot uses the `webex-bot` library.

- **Docker Support**: The repository includes a Dockerfile for building a Docker image of the chatbots.

# ✨ Usage

Here are the general steps to use the chatbots in this repository:

1. **Clone the Repository**: Clone the `chatbot-collections` repository to your local machine.

2. **Install Dependencies**: Navigate to the specific chatbot directory and install the necessary dependencies. 

For example, if you're using the Slack bot, navigate to the `slack-bot` directory and run `poetry install` to install the dependencies.

3. **Configure the Bot**: Each bot will require some configuration, such as setting up API keys or other credentials. Refer to the [my blog post](https://fishwongy.github.io/post/20240423_chatbot) for specific instructions.


