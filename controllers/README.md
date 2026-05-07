# Controllers Folder

This folder contains all the **robot controller source code** for the Maze Robot project in Webots.

The controller is structured using a **modular architecture**:

- Sensors → FSM → Movement

All controller implementation files are located inside the `main_controller/` subfolder.

---

## 📁 Folder Structure

**controllers/:**

- README.md
- **main_controller/:**
  - main_controller.py
  - fsm.py
  - navigation.py
  - movement.py
  - sensors.py
  - config.py
  - utils.py

---

## 📄 File Overview

### 1. `main_controller/main_controller.py`

- **Purpose:** Entry point of the robot controller (executed by Webots).
- Contains the **main control loop**.
- Integrates:
  - sensor readings (`sensors.py`)
  - decision logic (`fsm.py`)
  - movement execution (`movement.py`)
- Responsible for coordinating all modules.

---

### 2. `main_controller/fsm.py`

- **Purpose:** Implements the **Finite State Machine (FSM)**.
- Handles **decision-making logic**.
- Determines the robot’s next action based on sensor input.
- Outputs actions such as:
  - `MOVE_FORWARD`
  - `TURN_LEFT`
  - `TURN_RIGHT`

---

### 3. `main_controller/navigation.py`

- **Purpose:** Contains **navigation and decision helper logic**.
- Processes sensor data to support FSM decisions.
- Can include:
  - wall-following logic
  - multi-condition checks
  - path decision rules

---

### 4. `main_controller/sensors.py`

- **Purpose:** Handles all **sensor data collection**.
- Reads data from:
  - distance sensors (front, left, right)
- Returns structured sensor data to the FSM.

---

### 5. `main_controller/movement.py`

- **Purpose:** Controls the robot’s **actuators (motors)**.
- Implements movement functions:
  - move forward
  - turn left / right
  - stop
- Executes actions decided by the FSM.

---

### 6. `main_controller/config.py`

- **Purpose:** Stores **configuration values**.
- Includes:
  - sensor thresholds
  - movement speeds
- Central place for tuning robot behaviour.

---

### 7. `main_controller/utils.py` (optional)

- **Purpose:** Contains **helper functions** used across modules.
- Examples:
  - math utilities
  - reusable logic
- Helps keep code clean and modular.

---

## ⚠️ Important Notes

- All modules must use **consistent naming**:
  - FSM states (e.g. `"MOVE_FORWARD"`)
  - function names across files
- Do NOT mix responsibilities across files.
- Each module should focus on a **single responsibility**.

---

## 🔀 Git Workflow

- Each team member works mainly on their assigned module:
  - FSM → `fsm.py`
  - Movement → `movement.py`
  - Sensors → `sensors.py`, `config.py`, `navigation.py`
- Merge work into `develop` for integration.
- Only merge to `main` when the system is stable.

---

## 🚀 How It Works (High-Level)
