This Python script processes JSON files containing company and user data, applying token top-ups and generating a detailed output file based on specific business rules.

## Prerequisites

- Python 3.8+
- Required libraries:
  - `json`
  - `os`
  - `logging`
  - `argparse`

## Installation

1. Clone the repository
```bash
git clone https://github.com/ibadrehman90/thrive-task.git
cd thrive-task
```
## Usage

### Basic Usage
```bash
python challenge.py
```

### Custom JSON Files
```bash
python challenge.py --companies custom_companies.json --users custom_users.json
```

## Command Line Arguments

| Argument     | Description                | Default           |
|--------------|----------------------------|-------------------|
| `--companies`| Path to companies JSON file| `companies.json`  |
| `--users`    | Path to users JSON file    | `users.json`      |