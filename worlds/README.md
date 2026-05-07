# Worlds Folder

This folder contains all **Webots simulation environment files** for the Maze Robot project.  
It includes the maze layout, obstacles, and any assets used for the robot simulation.

---

## File Overview

### 1. `world.wbt`

- **Purpose:** Main maze environment where the robot navigates.
- Defines walls, floor, robot starting position, and obstacles.
- Used as the primary testing and demonstration world.

### 2. `simple_test_world.wbt` (optional)

- **Purpose:** Optional small test environment for debugging sensors or movement.
- Allows faster testing without the full maze layout.

### 3. `robot_proto.proto` (optional)

- **Purpose:** Custom robot definition for the simulation.
- Includes robot dimensions, sensors, actuators, and appearance.

### 4. `assets`

- **Purpose:** Stores visual textures used in the world files, such as:
  - `hedge_wall.png` → wall appearance, 64x64 px (https://www.manytextures.com/texture/70/hedge-wall/)
  - `stone_ground.png` → floor appearance, 64x64 px (https://www.manytextures.com/texture/96/small-stone-ground-pavement/)
- Helps keep the world files organized and separates visuals from geometry.

---

## Notes

- Webots reads the world files from this folder; do not move or rename them after linking them in your simulation.
- If you add new walls, floors, or other environment objects, update the world files here.
- Keep textures small (64×64 or 128×128 px) for performance.
