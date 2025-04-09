import yaml
import random
import time
from typing import Dict
from pydantic import BaseModel
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


def print_box(text: str, width: int = 60, padding: int = 1):
    """Print text in a decorative box."""
    horizontal_border = "+" + "-" * (width + padding * 2) + "+"
    empty_line = "|" + " " * (width + padding * 2) + "|"
    
    print(horizontal_border)
    print(empty_line)
    # Handle multi-line text
    for line in text.split('\n'):
        padded_text = line.center(width + padding * 2)
        print(f"|{padded_text}|")
    print(empty_line)
    print(horizontal_border)
    print()


class LiarGame:
    def __init__(self, config_path: str):
        """Initialize the game with configuration from yaml file."""
        self.config = self._load_config(config_path)
        self.players: Dict[str, BaseAgent] = {}
        self.judge: JudgeAgent = None
        self.initialize_agents()
        print_box("🎮 Welcome to the LIAR GAME! 🎭\nLet the deception begin!")

    def _load_config(self, config_path: str) -> dict:
        """Load game configuration from yaml file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            print("Configuration loaded successfully ✨")
            return config
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            raise

    def initialize_agents(self):
        """Initialize AI agents from configuration."""
        # Initialize players
        for player_config in self.config['players']:
            name = player_config['name']
            model_id = player_config['model_id']
            language = self.config['game'].get('language', 'en-US')
            self.players[name] = BaseAgent(name, model_id, language)

        # Initialize judge
        self.judge = JudgeAgent(self.config['judge']['model_id'], language)
        if self.config['game'].get('topic_genres'):
            self.judge.set_topic_genres(self.config['game']['topic_genres'])

        print_box(f"🎯 Game Setup Complete!\n{len(self.players)} clever minds will face off\nwith our mysterious judge watching closely...")

    def play_round(self, prev_topics) -> RoundResult:
        """Play a single round of the game."""
        # Generate topics
        main_topic, liar_topic = self.judge.generate_topic_pair(prev_topics)
        print_box(f"📚 Topics for this round:\n🌟 Main: {main_topic}\n🔮 Liar: {liar_topic}\n", width=50, padding=2)
        prev_topics.append(main_topic)

        # Select liar
        liar_name = random.choice(list(self.players.keys()))
        print("\n" + "="*60)
        print("🎲 The dice of deception have been rolled...")
        time.sleep(1)  # Add dramatic pause
        print("🎭 A player has been chosen to be the LIAR... but who could it be? 🤔")
        print("="*60 + "\n")

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
            # Print game progress
            print(f"{'😈' if player_name == liar_name else '🤔'} {player_name}'s turn...")
            time.sleep(1)
            print(f"   └─ Says: '{word}'")
            print(f"   └─ 💭 Reasoning: {reason}\n")
            # time.sleep(5)

        # Voting phase
        votes = {}
        for player_name, player in self.players.items():
            is_liar = player_name == liar_name
            topic = liar_topic if is_liar else main_topic
            vote, reason = player.vote_for_liar(all_words, topic)

            votes[player_name] = vote
            print(f"🗳️  {player_name} dramatically points at... ", end='')
            time.sleep(0.5)  # Dramatic pause
            print(f"{vote}! *suspenseful music*")
            print(f"   └─ 💭 Reasoning: {reason}\n")

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
        print_box("🎭 THE ULTIMATE GAME OF DECEPTION 🎭")\
        
        results = []
        losers = []
        prev_topics = []

        round_count = 1

        while len(self.players) > 2:
            print("\n" + "="*60)
            print(f"🔄 Round {round_count} - Let the mind games begin! 🎯".center(60))
            print("="*60 + "\n")
            round_result = self.play_round(prev_topics)
            results.append(round_result)
            
            # Log round results
            # Print round results in a fancy box
            result_text = [
                f"🎯 Round {round_count} Results - The Truth Emerges!",
                "",
                f"📝 The Real Topic Was: {round_result.main_topic}",
                f"🎭 The Liar's Secret Topic: {round_result.liar_topic}",
                f"😈 The True Liar Was: {round_result.liar}",
                "",
                "🎲 The Words That Were Played:",
            ]
            
            # Add words section
            for player, word in round_result.words.items():
                if player == round_result.liar:
                    result_text.append(f"   • {player} (The Liar) said: '{word}'")
                else:
                    result_text.append(f"   • {player} said: '{word}'")
            
            result_text.extend([
                "",
                "🗳️ The Accusations:",
            ])
            
            # Add voting section
            for voter, vote in round_result.votes.items():
                result_text.append(f"   • {voter} suspected {vote}")
            
            result_text.extend([
                "",
                "🏆 Final Verdict:",
                "   The group has CAUGHT THE LIAR! 🎉" if round_result.group_won else "   The Liar has FOOLED EVERYONE! 😱"
            ])
            
            print_box("\n".join(result_text), width=70)

            if round_result.group_won:
                print(f"\n👋 {round_result.liar} has been caught and eliminated from the game!")
                print("="*60 + "\n")
                self.players.pop(round_result.liar)
                losers.append(round_result.liar)
            else:
                print(f"\n👋 {round_result.most_voted} has been indicted and eliminated from the game!")
                print("="*60 + "\n")
                self.players.pop(round_result.most_voted)
                losers.append(round_result.most_voted)

            round_count += 1
        print("Winners")
        print([p.name for p in self.players])
        print("Losers")
        print(losers[::-1])
        return results
