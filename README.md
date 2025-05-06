# 🎟️ Book Tickets – Movie Ticket Booking App

**Developer:** Satvik Chandrakar  
**Roll No:** 21f1000344  
**Subject:** MAD-I Project

---

## 📖 About the Project

**Book Tickets** is a multi-user web application for booking show tickets. It allows users to browse movies, view venues, and book multiple tickets per show. Admins can manage venues and shows.

---

## 🚀 Technologies Used

- **Backend Framework:** Flask  
- **Database:** SQLite3  
- **Frontend:** Jinja2 Templating, Bootstrap

---

## 📌 Features

### 1. 👥 User and Admin Login
- Separate login forms for users and admins.
- Simple HTML forms for username and password.
- User credentials stored in a dedicated database model.

### 2. 🏢 Venue Management (Admin Only)
- Add, edit, or delete venues.
- Delete action includes confirmation prompt.

### 3. 🎬 Show Management (Admin Only)
- Add, edit, or delete shows.
- Assign venues while creating shows.
- One venue can host multiple shows.

### 4. 🎟️ Ticket Booking (User)
- View latest available shows.
- Book multiple tickets per show at selected venues.
- Bookings are disabled once a show is houseful.

### 5. 🔍 Search Functionality
- Search venues by location.
- Search movies by name or tags.
- Results show the most recently added shows.
- Basic homepage view for venues and shows.

---

## 🛠️ How to Run the Project

Follow these steps to run the project locally:

1. Install virtualenv:
```
$ pip install virtualenv
```

2. Create a virtual environment:
```
$ virtualenv env
```

3. Then run the command:
```
$ .\env\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python app.py
```
