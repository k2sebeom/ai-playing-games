import os
import sys
from loguru import logger
from src.game import LiarGame

def setup_logger():
    """Configure logging settings."""
    logger.remove()  # Remove default handler
    
    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )
    
    # Add file handler for persistent logs
    log_file = os.path.join(os.path.dirname(__file__), "game_logs.log")
    logger.add(
        log_file,
        rotation="500 MB",
        retention="10 days",
        level="DEBUG"
    )

def main():
    """Main entry point for the Liar Game."""
    setup_logger()
    logger.info("Starting Liar Game")

    # Get config path
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_path):
        logger.error(f"Config file not found at {config_path}")
        sys.exit(1)

    try:
        # Initialize and run game
        game = LiarGame(config_path)
        num_rounds = game.config['game'].get('num_turns', 1)
        results = game.play_game(num_rounds)

        # Log final statistics
        wins = sum(1 for r in results if r['group_won'])
        logger.info(f"\nGame Complete!")
        logger.info(f"Total Rounds: {len(results)}")
        logger.info(f"Group Wins: {wins}")
        logger.info(f"Liar Wins: {len(results) - wins}")

    except Exception as e:
        logger.error(f"Error during game execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
