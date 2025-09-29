#!/bin/bash

echo "How many pets do you have?" | festival --tts

echo "Recording... Please speak now."
arecord -d 5 -f cd -t wav -r 16000 -c 1 recorded.wav

echo "Transcribing your response..."
vosk-transcriber -i recorded.wav -o pets_answer.txt

echo "Your answer has been saved to pets_answer.txt"
cat pets_answer.txt
