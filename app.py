# Importing the required packages.  
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

# Initializing the app
app = Flask(__name__)
# SQLite database configuration relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booktickets.db'
# Database extension
db = SQLAlchemy()
# Initalizing the app with the extension
db.init_app(app)
# Creating context for our flask application. An active Flask application context is required to make queries and to access db.engine and db.session.
app.app_context().push()

#Models
class User(db.Model):
    __tablename__ = 'user'
    userId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(10))
    bookedshows = db.relationship("BookedShows",backref='user', lazy='dynamic', primaryjoin="User.userId == BookedShows.userId")

class Venue(db.Model):
    __tablename__ = 'venue'
    venueId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    screencount = db.Column(db.Integer)
    allocated = db.Column(db.String)

class Show(db.Model):
    __tablename__ = 'show'
    showId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Integer) #Static pricing
    tags = db.Column(db.String)
    sdate = db.Column(db.String)
    edate = db.Column(db.String)
    allocatedvenues = db.relationship("Allocatedvenues",backref='show',cascade="all, delete", lazy='dynamic',primaryjoin="Show.showId == Allocatedvenues.showId")

class Allocatedvenues(db.Model):
    __tablename__ = 'allocatedvenues'
    theaterId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    showId = db.Column(db.Integer, db.ForeignKey('show.showId'), nullable=False)
    venueId = db.Column(db.Integer, db.ForeignKey('venue.venueId'), nullable=False)
    screen_no = db.Column(db.Integer)
    seatbooking = db.relationship("Seatbooking",backref='allocatedvenues',cascade='all, delete', lazy='dynamic',primaryjoin='Allocatedvenues.theaterId == Seatbooking.theaterId')

class Seatbooking(db.Model):
    __tablename__ = 'seatbooking'
    seatId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    theaterId = db.Column(db.Integer, db.ForeignKey('allocatedvenues.theaterId'))
    date = db.Column(db.String)
    no_of_seats_booked = db.Column(db.Integer)

