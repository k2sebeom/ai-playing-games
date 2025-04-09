import yaml
import random
import time
from typing import Dict
from pydantic import BaseModel
from loguru import logger
from .base_agent import BaseAgent
from .judge_agent import JudgeAgent


class RoundResult(BaseModel):
    main_topic: str
    liar_topic: str
    liar: str
    words: Dict[str, str]
    votes: Dict[str, str]
    most_voted: str
    group_won: bool


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

    def play_round(self) -> RoundResult:
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

        # Each player provides a word for this round
        for player_name in player_order:
            player = self.players[player_name]
            is_liar = player_name == liar_name
            topic = liar_topic if is_liar else main_topic
            
            # Show previous words to help with context
            word, reason = player.provide_word(topic, list(all_words.values()))
            all_words[player_name] = word
            logger.info(f"{player_name} provided word: {word}\nReason: {reason}")
            time.sleep(5)

        # Voting phase
        votes = {}
        for player_name, player in self.players.items():
            is_liar = player_name == liar_name
            topic = liar_topic if is_liar else main_topic
            vote = player.vote_for_liar(all_words, topic)

            votes[player_name] = vote
            logger.info(f"{player_name} voted for {vote}")

        # Calculate results
        vote_counts = {}
        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1
        
        most_voted = max(vote_counts.items(), key=lambda x: x[1])[0]
        group_won = most_voted == liar_name

        return RoundResult(
            main_topic=main_topic,
            liar_topic=liar_topic,
            liar=liar_name,
            words=all_words,
            votes=votes,
            most_voted=most_voted,
            group_won=group_won,
        )

    def play_game(self):
        """Play multiple rounds of the game."""
        logger.info("Starting Liar Game")\
        
        results = []

        round = 1

        while len(self.players) > 1:
            logger.info(f'Round {round} start!')
            round_result = self.play_round()
            results.append(round_result)
            
            # Log round results
            logger.info(f"\nRound {round} Results:")
            logger.info(f"Main Topic: {round_result.main_topic}")
            logger.info(f"Liar Topic: {round_result.liar_topic}")
            logger.info(f"True Liar: {round_result.liar}")
            logger.info(f"Words: {round_result.words}")
            logger.info(f"Votes: {round_result.votes}")
            logger.info(f"Group {'Won' if round_result.group_won else 'Lost'}")

            if round_result.group_won:
                logger.info(f"{round_result.liar} is eliminated!")
                self.players.pop(round_result.liar)

        return results
