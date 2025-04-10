# AI Playing Games

A collection of AI-powered implementations of classic tabletop and party games, where AI agents compete against each other using large language models.

## Games

### 1. Liar Game
A deception-based word association game where AI agents try to identify the liar among them. The game uses AWS Bedrock models to power the AI agents, including:
- Multiple player agents who provide word associations
- A designated liar who must blend in
- A judge agent who manages the game and analyzes rounds

[Learn more about the Liar Game](./liar-game/README.md)

### 2. Mafia Game
A social deduction party game implementation where AI agents play as either Citizens or Mafia members. Features include:
- Multiple roles (Citizens, Mafia, Doctor, Detective, etc.)
- Day/Night cycle gameplay
- Complex social dynamics and voting systems
- Moderator-guided gameplay

[Learn more about the Mafia Game](./mafia-game/README.md)

## Project Structure

```
ai-playing-games/
├── liar-game/           # Liar Game implementation
│   ├── config.yaml      # Game configuration
│   ├── src/            # Source code
│   └── README.md       # Game-specific documentation
│
└── mafia-game/         # Mafia Game implementation
    └── README.md       # Game-specific documentation
```

## Prerequisites

- Python 3.8+
- AWS account with Bedrock access (for Liar Game)
- Required dependencies listed in each game's requirements.txt

## Getting Started

1. Clone this repository
2. Navigate to the specific game directory you want to try
3. Follow the game-specific README instructions for setup and gameplay

## Implementation Details

Each game is implemented as a standalone module with its own configuration and requirements. The games showcase different approaches to AI-powered gameplay:

- **Liar Game**: Focuses on natural language processing and word associations using AWS Bedrock models
- **Mafia Game**: Emphasizes social deduction and complex role-based interactions

## Contributing

Feel free to:
- Submit issues for bugs or enhancement requests
- Add new game implementations
- Improve existing games
- Enhance documentation
