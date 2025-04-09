import boto3
import logging


def setup_api_logging():
    """Setup logging for API interactions."""
    api_logger = logging.getLogger('api_logger')
    api_logger.setLevel(logging.INFO)
    handler = logging.FileHandler('api_log.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    api_logger.addHandler(handler)
    return api_logger


class BedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.logger = setup_api_logging()
        self.logger.info("Initialized Bedrock client")

    def invoke_model(self, model_id: str, prompt: str) -> str:
        """
        Invoke a Bedrock model with the given prompt using the Converse API.
        """
        try:
            # Log the prompt
            self.logger.info(f"\nPROMPT [{model_id}]:\n{'-'*50}\n{prompt}\n{'-'*50}")
            
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
            
            # Extract the response text
            response_text = response['output']['message']['content'][0]['text']
            
            # Log the response
            self.logger.info(f"\nRESPONSE [{model_id}]:\n{'-'*50}\n{response_text}\n{'-'*50}\n")
            
            return response_text
            
        except Exception as e:
            self.logger.error(f"Error invoking Bedrock model: {e}")
            raise
