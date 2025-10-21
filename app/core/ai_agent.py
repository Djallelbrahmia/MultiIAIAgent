from langchain_groq import  ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph .prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings


def get_response_from_ai_agent(llm_model_name: str, messages: str,allow_search:bool,system_prompt:str) -> str:

    llm = ChatGroq(model_name=llm_model_name)
    tools=[TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    ) 
    state={"messages":messages}
    response=agent.invoke(state)
    messages=response.get("messages",[])
    ai_messages=[msg.content for msg in messages if isinstance(msg,AIMessage)]
    return ai_messages[-1] if ai_messages else "No response from AI agent."