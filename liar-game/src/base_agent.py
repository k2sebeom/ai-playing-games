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
        return f"""You are {role} in a Liar Game. {context}
        
Your response should be clear and direct. When asked to choose a target, use XML tags like <target>Player 2</target>.
When providing a descriptive word, use XML tags like <word>sunny</word>.

Current context:
{context}

Please provide your response:"""

    def generate_response(self, role: str, context: str) -> str:
        """Generate a response using the Bedrock model."""
        prompt = self._format_prompt(role, context)
        try:
            response = self.client.invoke_model(self.model_id, prompt)
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

    def provide_word(self, topic: str, previous_words: List[str], is_liar: bool) -> str:
        """Provide a descriptive word for the current topic."""
        context = f"""The topic you {'think you know' if is_liar else 'know'} is: {topic}
Previous words used: {', '.join(previous_words) if previous_words else 'None'}

Provide ONE descriptive word related to the topic. The word should not be part of the topic itself.
Use <word>your_word</word> format."""
        
        response = self.generate_response("a player", context)
        word = self.extract_tagged_content(response, "word")
        if not word:
            logger.warning(f"Agent {self.name} provided invalid response format")
            return "invalid_response"
        return word

    def vote_for_liar(self, all_words: dict, topic: str) -> str:
        """Vote for who you think is the liar."""
        context = f"""Based on the following words provided by each player for the topic '{topic}':

{chr(10).join([f'{player}: {word}' for player, word in all_words.items()])}

Who do you think is the liar? Respond with the player name in <target>player_name</target> format."""
        
        response = self.generate_response("a player voting", context)
        target = self.extract_tagged_content(response, "target")
        if not target:
            logger.warning(f"Agent {self.name} provided invalid voting format")
            return "invalid_vote"
        return target
