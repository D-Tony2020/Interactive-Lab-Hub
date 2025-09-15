# Interactive Prototyping: The Clock of Pi

**Collaborators:** Dean Xu (hx332)
*(Please add the names of any lab partners here, if applicable.)*

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
