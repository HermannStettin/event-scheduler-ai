# agent_main.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# --- MODIFICATION: Import the correct prompt template class ---
from langchain.prompts import ChatPromptTemplate
# --- MODIFICATION: Import the correct agent creator ---
from langchain.agents import create_tool_calling_agent, AgentExecutor
from agent_tools import all_tools

def main():
    """Initializes and runs the AI Calendar Agent."""
    load_dotenv()
    print("🚀 Starting AI Calendar Agent...")
    print("Tell me what to do. For example: 'Check the doc with ID 123xyz and schedule the events.'")
    print("Type 'exit' to quit.")

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash", 
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. You have access to a set of tools. "
                "Use them to answer the user's question. "
                "**Important Rule: If a duration for an event is not specified, assume it is one hour long.**"
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, all_tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)

    while True:
        user_input = input(">> ")
        if user_input.lower() == 'exit':
            print("🤖 Agent shutting down. Goodbye!")
            break
        
        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": [] 
        })
        
        print("\n✅ Agent's Final Answer:")
        print(result["output"])
        print("-" * 30)

if __name__ == "__main__":
    main()