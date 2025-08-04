# 🏫 Classroom Timetable & Availability App

Hello!! This is Group 3 from the ISI Kyoso Programming Course!

This is a Streamlit app made by our group for managing and viewing classroom schedules, searching for classes/teachers, checking available rooms, and integrating with Google Calendar.

---

## 📌 Features

### 1. **FAQ Page**
- Searchable FAQ list with expandable answers.
- Contact form for inquiries (Name, Email, Message).

### 2. **Recommended Available Classrooms**
- Select a **day** and **period** to view all available rooms.
- Quick filtering between 3rd and 4th floor classrooms.
- Displays total number of available classrooms and a table list.

### 3. **Calendar**
- OAuth-based login with Google to access your calendars.
- Select a date to view all events across your calendars.
- Embedded calendar view for a chosen calendar.
- Supports login/logout.

### 4. **Classroom Timetable**
- View timetable for each classroom (3F & 4F rooms supported).
- Color-coded schedule:
  - **Green** = Available period
  - **Gray** = Occupied period
- Select any classroom from a dropdown to view its weekly schedule.

### 5. **Class Search**
- Search by **class name** or **teacher name** (supports Hiragana/Katakana conversion for flexible matching).
- Displays:
  - Matching classes
  - Teacher names
  - Room assignments
  - Day and period information

### 6. **Floor Maps**
- Select a **floor**, **date**, **period** and **classroom** to view its availability.
- Quick filtering between 3rd and 4th floor classrooms with map of Center 5 building.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **Pandas** — CSV data processing
- **Google Calendar API** — Calendar integration
- **jaconv** — Japanese text conversion
- **HTML/CSS** — Styling via `unsafe_allow_html=True`

