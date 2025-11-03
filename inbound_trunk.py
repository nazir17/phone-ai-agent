import asyncio
import os
from livekit import api
from dotenv import load_dotenv


async def main():
    load_dotenv()


    livekit_api = api.LiveKitAPI()


    inbound_trunk = api.SIPInboundTrunkInfo(
        name = "LiveKit to Twilio Trunk",
        auth_username = os.getenv("TWIML_USERNAME"),
        auth_password = os.getenv("TWIML_PASSWORD"),
        krisp_enabled = True,
    )


    request = api.CreateSIPInboundTrunkRequest(
        trunk = inbound_trunk,
    )

    inbound_trunk = await livekit_api.sip.create_inbound_trunk(request)

    await livekit_api.aclose()

asyncio.run(main())