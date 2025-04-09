from typing import List, Optional
from loguru import logger
from .ai_client import BedrockClient

class BaseAgent:
    def __init__(self, name: str, model_id: str):
        self.name = name
        self.model_id = model_id
        self.client = BedrockClient()
        logger.info(f"Initialized agent {name} with model {model_id}")

    def _format_prompt(self, role: str, context: str) -> str:
        """Format the prompt for the AI model."""
        return f"""Hi, {self.name}. You are {role} in a Liar Game. In this game, all players are given a topic except for one player (the liar) who receives a different topic.
Players take turns providing words related to their given topic. The goal for the regular players is to identify the liar, while the liar tries to blend in without knowing the main topic.
        
Your response should be clear and direct. When asked to choose a target, use XML tags like <target>Player Name</target>.
When providing a descriptive word, use XML tags like <word>sunny</word>.

{context}

Please provide your response:"""

    def generate_response(self, role: str, context: str) -> str:
        """Generate a response using the Bedrock model."""
        prompt = self._format_prompt(role, context)
        try:
            response = self.client.invoke_model(self.model_id, prompt)
            print(f'{prompt} -> {response}')
            logger.info(f"Agent {self.name} generated response")
            return response.strip()
        except Exception as e:
            logger.error(f"Error generating response for agent {self.name}: {e}")
            raise

    def extract_tagged_content(self, response: str, tag: str) -> Optional[str]:
        """Extract content from XML tags in the response."""
        import re
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, response)
        if match:
            return match.group(1).strip()
        return None

    def provide_word(self, topic: str, previous_words: List[str]) -> str:
        """Provide a descriptive word for the current topic."""
        context = f"""The topic is: {topic}
Words shared by other players: {', '.join(previous_words) if previous_words else 'None'}

Provide ONE descriptive word related to the topic. The word should not be part of the topic itself.

Note that you may be a liar too! If you think you are a liar, provide a word that blends in with others.
Use <word>your_word</word> format. Provide some thoughts on your decision too."""
        
        response = self.generate_response("a player", context)
        word = self.extract_tagged_content(response, "word")
        if not word:
            logger.warning(f"Agent {self.name} provided invalid response format")
            return "invalid_response"
        return word

    def vote_for_liar(self, all_words: dict, topic: str) -> str:
        """Vote for who you think is the liar."""
        context = f"""Now it is time to vote! Here is the list of words listed by players.:

Topic: {topic}

{chr(10).join([f'{player}: {word}' for player, word in all_words.items()])}

Who do you think is the liar? Don't vote for yourself, and respond with the player name in <target>player_name</target> format."""
        
        response = self.generate_response("a player voting", context)
        target = self.extract_tagged_content(response, "target")
        if not target:
            logger.warning(f"Agent {self.name} provided invalid voting format")
            return "invalid_vote"
        return target
