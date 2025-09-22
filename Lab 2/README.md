# Interactive Prototyping: The Clock of Pi

**Collaborators:** Dean Xu, Thomas Knoepffler, Carrie Wang, Xiaocheng Li, Julia Chen

---

## Part A. Connect to your Pi

In this part, I completed the following steps:

1. Used `ssh pi@<IP address>` to successfully connect remotely to the Raspberry Pi.
2. Created and activated a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   Once activated, the command line prefix changed to `(venv)`, confirming the environment was active.
3. Configured Git username and email:

   ```bash
   git config --global user.name "Dean Xu"
   git config --global user.email "hx332@cornell.edu"
   ```
4. Generated a GitHub Personal Access Token and tested push/pull authentication with it.

**Result:**
Successfully connected via SSH, set up the virtual environment, and configured GitHub authentication.

<img width="985" height="565" alt="8ea4dca2e619ac279736a30b1c8f9a4d" src="https://github.com/user-attachments/assets/e93e52ce-f526-47a2-8376-708b7f29e14d" />
<img width="909" height="661" alt="507e784786798a6d43d71a0170858839" src="https://github.com/user-attachments/assets/afc2169e-61b2-4c1c-bc44-1bb58d1bdeed" />


---

## Part B. Try out the Command Line Clock

In this part, I did the following:

1. Cloned the lab repository to the Pi:

   ```bash
   git clone https://github.com/hx332/Interactive-Lab-Hub.git
   cd Interactive-Lab-Hub/Lab\ 2/
   ```
2. Installed required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Ran the command line clock script:

   ```bash
   python cli_clock.py
   ```

   The current date and time were displayed in the terminal and updated continuously.

**Result:**
The command line clock successfully displayed system time. Pressing `ctrl-c` exited the script.

<img width="904" height="656" alt="15ca3f3d56f730efba184cc7f4c44111" src="https://github.com/user-attachments/assets/d72e1259-935d-4e0d-be8c-e8b5161ac90f" />


## Part C. Set up your RGB Display

In this part, I worked with the Adafruit MiniPiTFT display:

1. Inserted the MiniPiTFT screen onto the Raspberry Pi 40-pin header, aligning the mounting holes.
2. Tested the display using the command:

   ```bash
   python screen_test.py
   ```

   The screen successfully displayed background colors, and pressing the hardware buttons changed the display.
3. Explored the code in `screen_boot_script.py` to understand text display, and in `image.py` to see how to load and show images.

