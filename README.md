# Cardiff Airport Comedy Prompt Builder

This project provides a small [Streamlit](https://streamlit.io/) app for creating dialogue prompts.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run main.py
   ```

The app lets you pick a scene and character from the included JSON files and compose a line of dialogue. Check **Use bespoke scene** to type your own setting instead of selecting from the list.

Tick **Include random joke** to add a line from `one.csv`; used jokes are removed so they don't repeat. Tick **Include random life advice** to insert a line from `life.csv`.

Tick **Include random special** to add a quick tip from `special.csv`.

You can enter an optional character description that will be appended to the prompt and select a second character to appear in the scene.

Prompts can be previewed in the browser and saved to a text or CSV file of your choice.
After previewing, click **Copy Preview to Clipboard** to copy the text for use elsewhere.
