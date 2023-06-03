### About Myself

Name :- Satvik Chandrakar
Roll No :- 21f1000344
Subject :- MAD-I Project

### About Project 

Book Tickets is a multi user app used for booking show tickets. Users can book many tickets for many movies. 

Technologies used :
  - Application code : Flask 
  - Database : Sqlite3 
  - Style :- Jinja2, Bootstrap

Functionalities : 
   1. Admin and User Login 
       * Form for username and password for user
       * Separate form for admin login
       * Using simple html form with username and password for login 
       * There is a model for user in database to store its data 
    2. Venue Management (Only for Admin)
       * Admin can add new venue
       * It can edit details of a venue 
       * It can also remove venue with a confirmation 
    3. Show Management (Only for Admin)
       * Admin can add a new show
       * It can edit details of a show
       * It can also remove a show
       * Admin has to allocate venues while adding show and each venue can host multiple shows
    4. Booking for show tickets 
       * User can see the latest available shows
       * User can book multiple tickets for a show at a given venue
       * App will stop taking bookings in case of a houseful 
    5. Search for shows/venues
       * App has a ability to search venues based on location preference
       * It can also search movies based on movie name and tags 
       * Search result shows the latest added shows
       * There is a basic home view for a venue 

### How To Run 

Open a terminal in the project root directory and run the following commands

1. Install virtualenv:
```
$ pip install virtualenv
```

2. Create virtual environment:
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
