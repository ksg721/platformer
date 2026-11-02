# Vertical Ascent

Vertical Ascent is a precision 2D platforming game built with Python Arcade. The player climbs through ten connected levels by charging and aiming jumps with the mouse, navigating stationary and moving platforms, and avoiding solid walls.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Install Python 3.13, then install the required libraries with `python -m pip install arcade pyinstaller`.
2. Run the source version from the project folder with `python main.py`.
3. To build a Windows executable, run `pyinstaller --noconfirm --clean VerticalAscent.spec`; the finished game will be in `dist/VerticalAscent.exe`.

Instructions for using the software:

1. From the title screen, select **START CLIMB** or press Enter.
2. Use A/D or the arrow keys to move. Hold the left mouse button to charge a jump, aim with the mouse, and release the button to launch.
3. Climb all ten levels, use Escape to pause, and use the menus to adjust settings or view the leaderboard. Reach the final platform to finish the game.

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.13
* Python Arcade 3.3.3
* PyInstaller 6.11.0 for building the Windows executable

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Python Documentation](https://docs.python.org/3/)
* [Python Arcade Documentation](https://api.arcade.academy/en/latest/)
* [PyInstaller Documentation](https://pyinstaller.org/en/stable/)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add a full save-and-load system for unfinished runs, including the current level and player position.
* [ ] Add more visual themes, animations, and environmental artwork for the ten levels.
* [ ] Improve perfromance.
