import csv
import json
import random

import streamlit as st
import streamlit.components.v1 as components

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

# Load life advice from CSV
with open("life.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    advice_lines = [row["advice"] for row in reader if row.get("advice")]

# Load special lines from CSV
with open("special.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    special_lines = [row["special"] for row in reader if row.get("special")]

st.title("Cardiff Airport Comedy Prompt Builder")

save_file = st.text_input(
    "Save prompts to file (e.g., prompts.txt or prompts.csv)",
    value="prompts.txt",
)

use_bespoke = st.checkbox("Use bespoke scene")
if use_bespoke:
    bespoke_scene = st.text_area(
        "Bespoke Scene Description", height=80, placeholder="Enter scene"
    )
    scene_desc = bespoke_scene
else:
    scene = st.selectbox("Select Scene", scene_names)
    scene_desc = scene_dict[scene]

character = st.selectbox("Select Character", character_names)
character2 = st.selectbox(
    "Select Second Character (optional)", ["None"] + character_names
)

st.write("**Scene Description:**", scene_desc)
st.write("**Character Description:**", character_dict[character])
if character2 != "None":
    st.write("**Second Character Description:**", character_dict[character2])

include_joke = st.checkbox("Include random joke")
include_advice = st.checkbox("Include random life advice")
include_special = st.checkbox("Include random special")
extra_description = st.text_input(
    "Additional character description (optional)"
)

dialogue = st.text_area("Enter Character’s Line")

if st.button("Preview Prompt"):
    result = (
        f"Scene: {scene_desc}\n" f"{character}—{character_dict[character]}"
    )
    if extra_description.strip():
        result += f" {extra_description.strip()}"
    if character2 != "None":
        result += f"\n{character2}—{character_dict[character2]}"
    result += f"\n{character}: {dialogue}"
    if include_joke and jokes:
        st.session_state.preview_joke = random.choice(jokes)
        result += f"\nJoke: {st.session_state.preview_joke}"
    if include_advice and advice_lines:
        st.session_state.preview_advice = random.choice(advice_lines)
        result += f"\nAdvice: {st.session_state.preview_advice}"
    if include_special and special_lines:
        st.session_state.preview_special = random.choice(special_lines)
        result += f"\nSpecial: {st.session_state.preview_special}"
    st.session_state.preview_result = result
    st.session_state.show_copy = True
    st.text_area("Prompt Preview", value=result, height=200)

if st.session_state.get("show_copy"):
    if st.button("Copy Preview to Clipboard"):
        text = st.session_state.preview_result.replace("`", "\\`")
        components.html(
            f"<script>navigator.clipboard.writeText(`{text}`);</script>",
            height=0,
        )
        st.success("Prompt copied to clipboard")

if st.button("Save Prompt"):
    result = (
        f"Scene: {scene_desc}\n" f"{character}—{character_dict[character]}"
    )
    if extra_description.strip():
        result += f" {extra_description.strip()}"
    if character2 != "None":
        result += f"\n{character2}—{character_dict[character2]}"
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
    if include_advice and advice_lines:
        advice_to_use = st.session_state.get(
            "preview_advice"
        ) or random.choice(advice_lines)
        result += f"\nAdvice: {advice_to_use}"
    if include_special and special_lines:
        special_to_use = st.session_state.get(
            "preview_special"
        ) or random.choice(special_lines)
        result += f"\nSpecial: {special_to_use}"
    result += "\n---\n"
    with open(save_file, "a", encoding="utf-8") as f:
        f.write(result)
    st.success(f"Prompt saved to {save_file}")
