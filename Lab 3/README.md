# Chatterboxes

<mark> **Collaborators: Thomas Knoepffler, Carrie Wang, Xiaocheng Li Julia Chen, Dean Xu** </mark>

<details>
  <summary><strong>Lab Description</strong></summary>

[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything _but_ control lights (since we already did that in Lab 1). First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond. We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

</details>

<details>
  <summary><strong>Prep for Part 1: Get the Latest Content and Pick up Additional Parts</strong></summary>

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts

Please check instructions in [prep.md](prep.md) and complete the setup before class on Wednesday, Sept 23rd.

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [Logitech C270 Webcam](https://www.amazon.com/Logitech-Desktop-Widescreen-Calling-Recording/dp/B004FHO5Y6/ref=sr_1_3?crid=W5QN79TK8JM7&dib=eyJ2IjoiMSJ9.FB-davgIQ_ciWNvY6RK4yckjgOCrvOWOGAG4IFaH0fczv-OIDHpR7rVTU8xj1iIbn_Aiowl9xMdeQxceQ6AT0Z8Rr5ZP1RocU6X8QSbkeJ4Zs5TYqa4a3C_cnfhZ7_ViooQU20IWibZqkBroF2Hja2xZXoTqZFI8e5YnF_2C0Bn7vtBGpapOYIGCeQoXqnV81r2HypQNUzFQbGPh7VqjqDbzmUoloFA2-QPLa5lOctA.L5ztl0wO7LqzxrIqDku9f96L9QrzYCMftU_YeTEJpGA&dib_tag=se&keywords=webcam%2Bc270&qid=1758416854&sprefix=webcam%2Bc270%2Caps%2C125&sr=8-3&th=1) and bluetooth speaker on Wednesday at the beginning of lab. If you cannot make it to class this week, please contact the TAs to ensure you get these.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the _personal access token_ for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2025
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

</details>

## Part 1.

<details>
  <summary><strong>Setup</strong></summary>

### Setup

Activate your virtual environment

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ cd Lab\ 3
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python3 -m venv .venv
pi@ixe00:~/Interactive-Lab-Hub $ source .venv/bin/activate
(.venv)pi@ixe00:~/Interactive-Lab-Hub $
```

Run the setup script
`(.venv)pi@ixe00:~/Interactive-Lab-Hub $ pip install -r requirements.txt  `

Next, run the setup script to install additional text-to-speech dependencies:

```
(.venv)pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ ./setup.sh
```

</details>

<details>
  <summary><strong>Text to Speech</strong></summary>

### Text to Speech

In this part of lab, we are going to start peeking into the world of audio on your Pi!

We will be using the microphone and speaker on your webcamera. In the directory is a folder called `speech-scripts` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/speech-scripts $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files `.sh` by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/speech-scripts $ cat festival_demo.sh
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech
```

You can test the commands by running

```
echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file?
Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

---

Bonus:
[Piper](https://github.com/rhasspy/piper) is another fast neural based text to speech package for raspberry pi which can be installed easily through python with:

```
pip install piper-tts
```

and used from the command line. Running the command below the first time will download the model, concurrent runs will be faster.

```
echo 'Welcome to the world of speech synthesis!' | piper \
  --model en_US-lessac-medium \
  --output_file welcome.wav
```

Check the file that was created by running `aplay welcome.wav`. Many more languages are supported and audio can be streamed dirctly to an audio output, rather than into an file by:

```
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  piper --model en_US-lessac-medium --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -
```

</details>

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

<mark> Code can be found here [hello_thomas.sh](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/speech-scripts/hello_thomas.sh) </mark>

<details>
  <summary><strong>Speech to Text</strong></summary>

### Speech to Text

Next setup speech to text. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi.

Make sure you're running in your virtual environment with the dependencies already installed:

```
source .venv/bin/activate
```

Test if vosk works by transcribing text:

```
vosk-transcriber -i recorded_mono.wav -o test.txt
```

You can use vosk with the microphone by running

```
python test_microphone.py -m en
```

---

Bonus:
[Whisper](https://openai.com/index/whisper/) is a neural network–based speech-to-text (STT) model developed and open-sourced by OpenAI. Compared to Vosk, Whisper generally achieves higher accuracy, particularly on noisy audio and diverse accents. It is available in multiple model sizes; for edge devices such as the Raspberry Pi 5 used in this class, the tiny.en model runs with reasonable latency even without a GPU.

By contrast, Vosk is more lightweight and optimized for running efficiently on low-power devices like the Raspberry Pi. The choice between Whisper and Vosk depends on your scenario: if you need higher accuracy and can afford slightly more compute, Whisper is preferable; if your priority is minimal resource usage, Vosk may be a better fit.

In this class, we provide two Whisper options: A quantized 8-bit faster-whisper model for speed, and the standard Whisper model. Try them out and compare the trade-offs.

Make sure you're in the Lab 3 directory with your virtual environment activated:

```
cd ~/Interactive-Lab-Hub/Lab\ 3/speech-scripts
source ../.venv/bin/activate
```

Then test the Whisper models:

```
python whisper_try.py
```

and

```
python faster_whisper_try.py
```

</details>

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

<mark> Code can be found here [siblings.py](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/speech-scripts/siblings.py) </mark>

<mark> **Discalimer:** The interaction is unpolished. The standard TTS model misrecognizes some numbers and confuses them with other words. There’s a pause between the model asking the question and retrieving the TTS model for the user, causing a delay between the computer asking “how many siblings do you have?” and the user’s response. </mark>

<details>
  <summary><strong>NEW: AI-Powered Conversations with Ollama</strong></summary>

### 🤖 NEW: AI-Powered Conversations with Ollama

Want to add intelligent conversation capabilities to your voice projects? **Ollama** lets you run AI models locally on your Raspberry Pi for sophisticated dialogue without requiring internet connectivity!

#### Quick Start with Ollama

**Installation** (takes ~5 minutes):

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download recommended model for Pi 5
ollama pull phi3:mini

# Install system dependencies for audio (required for pyaudio)
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev

# Create separate virtual environment for Ollama (due to pyaudio conflicts)
cd ollama/
python3 -m venv ollama_venv
source ollama_venv/bin/activate

# Install Python dependencies in separate environment
pip install -r ollama_requirements.txt
```

#### Ready-to-Use Scripts

We've created three Ollama integration scripts for different use cases:

**1. Basic Demo** - Learn how Ollama works:

```bash
python3 ollama_demo.py
```

**2. Voice Assistant** - Full speech-to-text + AI + text-to-speech:

```bash
python3 ollama_voice_assistant.py
```

**3. Web Interface** - Beautiful web-based chat with voice options:

```bash
python3 ollama_web_app.py
# Then open: http://localhost:5000
```

#### Integration in Your Projects

Simple example to add AI to any project:

```python
import requests

def ask_ai(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3:mini", "prompt": question, "stream": False}
    )
    return response.json().get('response', 'No response')

# Use it anywhere!
answer = ask_ai("How should I greet users?")
```

**📖 Complete Setup Guide**: See `OLLAMA_SETUP.md` for detailed instructions, troubleshooting, and advanced usage!

</details>

\*\***Try creating a simple voice interaction that combines speech recognition, Ollama processing, and text-to-speech output. Document what you built and how users responded to it.**\*\*

<details>
  <summary><strong>Serving Pages</strong></summary>

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```

From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

</details>

<details>
  <summary><strong>Storyboard</strong></summary>

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.)

</details>

\*\***Post your storyboard and diagram here.**\*\*

![Sketch 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Sketch_2.jpg)
![Storyboard 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_1.jpg)
![Storyboard 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_2.jpg)

<mark> _**AI Usage:** Second storyboard generated using Google (Gemini). All original artifacts preserved._ </mark>

<details>

  <summary><mark><strong>Original Prompt(s)</strong></mark></summary>

  <br>

<mark> _"A minimalist stick figure storyboard, black and white line drawing, comic style: Panel 1 shows a smiling stick figure pressing a doorbell button on a wall with the speaker visible. Panel 2 shows the speaker saying “You brought nothing” as the surprised visitor stands empty-handed. Panel 3 shows the visitor replying “I came with true feelings,” and the doorbell responding “Feelings are cheap, a bottle of wine is better,” with the visitor looking nervous. Panel 4 shows the visitor pleading “Please let me in,” and the doorbell saying “I’ll tell them: someone came with nothing,” as the visitor appears embarrassed. Panel 5 shows the visitor walking away sadly, slumped, while the doorbell says “Finally understood.” Panel 6 shows the visitor walking away in the distance, the lonely doorbell on the wall, with the caption below: “When AI sets cold rules, can humans insist?”"_ </mark>

</details>

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses.

<mark> We imagine the dialogue happening between a doorway, so we envision the initial activation being pressing a doorbell button. But we want to take it further and envision a device that is also reactive and displaying some form of emotion or response to the user, which can be funny as well. If the user continues to engage us with the doorbell object, then they will continue to get a reaction from it, thus entering into a feedback loop of reaction, response, and engagement. </mark>

![Diagram 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Diagram_1.jpg)

\*\***Please describe and document your process.**\*\*

<mark>For this project, we had decided to create an expressive and funny doorbell. The scenario being the user would approach the doorbell, ring it, and by ringing it, would induce the doorbell to have a mean, angry dialogue against the user, subverting the assumption that objects associated with an entrance should be welcoming or inviting.</mark>

<mark>The project is a speculative, experimental piece, more for entertainment purposes but also exploring how AI and LLMs don’t always have to be “user friendly” too, so to speak.</mark>

![Sketch 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Sketch_1.jpg)
![Rendering 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Rendering_1.jpg)
![Rendering 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Rendering_2.jpg)

<mark> _**AI Usage:** Realistic renderings generated using Google (Gemini). All original artifacts preserved._ </mark>

<details>

  <summary><mark><strong>Original Prompt(s)</strong></mark></summary>

  <br>

<mark> _"Please render the following design sketch into a modern, technologically advanced doorbell device. Create a rendering of the device in a realistic scenario: mounted on a simple wooden or metal doorframe. Below or next to the doorbell, a small camera and microphone indicator should be located. It should include an LED indicator or touch panel. A virtual "venomous AI response" represented by a speech waveform or text bubble may be included to hint at its functionality. The overall design should be clear, modern, and representative of the product."_ </mark>

</details>

<details>
  <summary><strong>Acting out the dialogue</strong></summary>

### Acting out the dialogue

Find a partner, and _without sharing the script with your partner_ try out the dialogue you've designed, where you (as the device designer) act as the device you are designing. Please record this interaction (for example, using Zoom's record feature).

</details>

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

- <mark> Watch Acting Out Dialogue (CRINGE WARNING!!!): [Acting Dialogue Video Link](https://drive.google.com/file/d/1iuCn_zKxMuMryWU6V35-9RvXqLwkYUdT/view?usp=sharing) </mark>

<mark>The acted-out dialogue was a perfect example of learning by failure. We originally thought that the dialogue would feel a little bit funny or absurd, having a doorbell talk back to the user after it has been rung. However, as demonstrated by this dramatized reenactment of the tests, the interaction turned out to be rather awkward and clumsy. The users had no idea how to react to a belligerent doorbell, and trying to come up with quippy dialogue for the doorbell without having any context or any computer vision would be very difficult, without making any assumptions. So, considering these insights, it would be best to refactor the doorbell and implement other techniques to make the interaction slightly smoother while still maintaining the absurdity of the situation. Maybe incorporating a more robotic voice and changing the cadence to be more procedural rather than expressive so as to put the user in a different kind of context (i.e., knowing they are interacting with a machine rather than a human).</mark>

<details>
  <summary><strong>Wizarding with the Pi (optional)</strong></summary>

### Wizarding with the Pi (optional)

In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

</details>

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

- <mark> Watch Prototyped OpenAI Interaction: [OpenAI Interaction Video Link](https://drive.google.com/file/d/1pVRkpdU1npdhJN_5IxCguOnDIQZaxEN1/view?usp=sharing) </mark>

<mark> The prototyped interaction ran much smoother compared to the acted-out interaction. We managed to run OpenAI models through an API onto the Pi and made use of its extensive library of voices, cadences, and prompts. We decided to shift the tone of the device to mimic the individual who is interacting with it, instead of having an angry machine all the time. The initial instruction parameter was, "You are an emotion-responsive system that listens to transcribed speech from people (text converted from audio), detects emotion, and generates a short, friendly response." We also included various different adjectives so that it could qualify the cadence and speech, including a vector containing the strings ["Enthusiastic", "Indifferent", "Playful", "Sarcastic", "Caring", "Melancholic", "Grumpy", "Mysterious"]. While the interaction ran smoother, it still felt too contrived. The responses also seemed too short, giving the impression that the device was not animated, but rather a responsive chatbot.</mark>

# Lab 3 Part 2

<details>
  <summary><strong>Description</strong></summary>

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

</details>

<details>
  <summary><strong>Prep for Part 2</strong></summary>

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.

</details>

<details>
  <summary><strong>Prototype your system</strong></summary>

## Prototype your system

The system should:

- use the Raspberry Pi
- use one or more sensors
- require participants to speak to it.

_Document how the system works_

_Include videos or screencaptures of both the system and the controller._

</details>

<details>
  <summary><strong>Submission Cleanup Reminder</strong></summary>
  
  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
  
  This helps ensure your README.md is clear professional and uniquely yours!
</details>

<details>
  <summary><strong>Test the system</strong></summary>

## Test the system

Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

</details>

### <mark> Updated Storyboards </mark>

<mark> We continued to iterate upon our idea of creating a multi-variable emotional doorbell by generating many more storyboards. While they became entertaining and allowed for a larger possibility space, the sheer volume of different emotional categories and specific instances where each emotional response can take place became overwhelming. OpenAI's ChatGPT also is not very good at changing its cadence and being dramatic; it would have to be hard-prompted to be able to maintain a highly dramatized emotional response. This made us reconsider our initial proposition for a mean doorbell and potentially see if we can revitalize the original vision by embodying it in an enclosure and making it into an interactive device. Perhaps then, it could be a little bit more absurd and play on the sort of dramatized comedic element of a disgruntled inanimate object.</mark>

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_3.jpg" alt="Storyboard 3" width="49.5%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_4.jpg" alt="Storyboard 4" width="49.5%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_6.jpg" alt="Storyboard 6" width="49.5%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Storyboards/Storyboard_7.jpg" alt="Storyboard 7" width="49.5%"/>
</p>

<mark> _**AI Usage:** Storyboard generated using Google (Gemini) and OpenAI. All original artifacts preserved._ </mark>

<details>

  <summary><mark><strong>Original Prompt(s)</strong></mark></summary>

  <br>

<mark> _"A humorous and friendly black-and-white line-art comic storyboard with a 1:1 aspect ratio. Scene 1: An enthusiastic doorbell rings. Panel 1: A cheerful stick-figure visitor stands in front of a simple door with small steps, smiling and pressing the doorbell button. Panel 2: The doorbell speaker bursts out an enormous speech bubble, startling the visitor. Panel 3: The visitor scratches their head awkwardly, sweat drops show nervous amusement, while the doorbell says, “Come in, come in! You’re the star of the day!”. Panel 4: The visitor shrugs and rolls their eyes, a small grin on their face. The doorbell sits still on the wall. The scene closes with a warm, witty, and playfully comedic tone."_ </mark>

<mark> _"A minimalist black-and-white line-art comic storyboard with a 1:1 aspect ratio and a dry, deadpan tone. Scene 2 depicts an indifferent doorbell. Panel 1 shows a cheerful stick-figure visitor pressing the doorbell and asking, “Hi, anyone home?” The rectangular doorbell has one half-open, disinterested eye. The composition is clean and balanced, with humor arising from contrast. Panel 2 repeats the scene: the visitor stiffens in surprise as the doorbell’s eye droops, and it replies with a tiny, dull speech bubble, “Yeah.” The visitor’s awkward face amplifies the emotional mismatch. Panel 3 keeps the same layout: the visitor leans forward with polite hope, hands clasped, asking, “Can I come in?” The doorbell’s eye drifts away wordlessly, uninterested. Panel 4 concludes with the visitor giving a helpless laugh, shoulders raised, and palms open toward the viewer. The unmoved doorbell mutters, “Whatever.” The closing beat is minimalist, witty, and effortlessly deadpan."_ </mark>

<mark> _"A minimalist black-and-white line-art comic storyboard with a lighthearted and comical tone. Scene 3 features a playful doorbell. Panel 1 shows a stick-figure visitor looking down at their phone while a coffee cup tilts, a drop falls on the doorbell button, and its expressive eye opens in shock. Panel 2 repeats the setup, but the doorbell squints, yells “Ouch! That’s hot coffee!”, and the visitor jerks back. Panel 3 keeps the same framing, with the visitor apologizing and the doorbell’s eye softening into a sly smirk. Panel 4 closes the scene with the doorbell’s eye wide and grinning, a bubble reading “No worries! Just brew me another one next time.” The visitor laughs, hand over mouth, turning a small accident into playful camaraderie."_ </mark>

<mark> _"A minimalist black-and-white line-art comic storyboard with a comically inquisitive tone. Scene 4: A curious doorbell. Panel 1: A simple doorway and steps. A rectangular doorbell with one large, expressive eye looks puzzled. A stick-figure delivery person holds a large, oddly shaped package. The courier’s speech bubble reads, “Your delivery, please sign here.” The mood is professional but humorously tense. Panel 2: The courier sets the strange package on the step. The doorbell squints suspiciously, asking, “Wait… what’s in that package? It looks weird.” The courier stands neutrally. The comedy comes from the doorbell’s nosy personality. Panel 3: The courier walks away mid-step. The doorbell’s eye darts left and right, blur lines suggest restlessness. Its speech bubble shouts, “Hey! Don’t go! Tell me! Is it… an alien pet?!”. The scene ends with exaggerated, cinematic humor—a curious AI desperate for gossip, ignored by an indifferent human."_ </mark>

</details>

### <mark> Electronics Assembly </mark>

<mark> Our electronics assembly made use of the Pi, a breadboard, multiple jumper wires, a red LED, a 220 Ohm resistor, a tactile button switch, a mini speaker, and a WebCam for microphone use. The electronics were tested separately before being assembled.</mark>

![Process 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_3.jpg)

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_1.jpg" alt="Process 1" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_2.jpg" alt="Process 2" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_7.jpg" alt="Process 7" width="33%"/>
</p>

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_4.jpg" alt="Process 4" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_5.jpg" alt="Process 5" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Process/Process_6.jpg" alt="Process 6" width="33%"/>
</p>

### <mark> Drafting & Modeling </mark>

<mark> We modeled our enclosure in Rhino 3D. This time we made sure to accommodate all the internal electronics within the device. The doorbell was modeled with a modern aesthetic in mind, with beveled edges and a perforated speaker in the front, with a central button in the middle to ring the doorbell. The design was based on traditional injection molding processes and translated to 3D printing to preserve materiality. </mark>

![Draft 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Draft_1.png)
![Draft 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Draft_2.png)
![Draft 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Sketches/Draft_3.png)

### <mark> Device Enclosure </mark>

<mark> The enclosure was 3D printed using the BambooLab 3D printer, using standard white PLA. A plastic eye was put on the button for decor. </mark>

![Image 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_1.jpg)
![Image 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_2.jpg)
![Image 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_3.jpg)
![Image 4](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_4.jpg)
![Image 5](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_5.jpg)

### <mark> Python Code </mark>

<mark> Our code can be found at [mean-doorbell.py](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/speech-scripts/mean-doorbell.py) </mark>

<mark> _**AI Usage:** Utilized assistance from ChatGPT for the writing of code._ </mark>

<mark> _**Pros:** We were working together through pair programming for this assignment and began one set of code for one use case and then refactored it for another. ChatGPT was very helpful in summarizing the code from one developer to the other, and was able to refactor and make changes to it very easily without having to understand the finer details of the API implementation or the dependencies used._ </mark>

<mark> _**Cons:** This, however, can also be a con whereby if code is passed on from one developer to the next, there can be multiple layers of abstraction being created when working within a new code base. It could then become highly difficult to determine what code is becoming refactored and which code might also be vital to preserve for updates. It could also lead to more dependencies than need be._ </mark>

### <mark> Test Dialogue </mark>

- <mark> Watch Test Dialogue #1: [Doorbell #1 Video Link](https://drive.google.com/file/d/1Y69Cxp0skwV55OnjJOGuuaDrJjPpXC_Y/view?usp=sharing) </mark>

- <mark> Watch Test Dialogue #2: [Doorbell #2 Video Link](https://drive.google.com/file/d/15nI-p92rAE_d4e8osTV2ABTQFLTecTOJ/view?usp=sharing) </mark>

- <mark> Watch Test Dialogue #3: [Doorbell #3 Video Link](https://drive.google.com/file/d/1j2vnOPrFmgPWBDjEgYEVDZGm-Hjmz2gu/view?usp=sharing) </mark>

### <mark> Final Dialogue </mark>

- <mark> Watch Final Doorbell Dialogue: [Final Doorbell Video Link](https://drive.google.com/file/d/1En8NHS5hbooRlVKAHFeSg6Yi1Cz-Yzh2/view?usp=sharing) </mark>

### What worked well about the system and what didn't?

<mark> The system produced dynamic outputs and was able to expressively showcase at least one emotion (i.e., anger). However, the system was not able to scale across the subjective emotions and responses, and therefore needed to be explicitly prompted to do so. There was also trouble in creating dynamic conversations as there seemed to have been latency in some of the responses, and the conversation seemed to stay surface level in general rather than probing the user. </mark>

### What worked well about the controller and what didn't?

<mark> In our case, the controller was OpenAI’s ChatGPT. It worked well for our particular use case, but could be expanded upon further, and be prompted to have more detailed instructions as well as more fine-tuned hyperparameters. The expressive nature of the responses needed to be adjusted over time as some of the initial responses were somewhat convoluted or cliché. It was also important to balance the amount of sarcasm within their responses; too much, and the user would sense a pattern; too little, and it would not be funny. </mark>

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

<mark> Well, we spent very little time using Wizard of Oz techniques to prototype in the initial phases. We did try to envision how users might react based off of our acting interaction demo. Even so, perhaps it gave us too much of a bias towards seeing the negatives of the system and prevented us from engaging with the ideas that we initially had from the ground running. We immediately wanted to try to utilize more autonomous systems and therefore turned to ChatGPT and OpenAI as a sort of expressive contorller in the loop. Still, using an autonomous system requires just as much iteration and fine-tuning to ensure that the interactions that you're hoping to achieve run smoothly. So there isn't really an "end" to the evaluation or design. </mark>

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

<mark> We later hope to incorporate some amount of computer vision so that the system can recognize the user in front of them. While the immediate response would be that of reservation, considering that we wouldn't want a mean doorbell to be actively hostile to a user and their appearance, our intention is not to explicitly target appearance qualifiers from the user. Rather, we want to be able to investigate facial reactions and other nonverbal cues that might point towards more sophisticated responses from the AI. In this setting, the responses can also be more humorous as they're playing on other aspects the user may not necessarily be privy to. Similar to how a stand-up comedian might also bring up crowd members and their reactions in a playful way, not in a mocking way. We don't intend on creating a data set from any responses. It's more about seeing where the interaction will go and the qualitative experience that the user has on their end.</mark>

### <mark> Inspiration </mark>

<mark> Our project was inspired by a long line of art and media projects that seek to personify and animate inanimate objects. The number of examples are numerous, but the example that we found the most compelling were the Personality Cores from Portal 2. They are both NPC characters and objects to interact with in the game. They are essentially robotic, spherical gimbals with eyeballs attached to them, and each one is programmed to exhibit a personality, playing into the game's themes of absurdity and humor.</mark>

<mark> Another example that we found very fascinating was the Apple lamp or ELEGNT (Expressive and Functional Movement Design for Non-Anthropomorphic Robot), which was a recent project that wanted to animate a desktop lamp and incorporate smart features into it.</mark>

![Inspiration 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Inspiration/Inspiration_1.jpg)
<mark> _**Image Source:** Valve, Portal 2 (2011)._ </mark>

![Inspiration 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Inspiration/Inspiration_2.jpg)
<mark> _**Image Source:** Apple, ELEGNT (2025)._ </mark>

<mark> Collaborators: Thomas Knoepffler (Assembly & Developer), Carrie Wang (Drafter & Diagram Maker), Xiaocheng Li (3D Modeling), Julia Chen (Hardware & Developer), Dean Xu (AI Artist) </mark>

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_6.jpg" alt="Image 6" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_7.jpg" alt="Image 7" width="33%"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%203/Images/Image_8.jpg" alt="Image 8" width="33%"/>
</p>

### <mark> Interesting Note </mark>

- <mark> When asking ChatGPT to refactor some of the code and to create a more angry, hostile-sounding AI voice, ChatGPT immediately told us that it would not be able to do that for us as it went against its morals. We had to prompt it further and give it context about the project, what we were doing, and told it that it was going to be a comedic application, not for any insidious motive against user-friendliness. I guess LLMs have moral principles after all :)</mark>
