import streamlit as st
from story_generator import StoryGenerator

# Streamlit page config - MUST be the first Streamlit command!
st.set_page_config(page_title="📖 AI Story Generator", layout="wide")

# Instantiate the story generator
story_gen = StoryGenerator()

# Streamlit UI
st.title("📖 AI Story Generator")
st.write("Create unique stories with AI by providing details below.")

# User inputs
genre = st.selectbox("Select a Genre:", ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Horror"])
setting = st.text_input("Story Setting:", "A medieval kingdom")
tone = st.selectbox("Tone of the Story:", ["Adventurous", "Dark", "Humorous", "Inspirational"])

# Character input
st.subheader("Characters")
characters = []
num_chars = st.number_input("Number of Characters:", min_value=0, max_value=5, value=2)

for i in range(num_chars):
    name = st.text_input(f"Character {i+1} Name:", f"Character {i+1}")
    description = st.text_input(f"Character {i+1} Description:", "A brave warrior")
    characters.append({"name": name, "description": description})

# Plot elements
st.subheader("Plot Elements")
plot_elements = []
num_plot_points = st.number_input("Number of Plot Elements:", min_value=0, max_value=5, value=2)

for i in range(num_plot_points):
    plot_element = st.text_input(f"Plot Element {i+1}:", "A hidden treasure")
    plot_elements.append(plot_element)

# Generate story button
if st.button("Generate Story"):
    user_inputs = {
        "genre": genre,
        "setting": setting,
        "tone": tone,
        "characters": characters,
        "plot_elements": plot_elements
    }
    
    with st.spinner("Generating story... ⏳"):
        story = story_gen.generate_story(user_inputs)
        st.subheader("Generated Story:")
        st.write(story)
