# AI Liar Game

An implementation of the Liar Game using AWS Bedrock AI models, where AI agents try to identify the liar among them through word association and deductive reasoning.

## Overview

In this implementation, AI agents powered by AWS Bedrock models play the Liar Game. One agent is randomly chosen as the "Liar" and must blend in while other agents try to identify them. A judge agent manages the game, creates topics, and provides analysis of each round.

## Prerequisites

- Python 3.8+
- AWS EC2 instance with appropriate IAM role for Bedrock access
- AWS Region: us-west-2 (where Bedrock is available)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The game is configured through `config.yaml`. Here's an example configuration:

```yaml
game:
  num_turns: 2  # Number of turns per round
  num_players: 3  # Total number of players
  topic_genres:  # List of topic genres (if empty, random topics will be used)
    - animals
    - countries
    - food
    - sports

players:
  - name: "Player 1"
    model_id: "anthropic.claude-v2"  # Bedrock model ID
  - name: "Player 2"
    model_id: "anthropic.claude-v2"
  - name: "Player 3"
    model_id: "anthropic.claude-v2"

judge:
  model_id: "anthropic.claude-v2"  # Model ID for the judge
```

### Configuration Options

- `game.num_turns`: Number of turns each player gets per round
- `game.num_players`: Total number of players in the game
- `game.topic_genres`: List of genres for topics (optional)
- `players`: List of player configurations
  - `name`: Player's name
  - `model_id`: AWS Bedrock model ID to use for this player
- `judge`: Judge configuration
  - `model_id`: AWS Bedrock model ID to use for the judge

## Running the Game

To start the game:

```bash
python main.py
```

The game will:
1. Load the configuration from `config.yaml`
2. Initialize AI agents for players and judge
3. Run the specified number of rounds
4. Log all interactions and results

## Game Flow

1. **Initialization**
   - Judge generates a topic pair (main topic and liar topic)
   - One player is randomly chosen as the liar
   - Liar receives the liar topic, others receive the main topic

2. **Game Rounds**
   - Players take turns providing descriptive words
   - Each player sees previous words to help with context
   - The liar tries to blend in while others provide relevant words

3. **Voting Phase**
   - Each player votes for who they think is the liar
   - Votes are tallied and results are announced
   - Judge provides analysis of the round

4. **Results**
   - Game shows statistics about group vs liar wins
   - Detailed logs are saved for review

## Logging

The game provides detailed logging:
- Console output shows real-time game progress
- All interactions are saved to `game_logs.log`
- Logs include timestamps and color-coded levels

## AWS Bedrock Models

The game uses AWS Bedrock models for AI agents. Make sure your EC2 instance has the appropriate IAM role with permissions to access Bedrock services.

Currently supported models:
- anthropic.claude-v2
- (Add other Bedrock models as needed)

## Error Handling

The game includes robust error handling:
- Configuration validation
- API error handling
- Fallback mechanisms for topic generation
- Detailed error logging

## Contributing

Feel free to submit issues and enhancement requests!
