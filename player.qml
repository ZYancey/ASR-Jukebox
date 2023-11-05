import QtQuick 6.2
import QtQuick.Window 6.2
import QtQuick.Controls 6.2

ApplicationWindow {
    visible: true
    width: 600
    height: 920
    Rectangle {
        id: rectangle
        width: 600
        height: 920
        color: "#2f2f2f"

        }
        ProgressBar {
            id: progressBar
            objectName: "progressBar"
            x: 0
            y: 609
            width: 600
            height: 44
            layer.format: ShaderEffectSource.RGB
            value: 0
        }

        Image {
            id: image
            objectName: "art"
            visible: true
            x: 22
            y: 26
            width: 556
            height: 555
            source: ""
            fillMode: Image.PreserveAspectFit
        }

        Button {
            id: button1
            objectName: "playpauseButton"
            x: 128
            y: 769
            width: 344
            height: 104
            text: qsTr("Play")
            states: [
                State {
                    name: "clicked"
                    when: button1.checked
                }
            ]
        }

        Button {
            id: button2
            objectName: "skipButton"
            x: 478
            y: 769
            width: 100
            height: 56
            text: qsTr(">>>")
        }

        Text {
            id: text1
            objectName: "bottomText"
            x: 112
            y: 886
            width: 449
            height: 26
            color: "#fffdfd"
            text: qsTr("This is where a transcript of the recorded asr will be shown")
            font.pixelSize: 12
            verticalAlignment: Text.AlignVCenter
        }

        Switch {
            id: switch1
            objectName: "asrSwitch"
            x: 8
            y: 886
            width: 98
            height: 26
            text: qsTr("ASR")
            checked: false
        }

        BusyIndicator {
            id: busyIndicator
            objectName: "busyIndicator"
            visible: true
            x: 559
            y: 879
            width: 33
            height: 33
        }

        Button {
            id: button3
            objectName: "likeButton"
            x: 525
            y: 831
            width: 52
            height: 42
            text: qsTr("♡")
        }

        Button {
            id: buttonloop
            objectName: "loopButton"
            x: 478
            y: 831
            width: 52
            height: 42
            text: qsTr("↻")
        }

        Button {
            id: button4
            objectName: "prevButton"
            x: 22
            y: 769
            width: 100
            height: 56
            text: qsTr("<<<")
        }

        Button {
            id: button5
            objectName: "searchButton"
            x: 22
            y: 831
            width: 100
            height: 42
            text: qsTr("Search")
        }

        Text {
            id: text2
            objectName: "track"
            x: 30
            y: 659
            width: 531
            height: 54
            color: "#ffffff"
            text: qsTr("Track / Album")
            font.pixelSize: 24
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.styleName: "Bold"
            font.family: "Arial"
            font.bold: true
        }

        Text {
            id: text3
            objectName: "artist"
            x: 30
            y: 728
            width: 531
            height: 35
            color: "#ffffff"
            text: qsTr("Artist")
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.styleName: "Italic"
            font.family: "Arial"
        }






    
}
