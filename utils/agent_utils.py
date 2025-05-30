"""
Utility Script for AI Agent workflow.
"""
import os
import openai
from agents import Agent, Runner, WebSearchTool, function_tool, ModelSettings
from dataclasses import dataclass, asdict
from agents import set_default_openai_key
import json
import asyncio
from utils.ai_agents import main_agent
import streamlit as st

# set api keys
try:
    # locally
    api_key = os.getenv("OPENAI_API_KEY")
except:
    # streamlit cloud
    api_key = st.secrets["OPENAI_API_KEY"]

set_default_openai_key(api_key, use_for_tracing=False)


def get_conv_session_runner():
    """
    Initialize Runner object at start of the session.
    """
    return Runner()

async def get_response(input, thread):
    result = await Runner.run(main_agent, input=input, thread=thread)
    return result



