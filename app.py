"""
Streamlit app for AIBuddy: Multiagent AI assistant.

Currently supports following specialized agents:
Finance
Education, Job & Career
Health, Sports and Nutrition
Travel, Adventure and Exploration
"""
import streamlit as st
from utils.agent_utils import get_response, get_conv_session_runner
import asyncio
from utils.ai_agents import main_agent
from utils.ai_agents import welcome_prompt

def print_message_history():
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def run_buddy():
    st.title("AIBuddy: Your Multi-Agent AI assistant")
    # st.markdown(''':blue[Your Multi-Agent AI assistant]''')
    query_history = []

    # start session thread for agent
    if "conv_thread" not in st.session_state:
        st.session_state.conv_thread = get_conv_session_runner()
    if "message_history" not in st.session_state:
        st.session_state.message_history = []
    result = None

    print_message_history()



    # Agent chat loop

    # welcome prompt - runs first time every session
    if len(st.session_state.message_history) == 0:
        result = st.session_state.conv_thread.run(main_agent, welcome_prompt)
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
        st.markdown(result.final_output)

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

                ###
                # this is a non-blocking API call hence used async in backend
                # # result =  get_response(query_history)
                # result = get_response(st.session_state.message_history, thread=st.session_state.conv_thread)
                result = st.session_state.conv_thread.run(main_agent, st.session_state.message_history)
                # # handle async result request
                if asyncio.iscoroutine(result):
                    result = asyncio.run(result)
                ###

                st.markdown(f'**Agent used: {result.last_agent.name}**')
                st.markdown(result.final_output)
        
        st.session_state.message_history.append({"role": f"assistant", "content": result.final_output})
        print("----------------END OF RESPONSE----------------------")


if __name__ == '__main__':

    run_buddy()