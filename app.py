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
from utils.context_storage_utils import get_vector_index, write_to_knowledge_base, \
get_query_vector, setup_data, write_data, get_context

def print_message_history():
    """
    Print past mesage history in current session
    """
    for message in st.session_state.message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def run_buddy():
    st.title("AIBuddy: Multi-Agent AI Assistant")
    # st.markdown(''':blue[Your Multi-Agent AI assistant]''')
    query_history = []

    index_path = 'metadata/faiss_index.faiss'
    metadata_path = 'metadata/context_history.jsonl'
    if 'index' not in st.session_state:
        st.session_state['index'] = get_vector_index(index_path)
        print(f"session start: {st.session_state['index'].ntotal}")
    

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
        setup_data(metadata_path) # creates metedata jsonl file if not exists

    user_input = st.chat_input("Ask your AgenticAI Buddy ...")

    if user_input:
        # Update Message conversation history:
        st.session_state.message_history.append({"role": "user", "content": user_input})

        # Context Retrieval for RAG
        context = []
        vectors = get_query_vector(user_input)
        distances, indices = st.session_state['index'].search(vectors, 3)
        context = get_context(distances, indices, threshold=0.8)

        # check if relevant context was retrieved
        if len(context) > 0:
            input_with_context = f"Here are some relevant past answers:\n{context}\n\nUser Query: {user_input}"
        else:
            input_with_context = user_input
        
        # query_history.append({"role":"user", "content":user_input}) # without context
        query_history.append({"role":"user", "content":input_with_context}) # with context
        # print(f'query_history:{query_history}')
        # display user's input
        with st.chat_message("user"):
            st.markdown(user_input)

        # agent's response
        with st.chat_message("Agent"):
            with st.spinner("Agent Thinking & Responding"):

                ###
                # this is a non-blocking API call hence used async in backend
                # # result =  get_response(query_history)
                # result = get_response(st.session_state.message_history, thread=st.session_state.conv_thread)

                # without retrieved context
                # result = st.session_state.conv_thread.run(main_agent, st.session_state.message_history)
                
                # with retrieved context 
                result = st.session_state.conv_thread.run(main_agent, query_history)
                # # handle async result request
                if asyncio.iscoroutine(result):
                    result = asyncio.run(result)
                ###

                st.markdown(f'**Agent used: {result.last_agent.name}**')
                st.markdown(result.final_output)

        
        st.session_state.message_history.append({"role": f"assistant", "content": result.final_output})
        print("----------------END OF RESPONSE----------------------")

        # update knowledge base and return vector index
        query_response = f"Query: {user_input}\nResponse: {result.final_output}"
        st.session_state['index'] = write_to_knowledge_base(query_response, index_path)
        write_data({'query': user_input, 'response':result.final_output}, metadata_path)

if __name__ == '__main__':

    run_buddy()