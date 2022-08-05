from calendar import weekday
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 
from datetime import datetime, timedelta, date
from flask_login import current_user

def pastDate(days):
    past_date = datetime.now() - timedelta(days=days)
    return past_date
    
def toWeekDay(num):
    days = { 
        0 : 'monday',
        1 : 'tuesday',
        2 : 'wednesday',
        3 : 'thursday',
        4 : 'friday',
        5 : 'saturday',
        6 : 'sunday'

    }
    return days[num]
    

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    '''----------------------------------- Associamo Exercise a User tramite la FOREIGN KEY'''
    '''---------------------------- La FK fa riferimento ad una colonna di un altra tabella'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user minuscolo nonostante sia User
    '''--------------------------- in questo caso si tratta di una ONE to MANY relationship'''
    '''---------------------------------------------- User è il parent, Exercise è il child'''

    def oneRep(self):
        max =  self.weight / ( 1.0278 - 0.0278 * self.reps )

        return int(max)

    def weekWorkouts():
        #prima di tutto devo capire che giorno della settimana è questo
        day = datetime.today().weekday() 
        past_date = pastDate(day).date()
        print(past_date)

        #ora trovo tutti gli esercizi fatti durante la settimana
        exs = Exercise.query.filter(
            Exercise.user_id == current_user.id
        ).filter(
            Exercise.date > past_date
            ).all()
        
        print(exs)
        #ora li ordino in base alla giornata. Non la giornata della settimana. 

        ex_by_day = {}
        

        for ex in exs: 
            weekday = toWeekDay(ex.date.weekday())
            ex_by_day[weekday] = []

        for ex in exs: 
            weekday = toWeekDay(ex.date.weekday())
            ex_by_day[weekday].append(ex)

        print (ex_by_day)


        return ex_by_day

class Cardio(db.Model):
    __tablename__ = 'cardio'

    id = db.Column(db.Integer(), primary_key=True)
    zone = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    medium = db.Column(db.String(30))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    '''----------------------------------- Associamo Exercise a User tramite la FOREIGN KEY'''
    '''---------------------------- La FK fa riferimento ad una colonna di un altra tabella'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user minuscolo nonostante sia User
    '''--------------------------- in questo caso si tratta di una ONE to MANY relationship'''
    '''---------------------------------------------- User è il parent, Exercise è il child'''
    def weeklyCardio():
        weeklyCardio = 0
        past_date = pastDate(7)

        cardioSessions = Cardio.query.filter(
            Cardio.date > past_date
        ).filter(
            Cardio.user_id == current_user.id
        )
        for session in cardioSessions:
            weeklyCardio += session.duration
        
        return weeklyCardio


class FitnessGoal(db.Model):
    __tablename__ = 'fitnessgoal'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    reps = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user minuscolo nonostante sia User


class other(db.Model):
    __tablename__ = 'other'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user minuscolo nonostante sia User

    def dailyFocus():
        userId = current_user.id
        dailyFocus = 0

        focusSessions = other.query.filter(
            other.name == 'focus'
        ).filter(
            other.user_id == userId
        ).filter(
            other.date > date.today()
        ).all()


        for session in focusSessions:
            dailyFocus += session.duration
        # Get hours with floor division
        hours = dailyFocus // 60

        # Get additional minutes with modulus
        minutes = dailyFocus % 60

        
        return [hours, minutes]


    def focusYesterday():
        userId = current_user.id
        dailyFocus = 0

        focusSessions = other.query.filter(
            other.name == 'focus'
        ).filter(
            other.user_id == userId
        ).filter(
            other.date == pastDate(1)
        ).all()


        for session in focusSessions:
            dailyFocus += session.duration
        # Get hours with floor division
        hours = dailyFocus // 60

        # Get additional minutes with modulus
        minutes = dailyFocus % 60

        
        return [hours, minutes]

    def focusWeekly():
        userId = current_user.id
        days = 7
        totalFocus = 0

        focusSessions = other.query.filter(
            other.name == 'focus'
        ).filter(
            other.user_id == userId
        ).filter(
            other.date > pastDate(7)
        ).all()


        for session in focusSessions:
            totalFocus += session.duration
        # Get hours with floor division
        hours = totalFocus // 60

        # Get additional minutes with modulus
        minutes = totalFocus % 60

        
        return [hours, minutes]
'''exerciselib_muscleGroups = db.Table('exerciselib_muscleGroups', 
    db.Column('ExerciseLib_name', db.String(20), db.ForeignKey('exerciselib.name')),
    db.Column('MuscleGroups_name', db.String(20), db.ForeignKey('musclegroups.name'))
)


class ExerciseLib(db.Model):
    __tablename__ = 'exerciselib'

    name = db.Column(db.String(20), primary_key=True)
    MuscleGroups_used = db.relationship('MuscleGroups', secondary = exerciselib_muscleGroups, backref = 'MuscleGroups')


class MuscleGroups(db.Model):
    __tablename__ = 'musclegroups'
    
    name = db.Column(db.String(20), primary_key = True)
    exercise_id = db.Column(db.Integer) #user minuscolo nonostante sia User'''






'''----------------------------------------- UserMixin serve per le sessions di FlaskLogin '''
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    weight = db.Column(db.Integer)
    exercise = db.relationship('Exercise')
    cardio = db.relationship('Cardio')
    fitnessGoal = db.relationship('FitnessGoal')
    other = db.relationship('other')



'''------------------------------------------------- Qui il riferimento al child, Exercise '''

