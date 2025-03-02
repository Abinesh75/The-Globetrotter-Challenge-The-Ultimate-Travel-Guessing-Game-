import wikipediaapi
import random
import json

# Set up Wikipedia API with a proper User-Agent
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent="MyGlobetrotterGame/1.0 (contact: abineshab75@gmail.com)",  # Replace with your email or website
    language="en"
)

# List of destinations
destinations = ["Paris", "Tokyo", "Cairo", "New York City", "Sydney", "Rome", "Bangkok", "London", "Dubai", "Rio de Janeiro"]

def get_travel_facts(destination):
    page = wiki_wiki.page(destination)
    if page.exists():
        summary = page.summary.split(". ")[:3]  # Get first 3 sentences as facts
        clues = random.sample(summary, min(2, len(summary)))  # Pick 2 random clues
        return {"destination": destination, "clues": clues, "fun_facts": summary}
    return None

# Generate dataset
dataset = [get_travel_facts(dest) for dest in destinations if get_travel_facts(dest)]

# Save to JSON
with open("expanded_travel_dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4)

print("Dataset saved successfully!")
