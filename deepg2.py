import asyncio
import json

import pyaudio
import websockets
import zmq

from classifier import respond

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

DEEPGRAM_API_KEY = ""

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

audio_queue = asyncio.Queue()

audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

def callback(input_data, frame_count, time_info, status_flags):
    audio_queue.put_nowait(input_data)

    return input_data, pyaudio.paContinue


async def microphone():
    global stream
    stream.start_stream()

    while stream.is_active():
        await asyncio.sleep(0.1)

    stream.stop_stream()
    stream.close()


async def sender(ws):  # sends audio to websocket
    try:
        while True:
            data = await audio_queue.get()
            await ws.send(data)
    except Exception as e:
        print('Error while sending: ', + str(e))
        raise


async def receiver(ws):
    async for msg in ws:
        msg = json.loads(msg)
        transcript = msg['channel']['alternatives'][0]['transcript']
        if transcript:
            publisher.send_string(respond(transcript) + ' | ' + transcript)


async def process():
    extra_headers = {
        'Authorization': 'token ' + DEEPGRAM_API_KEY
    }

    async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1',
                                    extra_headers=extra_headers) as ws:
        await asyncio.gather(sender(ws), receiver(ws))


async def run():
    await asyncio.gather(microphone(), process())


if __name__ == '__main__':
    asyncio.run(run())