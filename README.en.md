# aiwolf-nlp-agent

[README in Japanese](/README.md)

This is a sample agent for the AIWolf Competition (Natural Language Division).

> [!IMPORTANT]
> Please refer to [aiwolfdial.github.io](https://aiwolfdial.github.io/aiwolf-nlp/) for the latest information.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Environment Setup](#environment-setup)
  - [Using uv](#using-uv)
  - [Without uv](#without-uv)
- [How to Run](#how-to-run)
  - [Running the Agent](#running-the-agent)
    - [How to Start with a Specific Configuration File](#how-to-start-with-a-specific-configuration-file)
  - [Running in Local Environment](#running-in-local-environment)
  - [How to Battle in Preliminaries](#how-to-battle-in-preliminaries)
  - [How to Battle in Finals](#how-to-battle-in-finals)
- [Configuration (config/config.yml)](#configuration-configconfigyml)
  - [web_socket](#web_socket)
  - [agent](#agent)
  - [log](#log)
    - [log.requests](#logrequests)
- [How to Customize Agents](#how-to-customize-agents)
  - [Common to All Roles (src/agent/agent.py)](#common-to-all-roles-srcagentagentpy)
    - [Methods Corresponding to Requests](#methods-corresponding-to-requests)
  - [Werewolf (src/agent/werewolf.py)](#werewolf-srcagentwerewolfpy)
  - [Possessed (src/agent/possessed.py)](#possessed-srcagentpossessedpy)
  - [Seer (src/agent/seer.py)](#seer-srcagentseerpy)
    - [How to Get Divination Results](#how-to-get-divination-results)
  - [Bodyguard (src/agent/bodyguard.py)](#bodyguard-srcagentbodyguardpy)
  - [Villager (src/agent/villager.py)](#villager-srcagentvillagerpy)
  - [Medium (src/agent/medium.py)](#medium-srcagentmediumpy)
    - [How to Get Medium Results](#how-to-get-medium-results)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

For werewolf game rules including roles and flow, please refer to [logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/logic.md).

Competition participants need to implement agents and run them on their own terminals to connect to the game server provided by the competition organizers. There are no restrictions on agent implementation, including the programming language.
For self-play, you can run 5 or 13 agents on your own terminal and connect to the self-play game server provided by the competition organizers to battle between agents.

For game servers for local testing and self-play, please refer to [aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server).

## Environment Setup

> [!IMPORTANT]
> Python 3.11 or higher is required.

### Using uv

```bash
git clone https://github.com/aiwolfdial/aiwolf-nlp-agent.git
cd aiwolf-nlp-agent
cp config/config.yml.example config/config.yml
uv sync
```

When using uv, replace `python src/main.py` with `uv run src/main.py` in the instructions below.

### Without uv

```bash
git clone https://github.com/aiwolfdial/aiwolf-nlp-agent.git
cd aiwolf-nlp-agent
cp config/config.yml.example config/config.yml
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> [!NOTE]
> aiwolf-nlp-common is a Python package that defines programs related to roles and connection methods.
> For details, please refer to [aiwolfdial/aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common).

## How to Run

### Running the Agent

```bash
python src/main.py
```

#### How to Start with a Specific Configuration File

By default, it starts by referring to the settings in `config/config.yml`.
Methods for specifying and starting, or running multiple configuration files simultaneously are as follows:

```bash
python src/main.py -c config/config_1.yml # To specify config/config_1.yml
python src/main.py -c config/config_1.yml config/config_2.yml # To specify config/config_1.yml and config/config_2.yml
python src/main.py -c config/config_*.yml # To specify config/config_*.yml
```

### Running in Local Environment

You need to start the game server in advance.
Please refer to [aiwolfdial/aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server).

### How to Battle in Preliminaries

You can battle by connecting to the address published on Slack that you will be invited to after registration.
Please change the relevant items in [Configuration](#web_socket) and then run the agent.

### How to Battle in Finals

You can battle by connecting to the address published on Slack that you will be invited to after registration.
In the finals, please set `web_socket.auto_reconnect` to `true`.
Please change the relevant items in [Configuration](#web_socket) and then run the agent.
Due to battle situations, there may be times when the competition management server is stopped, so connection errors (`[Errno 61] Connection refused`) may occur and automatic reconnection may be repeated.

## Configuration (config/config.yml)

### web_socket

`url`: The URL of the game server. If connecting to a local game server, the default value is fine.
`token`: The token for connecting to the game server. Please set the token provided by the competition organizers.
`auto_reconnect`: Setting for whether to automatically reconnect after a battle ends.

### agent

`num`: The number of agents to start. For self-play, the default value is fine.
`team`: The team name of the agent. Please set the team name provided by the competition organizers.
`kill_on_timeout`: Setting for whether to interrupt request processing on action timeout.

### log

`console_output`: Setting for whether to output logs to the console.
`file_output`: Setting for whether to output logs to files.
`output_dir`: The path to the directory where logs are saved.
`level`: The log output level. Set one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

#### log.requests

`name`, `initialize`, `daily_initialize`, `whisper`, `talk`, `daily_finish`, `divine`, `guard`, `vote`, `attack`, `finish`: Settings for whether to output logs for each request.

## How to Customize Agents

### Common to All Roles (src/agent/agent.py)

This file defines behaviors common to all roles.

#### Methods Corresponding to Requests

Methods corresponding to requests sent from the game server are as follows:

| Method Name        | Change Recommendation | Process                                        |
| ------------------ | --------------------- | ---------------------------------------------- |
| `name`             | **Not Recommended**   | Returns response to name request               |
| `initialize`       | **Medium**            | Performs initialization for game start request |
| `daily_initialize` | **Medium**            | Performs processing for day start request      |
| `talk`             | **High**              | Returns response to talk request               |
| `daily_finish`     | **Medium**            | Performs processing for day end request        |
| `divine`           | **High**              | Returns response to divination request         |
| `vote`             | **High**              | Returns response to vote request               |
| `finish`           | **Medium**            | Performs processing for game end request       |

### Werewolf (src/agent/werewolf.py)

This file defines the behavior of werewolves.
In addition to behaviors common to all roles, it has the following methods:

| Method Name | Change Recommendation | Process                             |
| ----------- | --------------------- | ----------------------------------- |
| `whisper`   | **High**              | Returns response to whisper request |
| `attack`    | **High**              | Returns response to attack request  |

### Possessed (src/agent/possessed.py)

This file defines the behavior of the possessed.

### Seer (src/agent/seer.py)

This file defines the behavior of the seer.
In addition to behaviors common to all roles, it has the following methods:

| Method Name | Change Recommendation | Process                                |
| ----------- | --------------------- | -------------------------------------- |
| `divine`    | **High**              | Returns response to divination request |

#### How to Get Divination Results

They can be obtained from `info.divine_result` in the day start request after the divination phase.
For details, please refer to [judge.py](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py).

### Bodyguard (src/agent/bodyguard.py)

This file defines the behavior of the bodyguard.
In addition to behaviors common to all roles, it has the following methods:

| Method Name | Change Recommendation | Process                           |
| ----------- | --------------------- | --------------------------------- |
| `guard`     | **High**              | Returns response to guard request |

### Villager (src/agent/villager.py)

This file defines the behavior of the villager.

### Medium (src/agent/medium.py)

This file defines the behavior of the medium.

#### How to Get Medium Results

They can be obtained from `info.medium_result` in the day start request after the exile phase.
For details, please refer to [judge.py](https://github.com/aiwolfdial/aiwolf-nlp-common/blob/main/src/aiwolf_nlp_common/packet/judge.py).
