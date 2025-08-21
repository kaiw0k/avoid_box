# Block Jump Adventure

A fast-paced, challenging platformer game built with Python and Pygame where you control a red block trying to survive
in a world of moving green blocks.

## Game Features

- **Dynamic Platform System**: Intelligently generated platforms with balanced distances and heights
- **Challenging Gameplay**: Dodge green blocks coming from both sides
- **Progressive Difficulty**: Speed and spawn rate increase as your score goes up
- **Double Jump Mechanic**: Master the double jump to survive longer
- **Platform Drop**: Press down + space to drop through platforms
- **Score System**: Score points by successfully dodging green blocks

## Controls

- **Left/Right Movement**: Arrow keys or A/D
- **Jump**: Space bar
- **Platform Drop**: Down arrow + Space
- **Toggle Fullscreen**: F key
- **Quit Game**: ESC key

## Game Mechanics

### Player Abilities

- Double jump capability
- Platform drop-through
- Smooth movement control

### Obstacles

- Green blocks spawn from both sides
- Dynamic spawn rates based on score
- Blocks can spawn at player height for extra challenge

### Scoring System

- Score points by successfully dodging green blocks
- Higher scores increase game difficulty
- Try to beat your high score!

### Platform Generation

- Smart platform placement algorithm
- Balanced horizontal and vertical distances
- Ensures playable and challenging layouts

## Technical Details

Built using:

- Python 3
- Pygame library
- Object-oriented architecture
- Dynamic difficulty scaling
- Smart platform generation algorithms

## Installation

1. Ensure Python 3 is installed
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python src/main.py
```

## Building Standalone Version

On macOS, use the included build script:

```bash
bash build_mac.sh
```

## Development Features

- Modular code structure
- Resolution scaling support
- Fullscreen capability
- Frame rate locked at 60 FPS
- Dynamic resource management

## Game Tips

- Use double jumps strategically
- Watch both sides of the screen
- Use platform drops to escape tight situations
- Stay near the center when possible
- Plan your movements ahead

Enjoy the challenge and try to achieve the highest score possible!
