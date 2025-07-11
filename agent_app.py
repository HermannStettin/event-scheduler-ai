# agent_streamlit.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from agent_tools import all_tools

# Initialize environment and session state
load_dotenv()


def initialize_agent():
    """Initialize the AI agent and executor (cached for performance)"""
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a helpful assistant with calendar management tools. "
         "**Important Rule: If event duration isn't specified, assume 1 hour.**"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    agent = create_tool_calling_agent(llm, all_tools, prompt)
    return AgentExecutor(agent=agent, tools=all_tools, verbose=True)


def main():
    st.set_page_config(page_title="AI Calendar Agent", page_icon="📅")
    st.title("🤖 AI Calendar Agent")
    st.caption("I can help manage your calendar. Example: 'Check doc ID 123xyz and schedule events'")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "How can I help with your calendar today?"
        }]

    # Initialize agent (cached)
    if "agent_executor" not in st.session_state:
        with st.spinner("Initializing agent..."):
            st.session_state.agent_executor = initialize_agent()

    # Display chat messages
    for msg in st.session_state.messages:
        role = "assistant" if msg["role"] == "assistant" else "user"
        with st.chat_message(role):
            st.write(msg["content"])

    # Handle user input
    if user_input := st.chat_input("Ask the agent..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Prepare chat history for agent
        chat_history = []
        for msg in st.session_state.messages[:-1]:  # Exclude current input
            if msg["role"] == "user":
                chat_history.append(HumanMessage(content=msg["content"]))
            else:
                chat_history.append(AIMessage(content=msg["content"]))

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.agent_executor.invoke({
                        "input": user_input,
                        "chat_history": chat_history
                    })
                    response = result["output"]
                except Exception as e:
                    response = f"⚠️ Error: {str(e)}"

            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()