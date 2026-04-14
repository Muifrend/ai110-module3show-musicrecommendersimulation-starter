import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV, converting numeric fields to int/float types."""
    int_fields = {"id", "key", "duration_sec"}
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "loudness_db",
        "instrumentalness",
        "speechiness",
        "bpm_confidence",
        "beat_strength",
        "energy_start",
        "energy_end",
    }

    songs: List[Dict] = []

    try:
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    for field in int_fields:
                        if field in row and row[field] != "":
                            row[field] = int(row[field])

                    for field in float_fields:
                        if field in row and row[field] != "":
                            row[field] = float(row[field])

                    songs.append(row)
                except ValueError:
                    # Skip malformed rows so one bad value does not block all loading.
                    continue
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Songs file not found: {csv_path}") from exc

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs


def score_song(
    user_prefs: Dict, song: Dict, last_song: Optional[Dict] = None
) -> Tuple[float, List[str]]:
    """Return a song score and reason list from profile or transition criteria."""
    if last_song is None:
        score = 0.0
        reasons: List[str] = []

        genre_points = 2.0
        mood_points = 1.5
        energy_points_max = 2.5
        acoustic_points = 1.0

        if song.get("genre", "").lower() == str(user_prefs.get("genre", "")).lower():
            score += genre_points
            reasons.append(f"genre match (+{genre_points:.1f})")

        if song.get("mood", "").lower() == str(user_prefs.get("mood", "")).lower():
            score += mood_points
            reasons.append(f"mood match (+{mood_points:.1f})")

        energy_target = float(user_prefs.get("energy", 0.5))
        energy_gap = abs(float(song.get("energy", 0.5)) - energy_target)
        energy_bonus = max(0.0, 1.0 - energy_gap) * energy_points_max
        score += energy_bonus
        reasons.append(
            f"energy closeness (target={energy_target:.2f}, gap={energy_gap:.2f}) (+{energy_bonus:.2f})"
        )

        likes_acoustic = user_prefs.get("likes_acoustic")
        if isinstance(likes_acoustic, bool):
            acoustic_value = float(song.get("acousticness", 0.0))
            acoustic_match = (likes_acoustic and acoustic_value >= 0.5) or (
                (not likes_acoustic) and acoustic_value < 0.5
            )
            if acoustic_match:
                score += acoustic_points
                reasons.append(f"acoustic preference match (+{acoustic_points:.1f})")

        return score, reasons

    # Transition-first scoring for songs 2..K.
    reasons: List[str] = []
    tempo_scale = 200.0
    distance = 0.0
    energy_gap = abs(
        float(song.get("energy", 0.0)) - float(last_song.get("energy", 0.0))
    )
    tempo_gap = (
        abs(float(song.get("tempo_bpm", 0.0)) - float(last_song.get("tempo_bpm", 0.0)))
        / tempo_scale
    )
    valence_gap = abs(
        float(song.get("valence", 0.0)) - float(last_song.get("valence", 0.0))
    )
    dance_gap = abs(
        float(song.get("danceability", 0.0)) - float(last_song.get("danceability", 0.0))
    )
    acoustic_gap = abs(
        float(song.get("acousticness", 0.0)) - float(last_song.get("acousticness", 0.0))
    )

    distance += energy_gap * 0.30
    distance += tempo_gap * 0.25
    distance += valence_gap * 0.15
    distance += dance_gap * 0.15
    distance += acoustic_gap * 0.15

    score = max(0.0, 1.0 - distance) * 100.0
    reasons.append(f"energy transition gap={energy_gap:.2f} (weight 0.30)")
    reasons.append(f"tempo transition gap={tempo_gap:.2f} (weight 0.25)")
    reasons.append(f"valence transition gap={valence_gap:.2f} (weight 0.15)")
    reasons.append(f"danceability transition gap={dance_gap:.2f} (weight 0.15)")
    reasons.append(f"acousticness transition gap={acoustic_gap:.2f} (weight 0.15)")
    reasons.append(f"transition score (+{score:.2f})")
    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Generate top-k recommendations using profile-first then transition-first ranking."""
    if not songs or k <= 0:
        return []

    target_k = min(k, len(songs))
    recommendations: List[Tuple[Dict, float, str]] = []

    # Phase 1: Choose the first song from user profile preferences.
    first_song, first_score, first_reasons = max(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: item[1],
    )
    first_explanation = "Profile-based first pick: " + "; ".join(first_reasons)
    recommendations.append((first_song, first_score, first_explanation))

    remaining = [song for song in songs if song is not first_song]
    last_song = first_song

    # Phase 2: Fill remaining slots by transition quality from the last selected song.
    while len(recommendations) < target_k and remaining:
        scored_candidates = sorted(
            ((song, *score_song(user_prefs, song, last_song)) for song in remaining),
            key=lambda item: item[1],
            reverse=True,
        )
        next_song, next_score, next_reasons = scored_candidates[0]
        next_explanation = "Transition-first pick: " + "; ".join(next_reasons)
        recommendations.append((next_song, next_score, next_explanation))
        remaining.remove(next_song)
        last_song = next_song

    return recommendations
