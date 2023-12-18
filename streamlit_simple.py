# Library
import openai
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from src.content_processor import Knowledge_base, Text_processor
from src.finetune_functions import create_message_for_finetune, get_answer_from_finetune
from src.RAG_functions import answer_idk, get_answer_from_chain, create_rag_chain
from src.utils import check_openai_api_key

# Create LLM
# RAG bot


def create_knowledge_base():
    text_processor = Text_processor("./content")
    knowledge_base = text_processor.load_knowledge_base("knowledge_base/knowledge_base_index")
    return knowledge_base

def display_intro():
    st.sidebar.title("Eyyo You got super :broccoli: here")
    st.sidebar.write("Roses are red,")
    st.sidebar.write("violets are blue")
    st.sidebar.write("Let me introduce you to a chatbot that’s here for you")
    st.sidebar.write("We get shit done here, no bullshit and I ain't mess around. Move your A$$ and lets loose weight bud")
    st.sidebar.markdown('---') 
    
def main():
     # Custom Streamlit app title and icon
    st.set_page_config(
        page_title="Tols",
        page_icon=":fire:",
    )
    
    if "api_key" not in st.session_state:
        st.title('API Key Validation')

        api_key = st.text_input("Enter API Key", "")

        # Check if the API key is incorrect or empty
        if not api_key:
            st.warning("Please enter a valid API key.")
            return
        elif not check_openai_api_key(api_key):
            st.warning("Incorrect API key. Please enter the correct API key.")
            return
        else:
            # If the API key is correct, show success message and set the API key in session state
            st.success("API key validated. You can proceed.")
            openai.api_key = api_key
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state["api_key"] = api_key
    
   

    display_intro()
    
    # Initialize Chat Messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    full_response = ""
        
    # Set the title
    st.title("Brocco_lee - a bud who cares :broccoli:")

    with st.sidebar.expander("ℹ️ Help :dark_sunglasses:"):
        st.write(
            "Hey, I am a wizzard at:\n\n"
            "1. Your goddamn fast food.\n"
            "2. Your soon-to-be lean food.\n"
            "3. All the nutrients in the world, I mean, in the total world, no doubt.\n\n"
            "P.S: get more :heart: with the option Finetune in config"
        )
    
    # Sidebar Configuration
    st.sidebar.title("Config")

    # Model Name Selector
    model_name = st.sidebar.selectbox(
        "Pick a model",
        ["RAG", "Finetune"]
    )

    if "model" not in st.session_state:
        model = model_name
    
    # init chain
    # Initialize Chat Messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Init RAG chain
    if "rag_chain" not in st.session_state:
        rag_chain = create_rag_chain()
        st.session_state["rag_chain"] = rag_chain
        # Init knowledgebase
        if "knowledge_base" not in st.session_state:
            knowledge_base = create_knowledge_base()
            st.session_state["knowledge_base"] = knowledge_base

    # Initialize DataFrame to store chat history
    chat_history_df = pd.DataFrame(columns=["Timestamp", "Chat"])

    # Reset Button
    if st.sidebar.button("Reset Chat"):
        # Save the chat history to the DataFrame before clearing it
        if "messages" in st.session_state and st.session_state.messages != []:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat_history = "\n".join(
                [f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            new_entry = pd.DataFrame(
                {"Timestamp": [timestamp], "Chat": [chat_history]})
            chat_history_df = pd.concat(
                [chat_history_df, new_entry], ignore_index=True)

            # Save the DataFrame to a CSV file
            chat_history_df.to_csv("chat_history.csv", index=False)

        # Clear the chat messages and reset the full response
        st.session_state.messages = []
        full_response = ""

    image_path = "pepe.png"  # Replace with your local image path

    with st.sidebar:
        st.image(image_path, width=200)
        st.write("## From :broccoli: with :heart:")
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input and AI Response
    if prompt := st.chat_input("Eyyo bud, how are you feeling today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if model_name == "RAG":
                response = get_answer_from_chain(st.session_state["rag_chain"], 
                                  st.session_state["knowledge_base"], prompt)
            else:
                messages = create_message_for_finetune(prompt)
                response = get_answer_from_finetune(messages)
                
            # Create replying effect
        message_placeholder = st.empty()
        for word in response.split():
            time.sleep(0.1)  # issue, add time sleep hid the first answer
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})

if __name__ == "__main__":
    main()