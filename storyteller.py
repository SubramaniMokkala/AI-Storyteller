import streamlit as st
from transformers import pipeline

# Load the text generation model (GPT-2 from Hugging Face)
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

# Streamlit UI
st.title("📖 AI-Powered Storyteller (Free Version)")
st.markdown("Enter a prompt, and the AI will generate a short story!")

# User input
prompt = st.text_input("Enter a story prompt (e.g., 'Once upon a time in a magical forest...')")

# Story length slider
length = st.slider("Story Length (words)", min_value=50, max_value=300, step=10, value=150)

# Generate button
if st.button("Generate Story"):
    if prompt:
        with st.spinner("Generating your story... ⏳"):
            story = generator(prompt, max_length=length, num_return_sequences=1)[0]["generated_text"]
            st.subheader("📝 Generated Story")
            st.write(story)
    else:
        st.warning("Please enter a prompt to generate a story!")

st.markdown("---")
st.caption("Powered by Hugging Face GPT-2 | Free & Runs Locally 🚀")
