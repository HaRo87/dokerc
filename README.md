# DokerC - Delphi Planning Poker (Doker) CLI
![DokerC Logo](img/Doker_Logo_DokerC_small.png?raw=true)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Test and deploy package](https://github.com/HaRo87/dokerc/workflows/Test%20and%20deploy%20package/badge.svg)
[![codecov](https://codecov.io/gh/HaRo87/dokerc/branch/main/graph/badge.svg?token=QU0YSFNZQ8)](https://codecov.io/gh/HaRo87/dokerc)

A CLI client for [DokerB](https://github.com/HaRo87/dokerb)

## ⚡️ Install

1. Clone this repository

2. Install a python environment like [Anaconda](https://www.anaconda.com/)

3. Create a new environment and activate it

```bash
conda create -n dokerc python=3.8
```

```bash
conda activate dokerc
```

4. Install the DokerC CLI

```bash
pip install .
```

## Usage

Now you should be able to run it, let's use a simple command to check:

```bash
dok
```

which should print the help:

```bash
Usage: dok [OPTIONS] COMMAND [ARGS]...

  DokerC CLI client for the Delphi Planning Poker Backend

Options:
  --help  Show this message and exit.

Commands:
  estimates  All commands related to estimates
  info       Provides some general info about DokerC
  init       Initialize DokerC - mainly generating the config
  session    All commands related to session handling
  tasks      All commands related to tasks
  users      All commands related to users
```

The first thing you should do is to initialize your client via:

```bash
dok init
```

Provide the requested info and then you should be able to start your 
first session via:

```bash
dok session start
```

which should provide a output like:

```bash
INFO [session] : New session started - token for sharing: 5f785c62a22638f3138585b634da81e2
```

Further info can be found via the `--help` flag.

## ⚠️ License

MIT &copy; [HaRo87](https://github.com/HaRo87).