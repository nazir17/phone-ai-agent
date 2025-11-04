from __future__ import annotations
import os
import logging
from livekit import rtc
from livekit.agents import ( AutoSubscribe, JobContext, WorkerOptions, cli, llm)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv


load_dotenv()


log = logging.getLogger("voice_agent")
log.setLevel(logging.INFO)


instructions_doc = open("instruction.txt", "r").read()
log.info(f"Instructions: (instructions_doc)")


async def main_entry(ctx: JobContext):

    log.info("Initiating the entry point")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    api_key = os.getenv("LIVEKIT_API_KEY")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    ai_model = openai.realtime.RealtimeModel(
        instructions=instructions_doc,
        voice="shimmer",
        temperature=0.8,
        modalities=["audio", "text"],
        api_key=openai_api_key,
    )

    mutlimodal_assistant = MultimodalAgent(model=ai_model)
    mutlimodal_assistant.start(ctx.room)


    session_instance = ai_model.sessions[0]
    session_instance.conversation.item.create(
        llm.ChatMessage(
            role="user",
            content="Please begin the interaction with the user in a manner consistence with your instructions."
        )
    )

    session_instance.response.create()

if __name__ == "__main__":
    log.info("About to run main")

    cli.run_app(WorkerOptions(entrypoint_fnc=main_entry, agent_name="inbound-agent"))