import asyncio
import os
import random
import subprocess
import sys

import zmq
from PyQt6 import QtCore, QtGui, QtQml

from player import play, pause, previous, next, np, queue, like, toggle_repeat

myApp = QtGui.QGuiApplication(sys.argv)
myEngine = QtQml.QQmlApplicationEngine()
directory = os.path.dirname(os.path.abspath(__file__))

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt(zmq.SUBSCRIBE, b"")  # Subscribe to all messages

poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

process = None
deep = False


def setASRText(transcript):
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", transcript)


def update_ui():
    busyIndicator = myEngine.rootObjects()[0].findChild(QtCore.QObject, "busyIndicator")
    busyIndicator.setProperty("visible", False)
    global deep
    if deep:
        busyIndicator.setProperty("visible", True)
        socks = dict(poller.poll(timeout=50))  # Poll for available messages, with a timeout of .05 second
        if subscriber in socks and socks[subscriber] == zmq.POLLIN:
            audio_text = subscriber.recv_string()
            setASRText(audio_text)  # Your audio text processing code here
            busyIndicator.setProperty("visible", False)
    track, art, artist, progress, isPlaying = np()
    album = myEngine.rootObjects()[0].findChild(QtCore.QObject, "art")
    album.setProperty("source", art)
    toptext = myEngine.rootObjects()[0].findChild(QtCore.QObject, "track")
    toptext.setProperty("text", track)
    bottomtext = myEngine.rootObjects()[0].findChild(QtCore.QObject, "artist")
    bottomtext.setProperty("text", artist)
    progressBar = myEngine.rootObjects()[0].findChild(QtCore.QObject, "progressBar")
    progressBar.setProperty("value", progress)
    if isPlaying:
        button = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
        button.setProperty("text", "Pause")
    else:
        button = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
        button.setProperty("text", "Play")


def playpause_clicked():
    button = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
    if button.property("text") == "Play":
        bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
        bottomText.setProperty("text", "Play Button Clicked")
        button = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
        button.setProperty("text", "Pause")
        play()
        update_ui()
    else:
        bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
        bottomText.setProperty("text", "Pause Button Clicked")
        button = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
        button.setProperty("text", "Play")
        pause()
        update_ui()


def skip_clicked():
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", "Skip Button Clicked")
    next()
    update_ui()


def prev_clicked():
    myEngine.retranslate()
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", "Previous Button Clicked")
    previous()
    update_ui()


def like_clicked():
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", "Like Button Clicked")
    like()


def search_clicked():
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", "Search Button Clicked")
    strings = ["Backseat Lovers", "Hozier", "Arctic Monkeys", "Tame Impala", "Taylor Swift", "Noah Kahan", "Imagine Dragons", "Dayglow", "ABBA",
               "The Beatles"]
    random_string = random.choice(strings)
    queue(random_string, 1)
    next()
    update_ui()


def loop_clicked():
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", "Repeat Button Clicked")
    toggle_repeat()


def asr_toggled():
    global process
    global deep
    toggle = myEngine.rootObjects()[0].findChild(QtCore.QObject, "asrSwitch")
    if toggle.property("checked"):
        setInfoText("ASR Turned On -- Waiting for Connection")
        print("Starting Up Connection to ASR Program")
        process = subprocess.Popen(["python", "deepg.py"])
        deep = True
    else:
        setInfoText("ASR Turned Off")
        print("Killing Connection to ASR Program")
        process.terminate()
        deep = False


def setInfoText(text):
    bottomText = myEngine.rootObjects()[0].findChild(QtCore.QObject, "bottomText")
    bottomText.setProperty("text", text)


async def run():
    myEngine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, 'player.qml')))

    if not myEngine.rootObjects():
        return -1

    # button interaction goes here
    playpauseButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "playpauseButton")
    playpauseButton.clicked.connect(lambda: playpause_clicked())
    skipButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "skipButton")
    skipButton.clicked.connect(lambda: skip_clicked())
    prevButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "prevButton")
    prevButton.clicked.connect(lambda: prev_clicked())
    likeButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "likeButton")
    likeButton.clicked.connect(lambda: like_clicked())
    searchButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "searchButton")
    searchButton.clicked.connect(lambda: search_clicked())
    loopButton = myEngine.rootObjects()[0].findChild(QtCore.QObject, "loopButton")
    loopButton.clicked.connect(lambda: loop_clicked())
    asrSwitch = myEngine.rootObjects()[0].findChild(QtCore.QObject, "asrSwitch")
    asrSwitch.clicked.connect(lambda: asr_toggled())

    timer = QtCore.QTimer()
    timer.timeout.connect(update_ui)
    timer.start(1000)  # 1000 milliseconds = 1 second
    myApp.exec()


if __name__ == "__main__":
    asyncio.run(run())
