import streamlit as st
from story_generator import generate_story

def main():
    st.title("AI-Powered Storyteller")
    
    # User inputs
    genre = st.selectbox("Choose a genre:", ["Fantasy", "Sci-Fi", "Mystery", "Adventure"])
    character = st.text_input("Enter the main character's name:")
    style = st.selectbox("Choose a writing style:", ["Formal", "Humorous", "Poetic"])
    length = st.selectbox("Select story length:", ["Short", "Medium"])
    
    if st.button("Generate Story"):
        if character.strip() == "":
            st.warning("Please enter a character name.")
        else:
            story = generate_story(genre, character, style, length)
            st.subheader("Your Story:")
            st.write(story)

if __name__ == "__main__":
    main()
