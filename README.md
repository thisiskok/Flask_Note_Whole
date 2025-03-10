**Notes:**
The backend may enter a sleep state after extended inactivity, requiring time to restart and re-establish the database connection when a new request arrives. This can cause an initial request delay of **30 seconds to 2 minutes** and a database connection delay of **10-15 seconds** during reinitialization.

**Flask Web Note-Taking App**: 
A simple, user-friendly web application for taking and managing notes, built with Flask, Postgresql, and Bootstrap.
![image](https://github.com/user-attachments/assets/1caf5628-fd0e-4b3c-891e-2c6fb5df3b09)

Project: https://flask-note-whole.onrender.com

**🌟 Features**

📝 User Authentication: Secure sign-up, login, and logout functionality.

📄 Note Management: Create, edit, delete, and view notes.

🔒 Authorization: Users can only access their own notes.

🔍 Search Functionality: Quickly find notes by keywords.

📅 Timestamps: Notes include creation and last modified dates.

**🛠️ Tech Stack**

Backend: Flask (Python)

Frontend: HTML, CSS (Bootstrap)

Database: PostgreSQL

Authentication: Flask-Login, Flask-WTF
