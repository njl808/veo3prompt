import streamlit as st
import json
import os

# Load data
with open("characters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)
with open("scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

character_names = [c["name"] for c in characters]
scene_names = [s["name"] for s in scenes]

character_dict = {c["name"]: c["description"] for c in characters}
scene_dict = {s["name"]: s["description"] for s in scenes}

st.title("Cardiff Airport Comedy Prompt Builder")

save_file = st.text_input("Save prompts to file (e.g., prompts.txt or prompts.csv)", value="prompts.txt")

scene = st.selectbox("Select Scene", scene_names)
character = st.selectbox("Select Character", character_names)

st.write("**Scene Description:**", scene_dict[scene])
st.write("**Character Description:**", character_dict[character])

dialogue = st.text_area("Enter Character’s Line")

if st.button("Preview Prompt"):
    result = f"Scene: {scene_dict[scene]}\n{character}—{character_dict[character]}\n{character}: {dialogue}"
    st.text_area("Prompt Preview", value=result, height=150)

if st.button("Save Prompt"):
    result = f"Scene: {scene_dict[scene]}\n{character}—{character_dict[character]}\n{character}: {dialogue}\n---\n"
    with open(save_file, "a", encoding="utf-8") as f:
        f.write(result)
    st.success(f"Prompt saved to {save_file}")
