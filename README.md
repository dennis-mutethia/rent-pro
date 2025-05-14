# RentPro

**Manage Your Rentals, Master Your Success**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/your-username/rentpro.svg)](https://github.com/your-username/rentpro/issues)

**RentPro** is a modern, all-in-one rental management platform crafted for **landlords**, **property managers**, and **Airbnb hosts**. With a sleek interface and a touch of Swahili-inspired warmth (think geometric patterns and vibrant hues), RentPro simplifies property management—from tenant screening to payment processing and guest communication. Our mission is to empower rental managers with professional, intuitive tools that make managing properties efficient, reliable, and welcoming.

---

## 🚀 Features

- **Unified Dashboard**: Centralize property listings, bookings, and financials in one place.
- **Automated Workflows**: Streamline rent collection, lease renewals, and guest check-ins.
- **Multi-User Support**: Tailored for landlords (long-term rentals), property managers (multiple properties), and Airbnb hosts (short-term stays).
- **Financial Tools**: Track rent payments, expenses, and generate tax reports effortlessly.
- **Booking System**: Calendar integration with dynamic pricing for Airbnb hosts.
- **Maintenance Hub**: Log and resolve maintenance requests with ease.
- **Analytics**: Gain insights into occupancy rates, revenue, and property performance.
- **Mobile Accessibility**: Manage on the go with iOS and Android apps.
- **Cultural Aesthetic**: Subtle Swahili-inspired design (e.g., woven patterns in burnt orange and deep blue) for a warm, global feel.

---

## 🛠 Installation

Get RentPro up and running locally for development or testing.

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **PostgreSQL** (v12 or higher)
- **Git** for cloning the repo
- **Docker** (optional, for containerized setup)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/rentpro.git
   cd rentpro
   ```

2. **Install Dependencies**:
   - Backend (Python/Flask):
   ```bash
   pip install -r backend/requirements.txt
   ```

  - Frontend (React)**:
  ```bash
  cd frontend
  npm install
  ```

3. **Set Up Environment Variables**:
  - Create a .env file in backend/ based on .env.example:
  ```env
  DATABASE_URL=postgresql://user:password@localhost:5432/rentpro
  SECRET_KEY=your-secret-key
  API_KEY=your-api-key
  ```

5. **Initialize the Database**:
  ```bash
  cd backend
  flask db init
  flask db migrate
  flask db upgrade
 ```

6. **Run the Application**:
 - Backend:
  ```bash
  cd backend
  flask run
 ```

 - Frontend:
  ```bash
  cd frontend
  npm start
 ```

7. **Access RentPro**:
 - Frontend: http://localhost:3000
 - Backend API: http://localhost:5000
