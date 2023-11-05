import asyncio
import json

import pyaudio
import websockets
import zmq

from classifier import respond

publisher = None

# print("Binding Connection Port: tcp://*:5556")
# context = zmq.Context()
# publisher = context.socket(zmq.PUB)
# publisher.bind("tcp://*:5556")
# print("Success!")

DEEPGRAM_API_KEY = ""

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000

audio_queue = asyncio.Queue()


def callback(input_data, frame_count, time_info, status_flags):
    audio_queue.put_nowait(input_data)

    return input_data, pyaudio.paContinue


async def microphone():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=callback
    )

    print("Listening!")
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
    global publisher
    async for msg in ws:
        msg = json.loads(msg)
        transcript = msg['channel']['alternatives'][0]['transcript']
        if transcript and publisher:
            publisher.send_string(respond(transcript) + ' | ' + transcript)


async def process():
    global publisher
    loop = asyncio.get_running_loop()

    print("Binding Connection Port: tcp://*:5556")
    context = await loop.run_in_executor(None, zmq.Context)
    publisher = await loop.run_in_executor(None, context.socket, zmq.PUB)
    await loop.run_in_executor(None, publisher.bind, "tcp://*:5556")
    await asyncio.sleep(1)
    await loop.run_in_executor(None, publisher.send_string, "Connection Successful! Now Listening!")
    print("Connection Success!")

    extra_headers = {
        'Authorization': 'token ' + DEEPGRAM_API_KEY
    }

    async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1',
                                    extra_headers=extra_headers) as ws:
        await asyncio.gather(sender(ws), receiver(ws))


async def run():
    print("Starting Up Connection to ASR Program")
    await asyncio.gather(microphone(), process())


if __name__ == '__main__':
    asyncio.run(run())
