<!-- Custom SVG Banner -->
<div align="center">
  <!-- Inline SVG: bus, chart, AI chip icons + title -->
  <svg width="100%" height="220" viewBox="0 0 1200 220" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <defs>
      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#4facfe" />
        <stop offset="50%" stop-color="#00f2fe" />
        <stop offset="100%" stop-color="#43e97b" />
      </linearGradient>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.15"/>
      </filter>
    </defs>

    <!-- Background rounded rect -->
    <rect x="10" y="10" rx="18" ry="18" width="1180" height="200" fill="url(#g1)" filter="url(#shadow)" />

    <!-- Left: stylized bus icon -->
    <g transform="translate(70,28) scale(1.2)">
      <rect x="0" y="40" rx="10" ry="10" width="160" height="70" fill="#ffffff" opacity="0.95" />
      <rect x="10" y="20" rx="6" ry="6" width="140" height="30" fill="#ffffff" opacity="0.95" />
      <circle cx="40" cy="120" r="12" fill="#222" />
      <circle cx="120" cy="120" r="12" fill="#222" />
      <rect x="24" y="56" width="40" height="24" fill="#4facfe" rx="4" />
      <rect x="76" y="56" width="60" height="24" fill="#00f2fe" rx="4" />
    </g>

    <!-- Center: Title & Tagline -->
    <g transform="translate(280,40)">
      <text x="0" y="36" font-family="Inter, Arial, sans-serif" font-size="34" fill="#ffffff" font-weight="800">BUSIQ Transit Dashboard  🚍</text>
      <text x="0" y="80" font-family="Inter, Arial, sans-serif" font-size="16" fill="#f7fffb">A real-time public transit monitoring &amp; optimization dashboard</text>

      <!-- Team / Hackathon badge -->
      <g transform="translate(0,105)">
        <rect x="0" y="-16" rx="8" ry="8" width="340" height="36" fill="#ffffff" opacity="0.12" />
        <text x="12" y="10" font-family="Inter, Arial, sans-serif" font-size="14" fill="#ffffff">Hackathon Project • Team: <tspan font-weight="700">The Dev Force</tspan></text>
      </g>
    </g>

    <!-- Right: icons (chart + AI chip) -->
    <g transform="translate(780,28)">
      <!-- Chart icon -->
      <g transform="translate(0,10)">
        <rect x="0" y="0" width="140" height="90" rx="10" fill="#ffffff" opacity="0.95" />
        <rect x="18" y="28" width="18" height="38" rx="3" fill="#43e97b" />
        <rect x="46" y="16" width="18" height="50" rx="3" fill="#00f2fe" />
        <rect x="74" y="8" width="18" height="58" rx="3" fill="#4facfe" />
      </g>

      <!-- AI chip icon -->
      <g transform="translate(0,110)">
        <rect x="0" y="0" width="140" height="70" rx="12" fill="#ffffff" opacity="0.95" />
        <rect x="18" y="14" width="104" height="42" rx="6" fill="#0b1a2b" />
        <text x="70" y="40" font-family="Inter, Arial, sans-serif" font-size="12" fill="#00f2fe" text-anchor="middle">AI</text>
      </g>
    </g>

  </svg>
</div>

---

# 📊 BUSIQ Transit Dashboard

**A real-time public transit monitoring and optimization dashboard**

<p align="center">
  <img src="assets/dashboard-preview.png" alt="BUSIQ Dashboard Screenshot" width="85%">
</p>

---

## 🏆 Hackathon & Team

**Hackathon project** — proudly built by **The Dev Force**.

**Team ID:** `The Dev Force`

Include your hackathon name, submission link, or mentor details here if you want them printed on the README or prize submission PDF.

---

## 🏅 Badges

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Flask](https://img.shields.io/badge/Flask-2.0-lightgrey?logo=flask)  
![License](https://img.shields.io/badge/License-MIT-green)  
![Status](https://img.shields.io/badge/Status-Active-brightgreen)  
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)  
![Stars](https://img.shields.io/github/stars/yourusername/busiq-transit-dashboard?style=social)

---

## 📖 Introduction

**BUSIQ** is a web-based dashboard built to revolutionize public transit management. It enables operators to:

- 🚍 **Track buses in real-time**
- ⚠️ **Detect operational issues like bus bunching**
- 📲 **Respond instantly with actionable alerts**

With **data-driven insights, live monitoring, and AI-powered optimization**, BUSIQ reduces delays, optimizes routes, and improves the passenger experience.

---

## ✨ Features

- 🚍 **Real-time Bus Tracking** – Live bus locations & occupancy on an interactive map.
- 📊 **Live Metrics** – KPIs: on-time performance, total buses, avg. occupancy.
- ⚠️ **Smart Alerts** – Instant notifications for delays, re-routing, bunching, and issues.
- 📈 **Fleet Optimization** – AI-based recommendations (e.g., hold bus for 60s).
- 📉 **Data Visualization** – Charts for ridership forecasts & analytics.
- 🌙 **Responsive UI** – Clean, mobile-friendly, supports dark mode.

---

## 🛠️ Technologies Used

### 🔹 Backend

- Python • Flask • Flask-SocketIO • Flask-CORS • SQLite3

### 🔹 Frontend

- HTML / CSS • Tailwind CSS • JavaScript
- Leaflet.js (maps) • Chart.js (graphs) • Socket.IO Client

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python **3.x**
- **pip** (comes with Python)

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/busiq-transit-dashboard.git
cd busiq-transit-dashboard

# Install dependencies
pip install -r requirements.txt
```

### ▶️ Running the Application

1️⃣ Setup the database

```bash
python setup_database.py
```

→ Creates `transit.db` with routes, buses, and alerts.

2️⃣ Start the backend server

```bash
python app.py
```

→ Runs Flask + WebSocket server.

3️⃣ Start the data simulator

```bash
python mock_bus_sender.py
```

→ Streams live bus data & alerts to backend.

4️⃣ Open the dashboard  
→ Simply open `index.html` in your browser.

---

## 📂 Project Structure

```bash
busiq-transit-dashboard/
│── app.py               # Flask app & WebSocket server
│── setup_database.py    # Initializes SQLite DB
│── mock_bus_sender.py   # Simulates bus data
│── transit.db           # Database file
│── index.html           # Dashboard frontend
│── requirements.txt     # Dependencies
│── assets/              # Images, screenshots, logos
```

---

## 🔄 How It Works

1. **Database Setup** → `setup_database.py` creates `transit.db`.
2. **Server Start** → `app.py` runs Flask + WebSocket backend.
3. **Simulation** → `mock_bus_sender.py` streams mock bus data.
4. **Processing** → Backend detects delays, bunching & pushes updates.
5. **Live Dashboard** → `index.html` shows real-time updates (map, charts, alerts).

---

## ⚡ Conclusion

🚍 BUSIQ makes public transport **smarter, faster, and more reliable.**  
It empowers operators to:

✅ Improve efficiency  
✅ Reduce delays  
✅ Deliver a better passenger experience

### 🔮 Future Scope

- GPS device integration
- Predictive ML analytics
- Multi-city fleet support

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

<!-- Footer -->
<div align="center">
  <p>Made with ❤️ for Smart Transit Systems • <strong>The Dev Force</strong></p>
  <p><small>Hackathon project — good luck with your submission!</small></p>
</div>
