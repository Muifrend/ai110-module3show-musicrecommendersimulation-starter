"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Works when executed as a module: python -m src.main
    from .recommender import load_songs, recommend_songs
except ImportError:
    # Works when executed as a script: python src/main.py
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations\n" + "=" * 20)
    for idx, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec

        label = explanation
        reasons = []
        if ": " in explanation:
            label, reasons_blob = explanation.split(": ", 1)
            reasons = [reason.strip() for reason in reasons_blob.split("; ") if reason.strip()]

        print(f"\n{idx}. {song['title']}")
        if idx == 1:
            print(f"   Profile Score: {score:.2f}")
        else:
            prev_song = recommendations[idx - 2][0]
            print(f"   Transition Score from {prev_song['title']}: {score:.2f}")
        print(f"   Type: {label}")
        print("   Reasons:")
        if reasons:
            for reason in reasons:
                print(f"   - {reason}")
        else:
            print("   - No detailed reasons provided")


if __name__ == "__main__":
    main()