class BookedShows(db.Model):
    __tablename__ = 'bookedshows'
    bookingId = db.Column(db.Integer, autoincrement=True, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.userId'))
    show_name = db.Column(db.String)
    venue = db.Column(db.String)
    date = db.Column(db.String)
    no_of_seats_booked = db.Column(db.Integer)
    screen_no = db.Column(db.Integer)
    timing = db.Column(db.String)


#Controllers
app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpassword = request.form['password']
        userBytes = userpassword.encode('utf-8')
        try:
            user = db.one_or_404(db.select(User).filter_by(username=username))
            actual_password = user.password
            result = bcrypt.checkpw(userBytes, actual_password) # Validating the password
            if result == True:
                return redirect(url_for('userprofile',username=username))
            else: 
                return redirect(url_for('error', message='Wrong Password'))
        except:
            return redirect('/register')
    else:
        return render_template("login.html")

@app.route('/error/<message>', methods=['GET'])
def error(message):
    return render_template("error.html",message=message)
   
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else: 
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        bytes = password.encode('utf-8') # converting password to array of bytes
        salt = bcrypt.gensalt() # generating the salt
        hashed_password = bcrypt.hashpw(bytes,salt) # Hashing the password
        new_user = User(username=username,password=hashed_password, first_name=first_name,last_name=last_name,phone_number=phone_number)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return redirect(url_for('error', message='Your account could not be created. Error occured'))

@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'GET':
        return render_template("admin.html")
    else:
        password = request.form['password']
        if password == "123":
            return redirect('/sysopt')
        else:
            return redirect(url_for('error', message='Wrong Password'))

@app.route('/sysopt', methods=['GET'])
def sysopt():
    return render_template('sysopt.html')

@app.route('/venuemanagement', methods=['GET'])
def venuemanagement():
    venue_list = Venue.query.all()
    return render_template("venuemanagement.html", venue_list=venue_list)

@app.route('/addvenue', methods=['POST'])
def addvenue():
    name = request.form['name']
    city = request.form['city']
    capacity = request.form['capacity']
    screencount = request.form['screencount']
    new_venue = Venue(name=name,city=city,capacity=capacity,screencount=screencount)
    try:
        db.session.add(new_venue)
        db.session.commit()
        return redirect('/venuemanagement')
    except:
        return redirect(url_for('error', message='Venue could not be added. Error occured'))

@app.route('/editvenue/<int:venueId>', methods=['POST'])
def editvenue(venueId):
    try: 
        venue = db.one_or_404(db.select(Venue).filter_by(venueId=venueId))
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.capacity = request.form['capacity']
        venue.screencount = request.form['screencount']
        db.session.commit()
        return redirect('/venuemanagement')
    except:
        return redirect(url_for('error', message='Edit Failed'))

@app.route('/removevenue/<int:venueId>', methods=['POST','GET'])
def removevenue(venueId):
    venue = db.one_or_404(db.select(Venue).filter_by(venueId=venueId))
    if request.method == 'GET':
        return render_template('removevenue.html', venue=venue)
    else: 
        try:
            db.session.delete(venue)
            db.session.commit()
            return redirect('/venuemanagement')
        except:
            return redirect(url_for('error', message='Venue could not be removed. Error occured'))

@app.route('/showmanagement', methods=['GET'])
def showmanagement():
    show_list = db.session.scalars(db.select(Show).order_by(Show.showId.desc())).all()
    return render_template("showmanagement.html", show_list=show_list)

@app.route('/addshow', methods=['POST'])
def addshow():
    name = request.form['name']
    price = request.form['price']
    tags = request.form['tags']
    sdate = request.form['sdate']
    edate = request.form['edate']
    new_show = Show(name=name,price=price,tags=tags,sdate=sdate,edate=edate)
    try:
        db.session.add(new_show)
        db.session.commit()
        venue_list = Venue.query.all()
        for venue in venue_list:
            venue.allocated = 'False'
        db.session.commit()
        return redirect(url_for('allocatevenue',show_name=name))
    except:
        return redirect(url_for('error', message='Show could not be added. Error occured'))

@app.route('/allocatevenue/<show_name>', methods=['POST','GET'])
def allocatevenue(show_name):
    if request.method == 'GET':
        venue_list = Venue.query.all()
        return render_template('allocatevenue.html', venue_list=venue_list, show_name=show_name)

@app.route('/venueallocation/<int:venueId>/<show_name>', methods=['POST'])
def venueallocation(venueId,show_name):
    screen_no = request.form['screen_no']
    show = db.one_or_404(db.select(Show).filter_by(name=show_name))
    allocatedvenue = Allocatedvenues(showId=show.showId,venueId=venueId,screen_no=screen_no)
    try:
        db.session.add(allocatedvenue)
        db.session.commit()
        venue = db.one_or_404(db.select(Venue).filter_by(venueId=venueId))
        venue.allocated = 'True'
        db.session.commit()
        return redirect(url_for('allocatevenue',show_name=show_name))
    except:
        return redirect(url_for('error', message='Venue could not be allocated. Error occured'))

@app.route('/editshow/<int:showId>', methods=['POST'])
def editshow(showId):
    try:
        show = db.one_or_404(db.select(Show).filter_by(showId=showId))
        show.name = request.form['name']
        show.price = request.form['price']
        show.tags = request.form['tags']
        show.sdate = request.form['sdate']
        show.edate = request.form['edate']
        db.session.commit()
        return redirect('/showmanagement')
    except:
        return redirect(url_for('error', message='Edit Failed'))

@app.route('/removeshow/<int:showId>', methods=['POST','GET'])
def removeshow(showId):
    show = db.one_or_404(db.select(Show).filter_by(showId=showId))
    if request.method == 'GET':
        return render_template('removeshow.html', show=show)
    else: 
        try:
            db.session.delete(show)
            db.session.commit()
            return redirect('/showmanagement')
        except:
            return redirect(url_for('error', message='Show could not be removed. Error occured'))

@app.route('/userprofile/<username>', methods=['GET'])
def userprofile(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    show_list = db.session.scalars(db.select(Show).order_by(Show.showId.desc())).all()
    bookedshows = db.session.scalars(db.select(BookedShows).filter(BookedShows.userId==user.userId))
    return render_template('userprofile.html',user=user,show_list=show_list,username=username,bookedshows=bookedshows)

@app.route('/booktickets/<username>/<int:showId>', methods=['GET'])
def booktickets(username,showId):
    show = db.one_or_404(db.select(Show).filter_by(showId=showId))
    venue_list = Venue.query.join(Allocatedvenues, Venue.venueId==Allocatedvenues.venueId).filter(Allocatedvenues.showId == showId).all() # List of venues allocated for show with given showId.
    return render_template('booktickets.html',show=show,venue_list=venue_list,username=username)

@app.route('/confirmbooking/<username>/<int:showId>', methods=['POST'])
def confirmbookings(username,showId):
    venueId = request.form['venue']
    no_seats = request.form['seat_count']
    booking_date = request.form['booking_date']
    timing = request.form['timing']
    show = db.one_or_404(db.select(Show).filter_by(showId=showId))
    venue = db.one_or_404(db.select(Venue).join(Allocatedvenues, Venue.venueId==Allocatedvenues.venueId).filter(Allocatedvenues.showId == showId, Venue.venueId == venueId))
    user = db.one_or_404(db.select(User).filter_by(username=username))
    allocatevenue = db.one_or_404(db.select(Allocatedvenues).filter_by(showId=showId,venueId=venueId))
    if int(no_seats) <= int(venue.capacity):
        try:
            seats = db.one_or_404(db.select(Seatbooking).filter(Seatbooking.theaterId == allocatevenue.theaterId, Seatbooking.date == booking_date))
            seats_remaining = int(venue.capacity) - int(seats.no_of_seats_booked)
            if seats_remaining > 0:
                if seats_remaining >= int(no_seats):
                    seats.no_of_seats_booked += int(no_seats)
                    db.session.commit()
                    amount = int(no_seats)*int(show.price)
                    db.session.add(BookedShows(userId=user.userId,show_name=show.name,venue=venue.name+','+venue.city,date=booking_date,no_of_seats_booked=no_seats,screen_no=allocatevenue.screen_no,timing=timing))
                    db.session.commit()
                    return render_template('bookingconfirmed.html', show=show,venue=venue,amount=amount,allocatevenue=allocatevenue,no_seats=no_seats,booking_date=booking_date,username=username,timing=timing)
                else:
                    return redirect(url_for('error', message='Not enough seats are available. Only '+str(seats_remaining)+' '+'seats are remaining'))
            else:
                return redirect(url_for('error',message='Housefull'))
        except:
            db.session.add(Seatbooking(theaterId=allocatevenue.theaterId,date=booking_date,no_of_seats_booked=no_seats))
            db.session.commit()
            amt = int(no_seats)*int(show.price)
            db.session.add(BookedShows(userId=user.userId,show_name=show.name,venue=venue.name+','+venue.city,date=booking_date,no_of_seats_booked=no_seats,screen_no=allocatevenue.screen_no,timing=timing))
            db.session.commit()
            return render_template('bookingconfirmed.html', show=show,venue=venue,amount=amt,allocatevenue=allocatevenue,no_seats=no_seats,booking_date=booking_date, username=username,timing=timing)
    else:
        return redirect(url_for('error', message='You have entered more number of seats than total seat capacity'))

@app.route('/searchvenues/<username>', methods=['POST'])
def searchvenues(username):
    city = request.form['city']
    query = "%" + city + "%"
    venues = Venue.query.filter(Venue.city.like(query)).all()
    return render_template('searchresult.html',results=venues,field='Venues in '+city,homeview='venuehome',username=username)

@app.route('/venuehome/<username>/<int:venueId>',methods=['GET'])
def venuehome(username,venueId):
    venue = db.one_or_404(db.select(Venue).filter_by(venueId=venueId))
    show_list = Show.query.join(Allocatedvenues, Show.showId==Allocatedvenues.showId).filter(Allocatedvenues.venueId == venueId).order_by(Show.showId.desc()).all()
    return render_template('venuehome.html',venue=venue,show_list=show_list,username=username)

@app.route('/searchshows/<username>', methods=['POST'])
def searchshows(username):
    q = request.form['query']
    query = "%" + q + "%"
    results1 = Show.query.filter(Show.tags.like(query)).all()
    results2 = Show.query.filter(Show.name.like(query)).all()
    return render_template('showsearchresult.html',results1=results1,results2=results2,field='Search Result',query=q,username=username)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)

