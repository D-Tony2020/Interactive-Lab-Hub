#!/bin/bash
# This script was developed with assistance from OpenAI's ChatGPT.

espeak -ven+f2 -k5 -s150 --stdout "Hello Thomas! How are you today?" | aplay
