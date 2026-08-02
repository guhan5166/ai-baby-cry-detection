import sounddevice as sd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
import time

# =====================================
# CONFIGURATION (Update These!)
# =====================================
# Telegram Config
BOT_TOKEN = "Replace it"
CHAT_ID = "Replace it"

# Blynk Config (Connects to your ESP8266)
BLYNK_AUTH = "Replace it"
# If latency is high, try: sgp1.blynk.cloud or lon1.blynk.cloud
BLYNK_URL = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH}&v1=1"

# Audio Settings
SAMPLE_RATE = 16000
DURATION = 2      # seconds of audio to analyze per loop
THRESHOLD = 0.80  # Cry detection sensitivity (0.0 to 1.0)

# =====================================
# LOAD MODELS
# =====================================
print("--- Initializing AI Systems ---")
print("Loading YAMNet from TFHub...")
yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")

print("Loading Your Cry Classifier...")
# Ensure this file is in the same folder as this script!
cry_model = tf.keras.models.load_model("cry_detection_yamnet_robust.keras")

print("✅ Systems Online. Ready to protect.")

# =====================================
# HELPER FUNCTIONS
# =====================================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        print("⚠️ Failed to send Telegram alert")

def trigger_blynk_cradle():
    print("📡 Sending Trigger to ESP8266...")
    try:
        response = requests.get(BLYNK_URL, timeout=5)
        if response.status_code == 200:
            print("🚀 Success: Cradle is now swinging!")
        else:
            print(f"❌ Blynk Error: Status Code {response.status_code}")
    except Exception as e:
        print(f"❌ Network Error: Could not reach Blynk Cloud. {e}")

# =====================================
# MAIN MONITORING LOOP
# =====================================
print("\n🎤 Listening for baby cries... (Press Ctrl+C to stop)")

while True:
    try:
        # 1. Record Audio
        audio = sd.rec(int(DURATION * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE,
                       channels=1,
                       dtype='float32')
        sd.wait()
        audio = np.squeeze(audio)

        # 2. Extract YAMNet Embeddings
        # YAMNet converts raw audio into a "fingerprint" the classifier understands
        scores, embeddings, _ = yamnet_model(audio)
        embedding = tf.reduce_mean(embeddings, axis=0).numpy()
        embedding = np.expand_dims(embedding, axis=0)

        # 3. AI Prediction
        prediction = cry_model.predict(embedding, verbose=0)[0][0]

        print(f"Cry Probability: {prediction:.3f}")

        # 4. Take Action if Cry Detected
        if prediction > THRESHOLD:
            print("\n🚨 CRY DETECTED! Confidence:", round(prediction, 2))
            
            # Action A: Notify Parents
            send_telegram(f"⚠️ Baby is crying!\nConfidence: {prediction:.2f}")
            
            # Action B: Start Mechanical Cradle
            trigger_blynk_cradle()
            
            # Action C: Anti-Spam Wait
            # Wait 20 seconds so the AI doesn't double-trigger 
            # while the 15-second servo loop is still running.
            print("⏳ Cooling down while cradle swings... (20s)")
            time.sleep(20)
            print("🎤 Resuming monitoring...")

        # Small pause between normal samples
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 System stopped by user.")
        break

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        time.sleep(5)
# If Code Not Working Message Me In Instagram "guhan.04"
