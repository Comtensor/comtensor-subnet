import numpy as np
import bittensor as bt
import math

from comtensor.miner.crossvals.subvortex.localisation import (
    compute_localisation_distance,
    get_localisation,
)

# Controls how quickly the tolerance decreases with distance.
SIGMA = 20
# Longest distance between any two places on Earth is 20,010 kilometers
MAX_DISTANCE = 20010

def wilson_score_interval(successes, total):
    if total == 0:
        return 0.5  # chance

    z = 0.6744897501960817

    p = successes / total
    denominator = 1 + z**2 / total
    centre_adjusted_probability = p + z**2 / (2 * total)
    adjusted_standard_deviation = math.sqrt((p * (1 - p) + z**2 / (4 * total)) / total)

    lower_bound = (
        centre_adjusted_probability - z * adjusted_standard_deviation
    ) / denominator
    upper_bound = (
        centre_adjusted_probability + z * adjusted_standard_deviation
    ) / denominator

    wilson_score = (max(0, lower_bound) + min(upper_bound, 1)) / 2

    bt.logging.trace(
        f"Wilson score interval with {successes} / {total}: {wilson_score}"
    )
    return wilson_score


async def compute_reliability_score(uid, database, hotkey: str):
    stats_key = f"stats:{hotkey}"

    # Step 1: Retrieve statistics
    challenge_successes = int(
        await database.hget(stats_key, "challenge_successes") or 0
    )
    challenge_attempts = int(await database.hget(stats_key, "challenge_attempts") or 0)
    bt.logging.trace(f"[{uid}][Score][Reliability] # challenge attempts {challenge_attempts}")
    bt.logging.trace(f"[{uid}][Score][Reliability] # challenge succeeded {challenge_successes}")

    # Step 2: Normalization
    normalized_score = wilson_score_interval(challenge_successes, challenge_attempts)

    return normalized_score


def compute_latency_score(uid, validator_country, response):
    initial_process_times = response[2]
    bt.logging.trace(f"[{uid}][Score][Latency] Process times {initial_process_times}")
    # bt.logging.trace(f"[{uid}][Score][Latency] Process time {initial_process_times[idx]}")

    # Step 1: Get the localisation of the validator
    validator_localisation = get_localisation(validator_country)

    # Step 2: Compute the miners process times by adding a tolerance
    country = response[1]
    process_time = response[2]

    distance = 0
    location = get_localisation(country)
    if location is not None:
        distance = compute_localisation_distance(
            validator_localisation["latitude"],
            validator_localisation["longitude"],
            location["latitude"],
            location["longitude"],
        )

    scaled_distance = distance / MAX_DISTANCE
    tolerance = 1 - scaled_distance

    process_time = process_time * tolerance if process_time else 5
    bt.logging.trace(
        f"[{uid}][Score][Latency] Process times with tolerange {process_time}"
    )

    # Step 3: Baseline Latency Calculation
    baseline_latency = np.mean(process_time)
    bt.logging.trace(f"[{uid}][Score][Latency] Base latency {baseline_latency}")

    # Step 4: Relative Latency Score Calculation
    relative_latency_score = 1 - (process_time / baseline_latency)
    bt.logging.trace(
        f"[{uid}][Score][Latency] Relative scores {relative_latency_score}"
    )

    # # Step 5: Normalization
    # min_score = min(relative_latency_scores)
    # bt.logging.trace(f"[{uid}][Score][Latency] Minimum relative score {min_score}")
    # max_score = max(relative_latency_scores)
    # bt.logging.trace(f"[{uid}][Score][Latency] Maximum relative score {max_score}")
    # score = relative_latency_scores[idx]
    # bt.logging.trace(f"[{uid}][Score][Latency] Relative score {score}")

    # normalized_score = (score - min_score) / (max_score - min_score)

    return relative_latency_score


def compute_distribution_score(response):
    # Step 1: Country of the requested response
    country = response[1]

    # Step 1: Country the number of miners in the country
    count = 0
    if response[1] == country:
        count = count + 1

    # Step 2: Compute the score
    score = 1 / count

    return score
