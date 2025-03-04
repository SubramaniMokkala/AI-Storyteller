import streamlit as st
from story_generator import StoryGenerator
import time

# Set page config MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Storyteller",
    page_icon="📚",
    layout="wide"
)

# Initialize the story generator (may take a moment to load the model)
@st.cache_resource
def load_generator():
    with st.spinner("Loading AI storyteller model... This might take a minute on first run."):
        return StoryGenerator()

story_gen = load_generator()

# App title and description
st.title("🪄 AI-Powered Storyteller")
st.markdown("""
Generate personalized stories based on your ideas using AI technology.
Fill in the form below to create your unique story!
""")

# Create a two-column layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("Story Parameters")
    
    # Genre selection
    genre = st.selectbox(
        "Genre",
        ["Fantasy", "Science Fiction", "Mystery", "Romance", "Adventure", "Comedy"]
    )
    
    # Setting
    setting = st.text_area(
        "Setting",
        placeholder="Describe where and when your story takes place...",
        help="Be detailed about the time period, location, and atmosphere."
    )
    
    # Character creation
    st.subheader("Characters")
    
    # Initialize character state if not present
    if 'num_characters' not in st.session_state:
        st.session_state.num_characters = 1
    
    # Function to add a new character form
    def add_character():
        st.session_state.num_characters += 1
    
    # Display existing character forms and collect data
    characters = []
    for i in range(st.session_state.num_characters):
        col1, col2 = st.columns([1, 3])
        with col1:
            char_name = st.text_input(f"Name", key=f"char_name_{i}")
        with col2:
            char_desc = st.text_area(
                f"Description", 
                key=f"char_desc_{i}", 
                placeholder="Character traits, background, goals...",
                height=100
            )
        
        if char_name and char_desc:
            characters.append({"name": char_name, "description": char_desc})
        
        if i < st.session_state.num_characters - 1:
            st.markdown("---")
    
    # Add character button
    st.button("Add Another Character", on_click=add_character, type="secondary")
    
    # Plot elements
    st.subheader("Plot Elements")
    plot_elements = st.text_area(
        "Key events or themes",
        placeholder="List the main events, conflicts, or themes you want in your story...",
        height=100
    )
    
    # Split plot elements by line
    plot_list = [p.strip() for p in plot_elements.split("\n") if p.strip()]
    
    # Tone selection
    tone = st.selectbox(
        "Tone",
        ["Adventurous", "Mysterious", "Humorous", "Serious", "Whimsical", "Inspirational"]
    )
    
    # Story length limitation note
    st.info("Note: This free version generates shorter stories. For longer, more coherent stories, you would need a more powerful model.")
    
    # Generate button
    generate_button = st.button("Generate My Story", type="primary", use_container_width=True)

# Story display area
with right_col:
    st.header("Your Story")
    
    if generate_button:
        # Check if we have the minimum information needed
        if not setting:
            st.error("Please provide a setting for your story.")
        elif not characters:
            st.error("Please add at least one character with name and description.")
        else:
            # Prepare the inputs
            story_inputs = {
                "genre": genre.lower(),
                "setting": setting,
                "characters": characters,
                "plot_elements": plot_list,
                "tone": tone.lower()
            }
            
            # Show generation in progress
            with st.spinner("Crafting your story... This might take a moment."):
                try:
                    # Generate the story
                    story = story_gen.generate_story(story_inputs)
                    
                    # Improve formatting by adding paragraph breaks
                    story = story.replace(". ", ".\n\n", 5)  # Add some paragraph breaks
                    
                    # Display the story with formatting
                    st.markdown("## Your Story")
                    st.write(story)
                    
                    # Add download option
                    st.download_button(
                        label="Download Story as Text",
                        data=story,
                        file_name=f"{genre.lower()}_story.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating your story: {str(e)}")
                    st.info("You might need to reduce your input complexity or try again.")

# Footer with information
st.markdown("---")
st.markdown("""
**About this application:**

This AI storyteller uses a free, local model (GPT-2) to generate stories based on your inputs. 
Because it uses a free model, the stories may be shorter and less coherent than those from commercial APIs.

**Free Model Limitations:**
- Shorter story length
- May not follow your inputs perfectly
- Less coherent narratives
- First-time model loading may take a minute

*Created for educational purposes. All stories are unique and generated just for you.*
""")