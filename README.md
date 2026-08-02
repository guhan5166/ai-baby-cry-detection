# 👶 AI Baby Cry Detection & Smart Cradle System

An **AI-powered baby monitoring system** that detects infant crying using a microphone and a custom **YAMNet-based deep learning classifier**.

When a cry is detected, the system:

1. 🎤 Captures audio from the microphone
2. 🧠 Extracts audio features using **YAMNet**
3. 🤖 Uses a custom trained **Keras cry classifier**
4. 🚨 Detects whether the baby is crying
5. 📱 Sends an alert through **Telegram**
6. 📡 Sends a command to **Blynk IoT**
7. 🛏️ Triggers an **ESP8266-controlled smart cradle**
8. ⏳ Waits during a cooldown period to prevent repeated alerts

---

## 🏗️ System Architecture

```text
                 🎤 Microphone
                       │
                       ▼
                Audio Recording
                  16 kHz / 2 sec
                       │
                       ▼
                 🧠 YAMNet
                       │
                       ▼
              Audio Embeddings
                       │
                       ▼
        🤖 Custom Cry Classifier
       cry_detection_yamnet_robust.keras
                       │
                       ▼
              Cry Probability
                       │
                 > 0.80 ?
                  /       \
                NO         YES
                │            │
                │            ├──────────► 📱 Telegram Alert
                │            │
                │            └──────────► ☁️ Blynk IoT
                │                              │
                │                              ▼
                │                         ESP8266
                │                              │
                │                              ▼
                │                       🛏️ Smart Cradle
                │
                ▼
             Continue
             Monitoring
```

---

# ✨ Features

* 🎤 Real-time microphone monitoring
* 🧠 Google YAMNet audio feature extraction
* 🤖 Custom infant cry classification model
* 📊 Cry probability output
* 🚨 Automatic cry detection
* 📱 Telegram notifications
* ☁️ Blynk IoT integration
* 📡 ESP8266 control
* 🛏️ Automatic cradle activation
* ⏳ Anti-spam cooldown mechanism
* 🔄 Continuous monitoring
* 🛑 Safe shutdown using `Ctrl+C`

---

# 🧠 AI Model

This project uses **YAMNet** as the audio feature extractor.

YAMNet is a pretrained neural network designed for audio event classification.

Instead of training an entire audio recognition network from scratch, this project uses YAMNet to convert raw audio into meaningful **audio embeddings**.

The custom classifier then uses those embeddings to determine whether the recorded audio contains a baby cry.

### Processing pipeline

```text
Raw Audio
    ↓
YAMNet
    ↓
Audio Embeddings
    ↓
Mean Embedding
    ↓
Custom Keras Classifier
    ↓
Cry Probability
```

The trained model used by this project is:

```text
cry_detection_yamnet_robust.keras
```

---

# 🎤 Audio Configuration

The system records audio using:

| Parameter          |     Value |
| ------------------ | --------: |
| Sample Rate        |  16000 Hz |
| Recording Duration | 2 seconds |
| Channels           |      Mono |
| Data Type          |   Float32 |
| Cry Threshold      |      0.80 |

The relevant configuration is:

```python
SAMPLE_RATE = 16000
DURATION = 2
THRESHOLD = 0.80
```

The threshold can be adjusted depending on the desired sensitivity.

For example:

```text
0.90 → Fewer false alarms
0.80 → Default sensitivity
0.70 → More sensitive detection
```

---

# 🚨 Cry Detection

For every audio segment, the system generates a probability value.

Example:

```text
Cry Probability: 0.123
Cry Probability: 0.346
Cry Probability: 0.821
```

If the probability exceeds the configured threshold:

```text
Cry Probability > 0.80
```

the system considers the audio a cry.

Example:

```text
🚨 CRY DETECTED! Confidence: 0.82
```

---

# 📱 Telegram Alert

When crying is detected, the system sends a Telegram notification.

Example:

```text
⚠️ Baby is crying!
Confidence: 0.82
```

Telegram is used to remotely notify the parent/caregiver.

> **Security:** Never upload your real Telegram bot token or chat ID to GitHub.

Store your credentials securely using environment variables or another secret-management method.

---

# ☁️ Blynk IoT

The system communicates with the ESP8266 through **Blynk IoT**.

When a cry is detected, the Python program sends a request to the Blynk API.

```text
Python AI System
       │
       ▼
 Blynk Cloud
       │
       ▼
    ESP8266
       │
       ▼
 Smart Cradle
```

The Blynk virtual pin used by the current implementation is:

```text
V1
```

The ESP8266 receives the command and activates the cradle mechanism.

> **Security:** Never publish your real Blynk authentication token.

---

# 🛏️ Smart Cradle Operation

The complete system combines:

### AI side

```text
Microphone
   ↓
Python
   ↓
YAMNet
   ↓
Cry Classifier
```

### IoT side

```text
Python
   ↓
Blynk Cloud
   ↓
ESP8266
   ↓
Motor / Servo
   ↓
Cradle Movement
```

This allows the AI monitoring system to remotely control the physical cradle when crying is detected.

---

# ⏳ Cooldown System

To prevent repeated alerts and repeated cradle activation, the program uses a cooldown period.

Current value:

```python
time.sleep(20)
```

After detecting a cry:

```text
Cry detected
     ↓
Telegram alert
     ↓
Blynk trigger
     ↓
20-second cooldown
     ↓
Resume monitoring
```

