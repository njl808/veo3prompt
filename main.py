import csv
import json
import random

import streamlit as st

# Load character and scene data
with open("characters.json", encoding="utf-8") as f:
    characters = json.load(f)
with open("scenes.json", encoding="utf-8") as f:
    scenes = json.load(f)

character_names = [c["name"] for c in characters]
scene_names = [s["name"] for s in scenes]

character_dict = {c["name"]: c["description"] for c in characters}
scene_dict = {s["name"]: s["description"] for s in scenes}

# Load jokes from CSV
with open("one.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    jokes = [row["joke"] for row in reader if row.get("joke")]

st.title("Cardiff Airport Comedy Prompt Builder")

save_file = st.text_input(
    "Save prompts to file (e.g., prompts.txt or prompts.csv)",
    value="prompts.txt",
)

scene = st.selectbox("Select Scene", scene_names)
character = st.selectbox("Select Character", character_names)

st.write("**Scene Description:**", scene_dict[scene])
st.write("**Character Description:**", character_dict[character])

include_joke = st.checkbox("Include random joke")
extra_description = st.text_input(
    "Additional character description (optional)"
)

dialogue = st.text_area("Enter Character’s Line")

if st.button("Preview Prompt"):
    result = (
        f"Scene: {scene_dict[scene]}\n"
        f"{character}—{character_dict[character]}"
    )
    if extra_description.strip():
        result += f" {extra_description.strip()}"
    result += f"\n{character}: {dialogue}"
    if include_joke and jokes:
        st.session_state.preview_joke = random.choice(jokes)
        result += f"\nJoke: {st.session_state.preview_joke}"
    st.text_area("Prompt Preview", value=result, height=200)

if st.button("Save Prompt"):
    result = (
        f"Scene: {scene_dict[scene]}\n"
        f"{character}—{character_dict[character]}"
    )
    if extra_description.strip():
        result += f" {extra_description.strip()}"
    result += f"\n{character}: {dialogue}"
    joke_to_use = None
    if include_joke and jokes:
        joke_to_use = st.session_state.get("preview_joke") or random.choice(
            jokes
        )
        result += f"\nJoke: {joke_to_use}"
        if joke_to_use in jokes:
            jokes.remove(joke_to_use)
            with open("one.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["joke"])
                writer.writeheader()
                for j in jokes:
                    writer.writerow({"joke": j})
        st.session_state.preview_joke = ""
    result += "\n---\n"
    with open(save_file, "a", encoding="utf-8") as f:
        f.write(result)
    st.success(f"Prompt saved to {save_file}")
