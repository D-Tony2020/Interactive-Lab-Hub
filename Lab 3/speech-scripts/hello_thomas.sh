#!/bin/bash
espeak -ven+f2 -k5 -s150 --stdout "Hello Thomas! How are you today?" | aplay
