
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# 1. INPUT SECTION
# -----------------------------
print("--- INITIALIZING ENVIRONMENTAL AGENT ---")
API_TOKEN = "         "
area = input("👉 Enter Area/City Name: ")

print("\n--- User Activity Profile ---")
print("1: Resting | 2: Walking | 3: Running/Heavy Exercise")
activity_input = input("👉 Select current activity level (1-3): ")

# Map activity to breathing multiplier (ENTC logic: Gain Factor)
activity_map = {"1": 1.0, "2": 2.5, "3": 5.0}
activity_level = activity_map.get(activity_input, 1.0)

print(f"\n[SYSTEM] Fetching live data for {area}...")

# -----------------------------
# 2. GEOLOCATION & DATA FETCH
# -----------------------------
headers = {"User-Agent": "Environmental-Agentic-AI-System"}
geo_url = f"https://nominatim.openstreetmap.org/search?q={area}&format=json&limit=1"
geo_response = requests.get(geo_url, headers=headers)

if not geo_response.json():
    print("❌ Location not found. Please check spelling.")
    exit()

geo_data = geo_response.json()
lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_TOKEN}"
data = requests.get(url).json()

if data["status"] != "ok":
    print("❌ No monitoring station nearby.")
    exit()

iaqi = data["data"]["iaqi"]
aqi = data["data"]["aqi"]
temp = iaqi["t"]["v"] if "t" in iaqi else "N/A"
humidity = iaqi["h"]["v"] if "h" in iaqi else "N/A"

# Pollutant Processing
pollutants_list = ["co","no2","so2","pm25","pm10"]
pollutants = {k: iaqi[k]["v"] for k in pollutants_list if k in iaqi}
df = pd.DataFrame(list(pollutants.items()), columns=["Pollutant","Value"])

# -----------------------------
# 3. WHO SAFETY & RISK (ORIGINAL LOGIC)
# -----------------------------
safety_limits = {"co": 9, "no2": 100, "so2": 75, "pm25": 15, "pm10": 45}
df["Safety_Limit"] = df["Pollutant"].map(safety_limits)
df["Excess_%"] = (((df["Value"] - df["Safety_Limit"]) / df["Safety_Limit"]) * 100).round(2)

def classify_risk(row):
    if row["Value"] <= row["Safety_Limit"]: return "Safe"
    elif row["Excess_%"] < 50: return "Moderate"
    elif row["Excess_%"] < 150: return "High"
    else: return "Severe"

df["Risk_Level"] = df.apply(classify_risk, axis=1)
risk_index = int(max(0, min(100, df["Excess_%"].mean())))

# -----------------------------
# 4. AGENTIC FEATURE ENGINE
# -----------------------------

# [Feature: PRS] Dynamic Pollution Risk Score
prs = min(100, (aqi * activity_level) / 5)

# [Feature: Forecast] Next-Hour Prediction (Micro Forecast)
hours = [datetime.now() + timedelta(hours=i) for i in range(7)]
prediction_trend = [aqi * (1 + 0.05 * np.sin(i)) * activity_level for i in range(7)]

# [Feature: Health] Impact Translator
def get_health_data(score):
    if score > 70: return "CRITICAL", "High Inflammation", "Rapid Exhaustion"
    if score > 40: return "MODERATE", "Mild Congestion", "Fatigue Risk"
    return "LOW", "Normal", "Negligible"
h_label, lung_stress, fatigue_risk = get_health_data(prs)

# [Feature: Smart City] Contextual Logic
traffic_prob = "High (Congestion Peak)" if aqi > 120 or pollutants.get("no2", 0) > 40 else "Low/Fluid"
vent_msg = "❌ CLOSE WINDOWS" if aqi > 110 else "✅ OPEN WINDOWS" if aqi < 55 else "⏳ CAUTION"
oasis = "Saras Baug / Empress Garden" if "pune" in area.lower() else "Local Public Green Zone"

# [Feature: Decision] Real-time AI Strategy
if "Severe" in df["Risk_Level"].values or prs > 75:
    ai_decision = "🚨 EMERGENCY: Immediate indoor retreat. Activate air purifiers."
elif "High" in df["Risk_Level"].values or prs > 50:
    ai_decision = "⚠️ WARNING: Delay travel by 1 hour. Switch to indoor activity."
else:
    ai_decision = "✅ SAFE: Conditions are within acceptable limits for you."

# -----------------------------
# 5. FINAL COMBINED OUTPUT
# -----------------------------
print("\n" + "="*60)
print(f"  ENVIRONMENTAL DIGITAL TWIN REPORT: {area.upper()}")
print("="*60)
print(f"LIVE DATA | AQI: {aqi} | Temp: {temp}°C | Humidity: {humidity}%")

print("\n[SECTION 1: ORIGINAL POLLUTANT ANALYSIS]")
print(df[["Pollutant","Value","Safety_Limit","Excess_%","Risk_Level"]])
print(f"\nEnvironmental Risk Index (0-100): {risk_index}")

print("\n" + "-"*30)
print("🔥 UNIQUE FEATURES & HEALTH")
print("-"*30)
print(f"1. Dynamic Risk Score (PRS):    {prs:.1f}/100")
print(f"2. 6-Hour Exposure Trend:       {int(prediction_trend[-1])} Units")
print(f"3. Lung Stress Level:           {lung_stress}")
print(f"4. Real-time AI Decision:        {ai_decision}")

print("\n" + "-"*30)
print("🌐 SMART CITY INSIGHTS")
print("-"*30)
print(f"🏎‍🟀 Probable Traffic Source:     {traffic_prob}")
print(f"🏠 Ventilator Advisor:          {vent_msg}")
print(f"🌳 Oxygen Oasis Locator:       {oasis}")
print("="*60)

# -----------------------------
# 6. TRIPLE VISUALIZATION (RADAR + TREND + BAR)
# -----------------------------
fig = plt.figure(figsize=(18, 6))

# Chart 1: Radar Chart (Pollution Signature)
ax1 = fig.add_subplot(131, polar=True)
categories = df["Pollutant"].tolist()
values = df["Value"].tolist()
values += values[:1] # Close the radar loop
angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
angles += angles[:1]
ax1.fill(angles, values, 'teal', alpha=0.3)
ax1.plot(angles, values, color='teal', linewidth=2)
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories)
ax1.set_title("Pollution Fingerprint (Radar)", pad=20)

# Chart 2: Exposure Trend
ax2 = fig.add_subplot(132)
time_labels = [h.strftime("%H:%M") for h in hours]
ax2.plot(time_labels, prediction_trend, marker='o', color='darkorange', linewidth=2)
ax2.fill_between(time_labels, prediction_trend, color='orange', alpha=0.1)
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.4, label="Danger Line")
ax2.set_title("6-Hour Personal Exposure Forecast")
ax2.set_ylabel("Risk Units")
ax2.legend()

# Chart 3: WHO Compliance Bar
ax3 = fig.add_subplot(133)
x = np.arange(len(df))
ax3.bar(x, df["Value"], color='skyblue', label='Current')
ax3.bar(x, df["Safety_Limit"], alpha=0.3, color='grey', label='WHO Limit')
ax3.set_xticks(x)
ax3.set_xticklabels(df["Pollutant"])
ax3.set_title("Pollutant vs WHO Limits")
ax3.legend()

plt.tight_layout()
plt.show()
