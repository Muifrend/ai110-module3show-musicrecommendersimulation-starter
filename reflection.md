# Reflection

## Profile Pair Comparisons

- High-Energy Pop vs Adversarial: High-Energy Sad Acoustic: 
the mood and energy differs from the normal pop profile which is why the initial songs were different

- Chill Lofi vs Adversarial: Acoustic Type Confusion: 
the likes_acoustic value was not a boolean in the adverserial profile, which is why it got skipped and so it focused on genre and energy

- Deep Intense Rock vs Adversarial: Out-of-Range and Noisy Text:
the adverserial profile had extra spaces and wrong cases which made the matching fail and since the energy value was out of range the adverserial choice was pretty random

For all of them however after the initial choice the subsequent matches were correct as they focused on how similar the tracks were and not on user profile.

