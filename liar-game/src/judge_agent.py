from typing import List, Tuple
from .base_agent import BaseAgent
import random


class JudgeAgent(BaseAgent):
    def __init__(self, model_id: str, language: str):
        super().__init__("Judge", model_id, language)
        self.topic_genres = []

    def set_topic_genres(self, genres: List[str]):
        """Set available topic genres for the judge to choose from."""
        self.topic_genres = genres
        print(f"🎲 Judge will choose from these genres: {', '.join(genres)}")

    def generate_topic_pair(self, previous_topics: List[str]) -> Tuple[str, str]:
        """Generate a pair of related topics - one for players and one for the liar."""
        genre = random.choice(self.topic_genres) if self.topic_genres else "any topic"

        context = f"""Generate two related but different topics for a Liar Game. 
The genre is: {genre}

The topics should be:
1. Similar enough that some descriptive words could apply to both
2. Different enough that specific words would only apply to one

Provide your response in this format:
<main_topic>topic1</main_topic>
<liar_topic>topic2</liar_topic>

Be creative! And refrain from using previously used topics: {','.join(previous_topics)}
"""

        response = self.generate_response("the judge", context)
        main_topic = self.extract_tagged_content(response, "main_topic")
        liar_topic = self.extract_tagged_content(response, "liar_topic")

        if not main_topic or not liar_topic:
            print("❌ Failed to generate valid topic pair, using fallback topics")
            return "beach", "desert"  # fallback topics

        return main_topic, liar_topic
