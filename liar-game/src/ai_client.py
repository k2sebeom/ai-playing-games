import boto3
import json
from typing import List, Dict, Any
from loguru import logger

class BedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime', region_name='us-west-2')
        logger.info("Initialized Bedrock client")

    def invoke_model(self, model_id: str, prompt: str) -> str:
        """
        Invoke a Bedrock model with the given prompt using the Converse API.
        """
        try:
            # Create message structure for Converse API
            messages = [{
                "role": "user",
                "content": [{"text": prompt}]
            }]

            # Set up inference configuration
            inference_config = {
                "temperature": 1,
                "topP": 0.9
            }

            response = self.client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            
            # Extract the response from the output message
            return response['output']['message']['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Error invoking Bedrock model: {e}")
            raise
