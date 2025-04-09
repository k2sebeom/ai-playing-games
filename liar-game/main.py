import os
import sys
from src.game import LiarGame, print_box


def main():
    """Main entry point for the Liar Game."""
    # Get config path
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    if not os.path.exists(config_path):
        print("❌ Config file not found!")
        sys.exit(1)

    try:
        # Initialize and run game
        game = LiarGame(config_path)
        results = game.play_game()

        # Print final statistics in a fancy box
        wins = sum(1 for r in results if r.group_won)
        stats = [
            "🏆 GAME COMPLETE! 🎮",
            "",
            f"📊 Final Statistics:",
            f"   • Total Rounds: {len(results)}",
            f"   • Group Wins: {wins}",
            f"   • Liar Wins: {len(results) - wins}",
            "",
            "Thanks for playing! 👋"
        ]
        print_box("\n".join(stats), width=50)

    except Exception as e:
        print("\n" + "="*60)
        print("❌ Error during game execution:")
        print(f"   {str(e)}")
        print("="*60 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
