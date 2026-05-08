
# Environmental Digital Twin & Agentic AI Visualizer

## 📌 Project Overview
This project is an **Environmental Digital Twin** designed to bridge the gap between raw atmospheric data and real-time personal health impacts. Developed as a cyber-physical monitoring solution, the system uses an **Agentic Logic Engine** to intersect real-time environmental telemetry with a **User Activity Profile**. 

By applying an engineering "Gain Factor" to pollutant exposure, the system provides autonomous, real-time health decisions and smart-city navigation insights, moving beyond simple data tracking into the realm of **Prescriptive Analytics**.

---

## 🚀 Key Features
* **Agentic Decision Engine:** A rule-based AI that interprets the environment and generates emergency protocols (e.g., "Immediate indoor retreat") or environmental advice ("Ventilator Advisor" for window control).
* **Dynamic Risk Scoring (PRS):** A personalized risk index ($0-100$) calculated by modulating pollutant concentrations with the user’s physical exertion levels (Resting, Walking, or Heavy Exercise).
* **WHO Compliance Benchmarking:** Automated real-time cross-referencing of $PM_{2.5}, PM_{10}, SO_2, NO_2,$ and $CO$ against **World Health Organization** safety limits.
* **Geospatial Intelligence:** Integrated **Nominatim API** for coordinate-based location fetching and **Oxygen Oasis** identification (finding the nearest clean-air parks like *Saras Baug* or *Empress Garden*).
* **Triple-Axis Visualization:** * **Pollution Fingerprint (Radar Chart):** Identifies the unique chemical "signature" of an area.
    * **Exposure Forecast:** A 6-hour predictive trend of personal risk units.
    * **WHO Compliance Bar:** Direct visual comparison of current data vs. international safety standards.

---

## 🛠️ Technical Architecture
The system operates as a modular data pipeline:
1.  **Ingestion Layer:** REST API calls to OpenStreetMap (Geolocation) and WAQI (Air Quality).
2.  **Processing Layer:** Data normalization and risk-factor multiplication using **Pandas** and **NumPy**.
3.  **Logic Layer:** The "Agent" translates numeric values into human-centric insights (Lung stress, Fatigue risk, Traffic probability).
4.  **HMI Layer:** High-fidelity plotting and UI generation via **Matplotlib**.

---

## 📊 Implementation Results
The system successfully processes real-time telemetry to provide:
* **Traffic Source Prediction:** Correlating $NO_2$ spikes with probable urban congestion peaks.
* **Health Impact Translation:** Predicting lung inflammation and metabolic exhaustion based on the current environment.
* **Environmental Risk Index:** A simplified $0-100$ score summarizing the overall threat level of the current location.
  
---

## 🔑 API Configuration
This project utilizes the **World Air Quality Index (WAQI)** API for real-time telemetry. 

**To run this project:**
1. Log in to the [WAQI API Dashboard](https://aqicn.org/data-platform/token/).
2. Copy your **API Token** from the dashboard.
3. Open the script and replace `"API_TOKEN"` with your unique key.
   

## 🖥️ Installation & Usage

### Option 1: Run on Google Colab (Recommended)
You can run this project directly in your browser:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ShravaniShalrushi/Environmental-Digital-Twin/blob/main/main.ipynb)

### Option 2: Local Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ShravaniShalrushi/Environmental-Digital-Twin.git](https://github.com/ShravaniShalrushi/Environmental-Digital-Twin.git)

2. **Install dependencies:**
   pip install requests pandas matplotlib numpy
   
4. **Run the digital twin**
    python main.py
  
