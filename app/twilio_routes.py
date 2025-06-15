from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from app.ai_logic import process_voice

router = APIRouter()

@router.post("/twilio/voice")
async def voice_webhook(request: Request):
    response = VoiceResponse()
    # Add a 2-second pause before greeting
    response.pause(length=2)
    audio_url = await process_voice(request)
    response.play(audio_url)
    return Response(content=str(response), media_type="application/xml")