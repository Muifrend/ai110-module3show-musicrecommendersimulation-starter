# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**Smoothify**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Smoothify is designed to start with what you like and then continue on a seamless musical journey. It is meant for classroom exploration, not real-world music discovery. It assumes the user wants a playlist that feels connected and easy to listen to, even if the profile is simple.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Smoothify uses the first song to match the user's profile by looking at genre, mood, energy, and acoustic preference. After that, it chooses the next songs based more on smooth transitions, so the playlist flows naturally from one track to the next. The score is built from those song features, with the first pick using the profile most strongly and later picks favoring songs that blend well with the previous one. I kept the idea simple so the recommender feels like it starts with your taste and then keeps the vibe going.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The dataset has 10 songs in data/songs.csv. It includes pop, lofi, rock, ambient, jazz, synthwave, and indie pop, with moods like happy, chill, intense, relaxed, moody, and focused. I did not add or remove songs from the dataset. Some tastes are still missing, like hip-hop, country, classical, and many subgenres, so the catalog is small and not very diverse.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Smoothify excels at making smooth transitions based on the data, even when the user profile is not very detailed. Since it is not that dependent on the profile after the first song, the sequence often feels cohesive and easy to listen to. It works especially well when the goal is a connected vibe instead of strict genre matching.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

During experiments, I noticed that the recommender can create a filter bubble after the first pick because the later songs are chosen mostly for smooth transitions from the previous song, not for matching the user's original preferences. That means a user with unusual or conflicting tastes can get pushed toward a narrow cluster of similar songs even if the rest of the profile says something different. The system also relies on exact genre and mood labels, so users whose preferences do not match the dataset's wording may be ignored or scored too low. Because the catalog is very small, a few songs can dominate each genre and make the rankings look more confident than they really are. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

I tested the High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles, plus three adversarial profiles that mixed conflicting or malformed preferences. The first recommendation usually changed when I changed the user profile, which showed that the profile inputs do affect the opening pick. What surprised me less was that the later recommendations often became similar across very different users, because the system focuses on transition smoothness after the first choice instead of constantly re-checking the full profile. That is not surprising once you look at the scoring rule, because there is no big dissonance between the output and the code: the recommender is doing what it was designed to do.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would make Smoothify prioritize smoothness and the user profile more at the same time, so the playlist stays connected without drifting too far from the listener's taste. I would also add better normalization for text inputs and more ways to compare songs beyond the current features. Another improvement would be making the top results more diverse while still keeping the flow.

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

When data is not inputted correctly then it will result in outputs that are inaccurate, so adding validation and data cleaning is important. Additionally, since my algorithm focuses on smooth transitions this choice heavily influenced subsequent music that was recommended not taking into consideration the user profile, which is a design choice, but whose consequences were large and so more considerations should be taken into account. And additionally, music recommender systems are way more complex then I initially thought and now I am thinking about how much of the heavy lifting is done in the data processing stage and then how much is decided later because some values could be precalculated and have heavy impact on choices and don't need to be calculated realtime and how much of the system is dynamic. 