**Result:**
The display hardware was correctly connected. The test script worked as expected, showing colors and text. The buttons triggered display changes successfully.
![7df3beaa7d283176d74bbea464e95d7b](https://github.com/user-attachments/assets/89bb896a-c177-4cc0-8b21-ba3b5eb3f037)
![302a8617f0f9c1f4234b245bad9b91b9](https://github.com/user-attachments/assets/7b107e07-2bb6-4cc9-a1a5-074dc29a6549)
![2167b38c7870f5e9d7a18b8b568e31d1](https://github.com/user-attachments/assets/92c6cb96-8078-4e36-b097-4b8a28b990ff)
![ee2bbff7b2810e2c6294b5de3f03759c](https://github.com/user-attachments/assets/12148039-5578-403b-9f48-468efd470640)
![bf5459099569f71d9c4a3bf7d5fe6565](https://github.com/user-attachments/assets/8f923796-cb11-49b6-b9cb-bdbafd944f07)
![6a03a60743fc92632d8996e0d6501ce4](https://github.com/user-attachments/assets/a0f3e026-245a-4240-b8b2-90883c91b77a)

---

## Part D. Set up the Display Clock Demo

In this part, I edited the `screen_clock.py` file and implemented the logic to show real-time date and time on the MiniPiTFT screen.

### Before (original `TODO` placeholder)

```python
# TODO: show the time here
```

### After (my implementation)

```python
while True:
    # Clear the screen background
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Get current time in MM/DD/YYYY HH:MM:SS format
    now = time.strftime("%m/%d/%Y %H:%M:%S")

    # Set text position
    text_x = 20
    text_y = height // 2 - 10

    # Draw the time on the screen
    draw.text((text_x, text_y), now, font=font, fill="#FFFFFF")

    # Refresh the display
    disp.image(image, rotation)

    # Update once per second
    time.sleep(1)
```

**Result:**

* The MiniPiTFT screen now displays the current date and time (to the second).
* The display refreshes once every second, and the background is cleared each cycle to avoid ghosting.
![545386b84de54e809a3dc451e7169cea](https://github.com/user-attachments/assets/74871335-b2e7-42db-bfbb-2c2a6a0bdb3c)


---

## Part G.
Individual Work (Dean Xu)
<img width="1079" height="1527" alt="image" src="https://github.com/user-attachments/assets/f54b7821-8697-464c-9edb-e37d32bde717" />

Wenzhuo Ma: The 3D effect is very creative and makes the idea stand out. I personally really like how it turns the passing of time into something you can almost touch and see. It’s a simple but striking reminder to value every hour, and the image grows more powerful as the wall slowly empties.

# Lab 2 Part 2

**Group Work (Dean Xu, Thomas Knoepffler, Carrie Wang, Xiaocheng Li Julia Chen)**

## Assignment that was formerly Lab 2 Part E.

### Modify the barebones clock to make it your own

Does time have to be linear? How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)

Can you make time interactive? You can look in `screen_test.py` for examples for how to use the buttons.

Please sketch/diagram your clock idea. (Try using a [Verplank digram](http://www.billverplank.com/IxDSketchBook.pdf)!

**We strongly discourage and will reject the results of literal digital or analog clock display.**

\*\*\***A copy of your code should be in your Lab 2 Github repo.**\*\*\*

For the next part of this lab, our team came together to conceptualize a kind of clock that we could collectively work on. We came together with our initial ideas and deliberated on common themes that resonated with eachother. We decided to go with an idea we were ideating upon in last semester's Design for Phsyical Interaction class in Ithaca, an alarm clock that pours water on the user's head when it is time to wake up. The device would be a playful frustration for user's morning routine, adding a comedic schadenfreude to begrudgingness that is present in most traditional alarm clocks. 

![Storyboard 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Storyboard_1.jpg)

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Storyboard_2.jpg" alt="Storyboard 2" width="500"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Storyboard_3.jpg" alt="Storyboard 3" width="500"/>
</p>


**AI Usage:** Storyboard 7 generated using Google (Gemini). All original artifacts preserved._ </mark>

**Original Prompt:** "Please design product renderings for a water-based alarm clock. The alarm clock's base should be a clear water tank with a digital time display. The robotic arm of the alarm clock should have a nozzle at its end, capable of extending over the bed to aim at a sleeping person's face. Ensure the bedside table is flush with the bed, and a plant is placed on the bedside table. For the second consecutive story image, please show the alarm clock display reading 'Wake Up' with a water droplet icon, while the nozzle gently mists a small amount of water onto a naturally waking person with slightly opened eyes."_ </mark>


We utilized both the MiniPiTFTF to display a short 10 second count down followed by a "WAKE UP!!!" message on the screen, and a small Stepper Motor that would hold a cup of water and pour it at the end of the countdown. This required a careful consideration of we might use multi-threading functions so as to not overlap protocols with one another, but still alow the user to have various controls. We also needed to change our initial pin setup, eventually using a pin extender add-on that would let us use shared pins. A 3D printed platform was made to hold the electronics assembly and a cardboard enclosure was created to house the wires. The clock was then decorated with office decor to make more appropriate for a domestic setting.

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_1.jpg" alt="Assembly 1" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_2.jpg" alt="Assembly 2" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_3.jpg" alt="Assembly 3" width="333"/>
</p>

<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_4.jpg" alt="Assembly 1" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_5.jpg" alt="Assembly 2" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Assembly_6.jpg" alt="Assembly 3" width="333"/>
</p>


The device was situated to hang over a shelf or other elevation above a bed. The display showcasing the moment of waterfall. A secondary function had to be incorporated onto the other button on the MiniPiTFTF to adjust the Stepper Motor to be in the correct position. In hindsight, this is a limitation of the Stepper Motor where it cannot be precise in the angle positioning, rather it can only to take a set of steps towards a particular direction. In a future implementation, it would be ideal to use a Servo Motor instead. The demostration showed that the device worked in concept, although considering the anticipation and depending on the sleeping position, the moment of waterfall can be a little...unexpected.


<p align="center">
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Internals_1.jpg" alt="Internals 1" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Internals_2.jpg" alt="Internals 2" width="333"/>
  <img src="https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/Internals_3.jpg" alt="Internals 3" width="333"/>
</p>

![View 1](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/View_1.jpg)
![View 2](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/View_2.jpg)
![View 3](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Images/View_3.jpg)

## Assignment that was formerly Part F.

## Make a short video of your modified barebones PiClock

**Take a video of your PiClock.**

Our code can be found at [water_alarm_clock.py](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/water_alarm_clock.py)

**AI Usage:** Utilized assistance from ChatGPT for the writing of code.

**Pros:** The code was very quick to generate and was pretty adaptive to the broader context of the task. ChatGPT is very adept at remembering context for extended converations and can call-back to various instances to revise earleir versions of the genrerated code, which was ideal for building upon both the Stepper Motor and the MiniPiTFT functionality._ 

**Cons:** Often times, ChatGPT can often get stuck in a suggestion loop (i.e., suggesting code changes that already have been proposed but have no effect). The biggest limitation was the fact that it is very myopic when it comes to hardware issues. After deugging the code extensivley, we found the main issue to be hardware related (e.g., a change in wire setup) which was something that ChatGPT could not pick up on.


Watch the Clock View 1 here: [Clock 1 Video Link](https://drive.google.com/file/d/10chgjFNB8tFSNr2_Ddpjtch2ASdxsr6L/view?usp=sharing)

Watch the Clock View 2 here: [Clock 2 Video Link](https://drive.google.com/file/d/14ocHxTv_eLegoDM1LgB9Ggoroa1MLGL-/view?usp=sharing)

After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git add .
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!

[Update your Lab Hub](pull_updates/README.md) to get the latest content and requirements for Part 2.

Modify the code from last week's lab to make a new visual interface for your new clock. You may [extend the Pi](Extending%20the%20Pi.md) by adding sensors or buttons, but this is not required.

As always, make sure you document contributions and ideas from others explicitly in your writeup.

One other work that inspired us for this lab was the wearable art of Kathleen McDermott. Specifically Urban Armor #9, a harness that slaps the wearers face at 5:00pm to signal the end of the work day. Our work hopes to explore a similar design space, namley a satirical play on human interfacing objects and their relationship to ourselves and time.
![Inspiration 4](https://github.com/thomknoe/INFO-5345/blob/Fall2025/Lab%202/Proccess/Inspiration_4.jpg)

**Image Source:** Kathleen McDermott, Urban Armor #9 (2019).

Collaborators: Thomas Knoepffler (Hardware & Assembly), Carrie Wang (Storyboards & Editor), Xiaocheng Li (3D Modeling), Julia Chen (Developer & Debugger), Dean Xu (AI Artist)

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. What each person did should be explicitly documented. Make sure the page for the group turn in is linked to your Interactive Lab Hub page.

