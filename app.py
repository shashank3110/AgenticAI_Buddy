"""
Streamlit app for AIBuddy: Multiagent AI assistant.

Currently supports following specialized agents:
Finance
Education, Job & Career
Health, Sports and Nutrition
"""
import streamlit as st
from utils.agent_utils import get_response
import asyncio


def print_message_history():
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def run_buddy():

    query_history = []
    if "message_history" not in st.session_state:
        st.session_state.message_history = []
    result = None

    print_message_history()

    # Agent chat loop

    user_input = st.chat_input("Ask your AgenticAI Buddy ...")

    if user_input:
        st.session_state.message_history.append({"role": "user", "content": user_input})
        query_history.append({"role":"user", "content":user_input})
        # user's input
        with st.chat_message("user"):
            st.markdown(user_input)

        # agents response
        with st.chat_message("Agent"):
            with st.spinner("Agent Thinking & Responding"):

                result =  get_response(query_history)

                # handle async result request
                if asyncio.iscoroutine(result):
                    result = asyncio.run(result)
                st.markdown(f'**Agent used: {result.last_agent.name}**')
                st.markdown(result.final_output)
        
        st.session_state.message_history.append({"role": "assistant", "content": result.final_output})
        print("----------------END OF RESPONSE----------------------")


if __name__ == '__main__':



    run_buddy()
