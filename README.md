# 🚀 Real-Time Chat API

A WebSocket-based **Real-Time Chat API** built with **FastAPI** and **Redis**, supporting **JWT authentication**, **chat rooms**, and **MongoDB message storage**.

## 📌 Features
- 🔗 **Real-Time Messaging** using **WebSockets**
- 🔑 **User Authentication** with **JWT**
- 📢 **Chat Rooms** for group messaging
- 💾 **Message History Storage** in **MongoDB**
- 📡 **Redis Pub/Sub** for message broadcasting
- 🐳 **Docker-Ready** for easy deployment

---

## 🏗️ Project Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/real-time-chat-api.git
cd real-time-chat-api
```

### 2️⃣ Create a Virtual Environment & Activate It
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
uvicorn app.main:app --reload
```
✅ **API will be available at:** `http://127.0.0.1:8000/docs`

---

## ⚙️ WebSocket Usage

### Connect to a Chat Room
```
ws://localhost:8000/ws/{room}?token=your_jwt_token
```
- Replace `{room}` with the chat room name.
- Replace `your_jwt_token` with a valid token.

### Send Messages
- Once connected, send messages as plain text.
- Messages will be **broadcasted** to all users in the room.

---

## 🔑 Authentication (JWT)
### Obtain a JWT Token
Make a **POST** request to:
```
POST http://localhost:8000/token
```
#### Request Body:
```json
{
  "username": "alice",
  "password": "your_password"
}
```
#### Response:
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```
Use this token for **WebSocket connections & API requests**.

---

## 📜 Message History
### Fetch Previous Messages
Make a **GET** request to:
```
GET http://localhost:8000/messages/{room}
```
#### Response Example:
```json
[
  {
    "room": "general",
    "sender": "alice",
    "content": "Hello, World!",
    "timestamp": "2024-02-05T12:34:56"
  }
]
```
---

## 🗃️ Database Setup (MongoDB)
1. **Install MongoDB** (if not installed):
   ```bash
   sudo apt update && sudo apt install -y mongodb
   ```
2. **Run MongoDB**:
   ```bash
   mongod --dbpath /data/db
   ```
3. **Check Connection**:
   ```bash
   mongosh
   use chat_db
   db.messages.find().pretty()
   ```

---

## 🐳 Docker Setup
### 1️⃣ Build the Docker Image
```bash
docker build -t fastapi-chat .
```
### 2️⃣ Run the Container
```bash
docker run -p 8000:8000 fastapi-chat
```
✅ Your app is now running inside a **Docker container**!

---

## 📌 Next Steps
🔹 **Step 8:** Deploy to **AWS/GCP/DigitalOcean** with **managed Redis** (Coming Soon!)

---

## 🛠️ Technologies Used
- **FastAPI** 🚀 (Backend Framework)
- **WebSockets** 📡 (Real-Time Communication)
- **MongoDB** 🗃️ (Database for Chat History)
- **Redis** ⚡ (Message Broadcasting)
- **JWT Authentication** 🔑 (User Security)
- **Docker** 🐳 (Containerization)

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Contributing
Feel free to **fork this repo** and contribute! 🚀

📩 Have suggestions? Open an **issue** or a **pull request**.

---

## ⭐ Star This Repo!
If you found this useful, don’t forget to ⭐ **star** this repository!