This prevents the system from continuously triggering while the baby is still crying.

---

# 💻 Requirements

## Hardware

* 🎤 Microphone
* 💻 Computer / laptop capable of running Python
* 📡 ESP8266
* 🛏️ Smart cradle mechanism
* ⚙️ Servo/motor control hardware
* 🌐 Internet connection

## Software

* Python 3
* TensorFlow
* TensorFlow Hub
* NumPy
* SoundDevice
* Requests

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/smart-cradle-ai.git
```

Enter the project directory:

```bash
cd smart-cradle-ai
```

Create a virtual environment:

```bash
python3 -m venv cryenv
```

Activate it on Linux:

```bash
source cryenv/bin/activate
```

On Windows:

```powershell
cryenv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 📥 Model Setup

Place the trained model inside the `models` directory:

```text
models/
└── cry_detection_yamnet_robust.keras
```

The Python program should load it using:

```python
cry_model = tf.keras.models.load_model(
    "models/cry_detection_yamnet_robust.keras"
)
```

---

# 🔐 Configuration

The system requires:

```text
Telegram Bot Token
Telegram Chat ID
Blynk Authentication Token
```

These should be provided securely through environment variables or a local configuration file that is excluded using `.gitignore`.

Example environment variables:

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
export BLYNK_AUTH_TOKEN="YOUR_BLYNK_AUTH_TOKEN"
```

The Python program can then access them using:

```python
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BLYNK_AUTH = os.getenv("BLYNK_AUTH_TOKEN")
```

---

# ▶️ Running the System

Activate the virtual environment.

Linux:

```bash
source cryenv/bin/activate
```

Then run:

```bash
python cry_monitor.py
```

The program should display:

```text
--- Initializing AI Systems ---
Loading YAMNet from TFHub...
Loading Your Cry Classifier...
✅ Systems Online. Ready to protect.

🎤 Listening for baby cries...
```

During monitoring:

```text
Cry Probability: 0.132
Cry Probability: 0.284
Cry Probability: 0.791
Cry Probability: 0.846

🚨 CRY DETECTED! Confidence: 0.85
📡 Sending Trigger to ESP8266...
🚀 Success: Cradle is now swinging!
⏳ Cooling down while cradle swings... (20s)
```

Press:

```text
Ctrl + C
```

to stop the monitoring system.

---

# ⚙️ How It Works

### 1. Audio Recording

The microphone records a 2-second audio segment at 16 kHz.

### 2. YAMNet Feature Extraction

The recorded audio is passed to YAMNet.

```python
scores, embeddings, _ = yamnet_model(audio)
```

### 3. Embedding Generation

The YAMNet embeddings are averaged:

```python
embedding = tf.reduce_mean(
    embeddings,
    axis=0
).numpy()
```

### 4. Cry Classification

The custom Keras model receives the embedding:

```python
prediction = cry_model.predict(
    embedding,
    verbose=0
)[0][0]
```

### 5. Decision

The prediction is compared with the threshold:

```python
if prediction > THRESHOLD:
```

### 6. Remote Notification

Telegram sends an alert to the caregiver.

### 7. Cradle Activation

Blynk sends the command to the ESP8266.

### 8. Cooldown

The system waits before continuing detection.

---

# 📊 Example Output

```text
🎤 Listening for baby cries...

Cry Probability: 0.031
Cry Probability: 0.112
Cry Probability: 0.284
Cry Probability: 0.794
Cry Probability: 0.823

🚨 CRY DETECTED! Confidence: 0.82

📡 Sending Trigger to ESP8266...
🚀 Success: Cradle is now swinging!

⏳ Cooling down while cradle swings... (20s)

🎤 Resuming monitoring...
```

---

# ⚠️ Important Notes

### Internet Connection

Internet access is required for:

* Loading YAMNet from TensorFlow Hub
* Telegram notifications
* Blynk communication

### Microphone

Make sure the correct microphone/input device is available to `sounddevice`.

You can check available devices with:

```python
import sounddevice as sd
print(sd.query_devices())
```

### False Positives

The cry classifier is not guaranteed to perfectly distinguish crying from every environmental sound.

Performance can vary depending on:

* Background noise
* Microphone quality
* Baby's distance from microphone
* Cry intensity
* Room acoustics
* Dataset/model limitations

The threshold can be adjusted to balance sensitivity and false detections.

---

# 🚀 Future Improvements

Possible future improvements include:

* 🎧 Continuous streaming audio instead of 2-second recordings
* 🔇 Better background-noise filtering
* 🧠 Improved cry classification model
* 📊 Real-time monitoring dashboard
* 📈 Cry history and statistics
* 🗄️ Cloud database integration
* 📱 Dedicated mobile application
* 🔋 Battery-powered standalone AI device
* 🤖 Edge AI deployment on Raspberry Pi / ESP32-class hardware
* 🔊 Multiple baby sound classifications
* 💤 Sleep/activity monitoring
* 🌡️ Integration with temperature and humidity sensors

---

# 👨‍💻 Project

This project is part of an **AI and IoT-based Smart Cradle / Baby Monitoring System**.

The system combines:

```text
Artificial Intelligence
        +
Audio Processing
        +
IoT
        +
ESP8266
        +
Remote Notification
        +
Automated Cradle Control
```

The goal is to provide an automated system that can **detect infant crying, notify the caregiver, and initiate cradle movement remotely**.

---
