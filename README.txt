AarogyaSakhi 2.0 — interactive Streamlit website

DESIGN UPDATE
- Dark plum background with blush pink, lilac, and mint accents (no all-white interface)
- Catchy headings paired with clear workspace labels
- Direct sidebar navigation: selecting a workspace opens it immediately
- Gentle hover transitions, card lift, and button glow
- Friendly copy, emojis, and a clearer privacy note

FILES
- app.py: the website
- requirements.txt: Python packages
- .streamlit/config.toml: dark theme and first-run configuration

RUN ON WINDOWS
1. Extract this ZIP.
2. Open the extracted aarogyasakhi_interactive_v2 folder in VS Code.
3. Open Terminal > New Terminal.
4. Run: py -m pip install -r requirements.txt
5. Run: py -m streamlit run app.py
6. Open the localhost URL shown in the terminal (usually http://localhost:8501).

TRACKER FEATURES
- Add dated symptom entries with pain, fatigue, mood, cycle day, other symptoms, daily impact, and notes.
- View and delete entries in the symptom diary.
- View charts and plain-language summaries based on logged entries.
- Download a CSV of entries and an HTML report that can be printed or saved as PDF.
- Add lab results and include them in the report.
- Health check-in guide, health statistics, and help resources.

PRIVACY AND HEALTH NOTE
Entries are stored in Streamlit's active session only; they are not saved permanently to a database. They may disappear when the session ends or the app restarts. Download the report/CSV if you need to keep demo data. Use fictional data in public demonstrations and avoid entering identifying details. This prototype is educational and does not diagnose or replace medical advice.

Visual refresh: Blush Bloom theme with Playfair Display headings, DM Sans body text, richer rose/lilac accents, hover glow/lift, and reduced-motion-aware entrance transitions.
