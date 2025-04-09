from typing import List, Tuple
from loguru import logger
from .base_agent import BaseAgent
import random

class JudgeAgent(BaseAgent):
    def __init__(self, model_id: str):
        super().__init__("Judge", model_id)
        self.topic_genres = []

    def set_topic_genres(self, genres: List[str]):
        """Set available topic genres for the judge to choose from."""
        self.topic_genres = genres
        logger.info(f"Set topic genres: {genres}")

    def generate_topic_pair(self) -> Tuple[str, str]:
        """Generate a pair of related topics - one for players and one for the liar."""
        genre = random.choice(self.topic_genres) if self.topic_genres else "any topic"
        
        context = f"""Generate two related but different topics for a Liar Game. 
If genre is specified, use it: {genre}

The topics should be:
1. Similar enough that some descriptive words could apply to both
2. Different enough that specific words would only apply to one

Provide your response in this format:
<main_topic>topic1</main_topic>
<liar_topic>topic2</liar_topic>"""

        response = self.generate_response("the judge", context)
        main_topic = self.extract_tagged_content(response, "main_topic")
        liar_topic = self.extract_tagged_content(response, "liar_topic")

        if not main_topic or not liar_topic:
            logger.error("Failed to generate valid topic pair")
            return "beach", "desert"  # fallback topics
            
        logger.info(f"Generated topic pair: {main_topic} (main) / {liar_topic} (liar)")
        return main_topic, liar_topic

    def evaluate_round(self, all_words: dict, true_liar: str, votes: dict) -> str:
        """Evaluate the round and provide commentary."""
        context = f"""As the judge, evaluate this round of the Liar Game:

Words provided by each player:
{chr(10).join([f'{player}: {word}' for player, word in all_words.items()])}

Votes cast:
{chr(10).join([f'{player} voted for {vote}' for player, vote in votes.items()])}

The true liar was: {true_liar}

Provide an analysis of the round, including:
1. How well the liar blended in
2. Any particularly suspicious or clever plays
3. The effectiveness of the group's voting

Use <analysis>your_analysis</analysis> format."""

        response = self.generate_response("the judge", context)
        analysis = self.extract_tagged_content(response, "analysis")
        
        if not analysis:
            logger.warning("Judge provided invalid analysis format")
            return "Round complete."
            
        return analysis
