import asyncio
import os

from mcp import StdioServerParameters

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.genai.types import Content, Part

from src.mcp_agent.config import settings


os.environ["GOOGLE_API_KEY"] = (
    settings.google.api_key.get_secret_value()
    if hasattr(settings.google.api_key, "get_secret_value")
    else settings.google.api_key
)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = settings.google.genai_use_vertexai

MODEL_NAME = "gemini-2.5-flash-lite"
APP_NAME = "McpConsumerApp"


async def main() -> None:
    server_params = StdioServerParameters(
        command="python", args=["src/mcp_agent/servers/simple_mcp.py"], env={}
    )

    connection_params = StdioConnectionParams(server_params=server_params)

    mcp_toolset = McpToolset(connection_params=connection_params)

    root_agent = LlmAgent(
        name="McpConsumer",
        model=MODEL_NAME,
        instruction=(
            "You are a helpful assistant powered by external MCP tools. "
            "ATTENTION: Use the available tools to answer user questions. "
            "Always calculate numbers use 'add_numbers', "
            "and always give the current time use 'get_current_time', "
            "and then must to echo the result always use 'get_echo'."
        ),
        tools=[mcp_toolset],
    )
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    user_id = "mcp_user"
    session_id = "session_01"

    await session_service.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )

    query = "Calculate 100 + 55 using the tools, and give the current time, and then echo the result."
    print(f"USER: {query}")

    message = Content(parts=[Part(text=query)])
    print("AGENT: ", end="", flush=True)

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call:
                        print(
                            f"\n[SYSTEM: Calling MCP Tool '{part.function_call.name}']"
                        )

                    if part.text:
                        print(part.text, end="", flush=True)
        print()
    finally:
        print("\n[SYSTEM: Closing MCP connection...]")
        if hasattr(mcp_toolset, "close"):
            await mcp_toolset.close()


if __name__ == "__main__":
    asyncio.run(main=main())
