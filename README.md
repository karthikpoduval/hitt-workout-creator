# HIIT Workout Video Creator

A Python tool that automatically stitches together individual workout clips into a professional Tabata-style HIIT (High-Intensity Interval Training) video. 



## Features
* **Customizable Length**: Choose the number of rounds via command line.
* **Smart Looping**: Automatically loops short workout clips to fill the 40-second work interval.
* **Visual Timers**: 
  - Shrinking progress bar at the bottom.
  - On-screen numeric countdown for both work and rest phases.
* **Rest UI**: Displays a "Rest" message and previews the next exercise name during the 20-second break.
* **Audio Mixing**: Loops your provided background music and ducks volume for a polished feel.
* **Clean Text Rendering**: Uses fixed-box captioning to prevent text clipping on Windows/Linux.

## Prerequisites
* **Python 3.10+**
* **FFmpeg**: Must be installed and added to your system PATH.
* **ImageMagick**: Required by MoviePy to render text.
  - *Note: On Windows, install and ensure you check 'Install legacy utilities' during setup.*

## Installation
Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/hitt-workout-creator.git](https://github.com/yourusername/hitt-workout-creator.git)
   cd hitt-workout-creator
  ```

## Create and activate a virtual environment

  ```bash
  python -m venv venv-hitt-workout-creator
  source venv-hitt-workout-creator/bin/activate
  ```

## On Windows use: 
  ```bash
  .\venv-hitt-workout-creator\Scripts\activate.ps1
   ```
you also may need to run this command on certain windows systems to allow execution on current shell
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

## Install dependencies
  ```bash
  pip install moviepy
  ```
## Usage
Prepare a folder containing .mov files named after the exercise (e.g., push_ups.mov, mountain_climbers.mov).Run the script:
```bash
  python hitt_workout_creator.py --folder ./videos --music track.mp3 --rounds 8 --title "HITT Routine"
 ```

### Arguments:

| Argument | Required | Description |
| --- | --- | --- |
| --folder | Yes | Path to the directory containing your .mov workout clips. |
| --music  | Yes | Path to the background music file (mp3/wav/wav). |
| --rounds | No  | Total number of exercise intervals to generate (Default: 4). |
| --title  | No  | The main title text shown during the first 10 seconds. |
| --out    | No  | The filename for the final rendered video (Default: hitt_session.mp4). |

