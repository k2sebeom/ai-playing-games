import yaml
import random
from typing import Dict, List
from loguru import logger
from .base_agent import BaseAgent
from .judge_agent import JudgeAgent

class LiarGame:
    def __init__(self, config_path: str):
        """Initialize the game with configuration from yaml file."""
        self.config = self._load_config(config_path)
        self.players: Dict[str, BaseAgent] = {}
        self.judge: JudgeAgent = None
        self.initialize_agents()
        logger.info("Liar Game initialized")

    def _load_config(self, config_path: str) -> dict:
        """Load game configuration from yaml file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info("Loaded configuration file")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise

    def initialize_agents(self):
        """Initialize AI agents from configuration."""
        # Initialize players
        for player_config in self.config['players']:
            name = player_config['name']
            model_id = player_config['model_id']
            self.players[name] = BaseAgent(name, model_id)

        # Initialize judge
        self.judge = JudgeAgent(self.config['judge']['model_id'])
        if self.config['game'].get('topic_genres'):
            self.judge.set_topic_genres(self.config['game']['topic_genres'])

        logger.info(f"Initialized {len(self.players)} players and judge")

    def play_round(self) -> dict:
        """Play a single round of the game."""
        # Generate topics
        main_topic, liar_topic = self.judge.generate_topic_pair()
        
        # Select liar
        liar_name = random.choice(list(self.players.keys()))
        logger.info(f"Selected {liar_name} as the liar")

        # Track words and their order
        all_words = {}
        player_order = list(self.players.keys())
        random.shuffle(player_order)

        # Each player takes turns providing words
        for _ in range(self.config['game']['num_turns']):
            for player_name in player_order:
                player = self.players[player_name]
                is_liar = player_name == liar_name
                topic = liar_topic if is_liar else main_topic
                
                # Show previous words to help with context
                word = player.provide_word(topic, list(all_words.values()), is_liar)
                all_words[player_name] = word
                logger.info(f"{player_name} provided word: {word}")

        # Voting phase
        votes = {}
        for player_name, player in self.players.items():
            vote = player.vote_for_liar(all_words, main_topic)
            votes[player_name] = vote
            logger.info(f"{player_name} voted for {vote}")

        # Get judge's analysis
        analysis = self.judge.evaluate_round(all_words, liar_name, votes)

        # Calculate results
        vote_counts = {}
        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
        
        most_voted = max(vote_counts.items(), key=lambda x: x[1])[0]
        group_won = most_voted == liar_name

        return {
            'main_topic': main_topic,
            'liar_topic': liar_topic,
            'liar': liar_name,
            'words': all_words,
            'votes': votes,
            'most_voted': most_voted,
            'group_won': group_won,
            'analysis': analysis
        }

    def play_game(self, num_rounds: int = 1):
        """Play multiple rounds of the game."""
        results = []
        for round_num in range(num_rounds):
            logger.info(f"Starting round {round_num + 1}")
            round_result = self.play_round()
            results.append(round_result)
            
            # Log round results
            logger.info(f"\nRound {round_num + 1} Results:")
            logger.info(f"Main Topic: {round_result['main_topic']}")
            logger.info(f"Liar Topic: {round_result['liar_topic']}")
            logger.info(f"True Liar: {round_result['liar']}")
            logger.info(f"Words: {round_result['words']}")
            logger.info(f"Votes: {round_result['votes']}")
            logger.info(f"Group {'Won' if round_result['group_won'] else 'Lost'}")
            logger.info(f"Judge's Analysis: {round_result['analysis']}\n")

        return results
