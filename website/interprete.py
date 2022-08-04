from datetime import datetime, timedelta
from . import db, LoginManager
from .models import User, Cardio, Exercise, FitnessGoal, other
from flask import flash
from flask_login import current_user
from sqlalchemy import update
from .stats import ex_muscle_groups



def updateLog(initialString):
    fOpen = open('website/md/log.md', 'r+')
    content = fOpen.read()
    fOpen.seek(0)
    fOpen.write(initialString + ' ' + datetime.today().strftime('%Y-%m-%d') + '\n' + content)
    fOpen.close()
'''--------------------------------------------------------------------------'''
''' questo metodo interpreta la stringa in entrata e fa capire quale operazione da fare nel db'''
def interString(String):
    if len(String) < 5 : 
        return None

    String = String.lower()
    if String.startswith('db add'):
        return 'dbAdd'
    if String.startswith('add') and String.endswith('to lib'):
        return 'addLib'    
    elif String.startswith('add'): 
        if String.startswith('add zone'):
            return 'Cardio'
        if String.startswith('add focus'):
            return 'Focus'
        else:
            return 'Resistance'
    elif String.startswith('set'):
        if String.startswith('set bw'):
            return 'setBw'
        elif String.startswith('set goal'):
            return 'setGoal'
    elif String.startswith('muscle group'):
        return 'addMuscle'
    elif String.lower().rstrip().split()[1] == "work":
        return 'setRel'


def addFocus(String, userId):
    initialString = String
    #add focus 30min
    String = String.rstrip().lower().split()
    String.pop(0)
    String.pop(0)
    duration = String[0][:-3]
    print(f"duration is {duration}")

    focus = other(name = 'focus', duration = duration, user_id = userId)
    db.session.add(focus)
    db.session.commit()
    flash(f"added {duration} min of focus", category='success')
    updateLog(initialString)


def addResistance(String, userId):
    initialString = String
    String = String.rstrip()

    String = String.lower()
    String = String.split()
    String.pop(0)

    print(String)

    exName = String[0]
    print(exName)
    if exName not in ex_muscle_groups:
        flash(f"exercise not in db", category='error')
        return 0

    if String[1] == "bw":
        exWeight = 0
    else:
        exWeight = String[1][:-2]
        print(exWeight)

    print(f"string[2] is {String[2]}")



    if String[2].startswith('x'): #compact add
        sets = String[2][1:].split("x") # list of the sets. each item has the reps
        print(sets)
        for set in sets: 
            new_ex = Exercise(name = exName, reps = set, weight = exWeight, user_id = userId, date = datetime.now())
            db.session.add(new_ex)
            db.session.commit()
            flash(f"added {exName}, {exWeight}kg, {set} reps", category='success')
        updateLog(initialString)

    elif String[2][0].isdigit():
        sets = String[2].split('x')[0]
        print("Sets is", sets)
        reps = String[2].split('x')[1]
        for set in range(int(sets)):
            new_ex = Exercise(name = exName, reps = reps, weight = exWeight, user_id = userId, date = datetime.now())
            db.session.add(new_ex)
            db.session.commit()
            flash(f"added {exName} {exWeight}kg x{sets}x{reps}", category='success')
        updateLog(initialString)
    


def setGoal(String, userId):
    initialString = String
    split = String.rstrip().split()
    split.pop(0)
    split.pop(0)
    exName = split[0].lower()
    split.pop(0)
    if split[0] == 'bw':
        exName = exName + ' bw'
        weight = 0
    else:
        weight = split[0][:-2]
    split.pop(0)
    reps = split[0][1:]

    print(f"{exName}, {weight}, {reps}")
    print(f"searching goal {exName}")
    '''se trova una corrispondenza deve aggiornare, sennò creare'''
    ex = FitnessGoal.query.filter_by(name=exName, user_id = userId).first()

    if ex:
        print('goal found!')
        

        ex.weight = weight
        ex.reps = reps     
        
        db.session.commit()
        
        updateLog(initialString)
        flash(f"Updated goal: {exName} x {weight}kg x {reps}", category='success')
        

    if not ex:
        newFitnessGoal = FitnessGoal(name = exName, weight = weight, reps = reps, user_id = userId)
        db.session.add(newFitnessGoal)
        db.session.commit()

        updateLog(initialString)
        flash(f"Added goal: {exName} x {weight}kg x {reps}", category='success')







def addCardio(String, userId):
    initialString = String
    String = String.rstrip()
    String = String.lower()
    String = String.split()
    String.pop(0)
    print(String)
    #zone 2 30min cyclette 
    zone = String[1]
    duration = String[2][:-3]
    medium = String[3]
    new_cardio = Cardio(zone = zone, duration = duration, medium = medium, user_id = userId, date = datetime.now())
    db.session.add(new_cardio)
    db.session.commit()
    flash(f"added cardio zone {zone}, {duration}min, {medium}", category='success')
    updateLog(initialString)
'''
def addLib(String):
    print('attempting to add to lib')
    initialString = String
    String = String.rstrip().lower()
    name = String.split()[1]

    se trova una corrispondenza deve aggiornare, sennò creare
    ex = ExerciseLib.query.filter_by(name=name).first()

    if ex:
        print('ex already found in lib!')
        flash(f"Exercise already in the library", category='error')
    else:
        exercise = ExerciseLib(name = name)
        db.session.add(exercise)
        db.session.commit()
        
        flash(f"added an exercise to the library: {name} ", category='success')
        updateLog(initialString)'''

    

'''def addMuscle(String):
    print('attempting to add a muscle')
    initialString = String

    String = String.rstrip().lower().split() # muscle group chest
    String.pop(0)
    String.pop(0)
    muscle = String[0]
    print(muscle)
    se trova una corrispondenza deve aggiornare, sennò creare
    ex = MuscleGroups.query.filter_by(name=muscle).first()

    if ex:
        print('muscle already found in lib!')
        flash(f"Muscle already in the library", category='error')
    else:
        muscleGroup = MuscleGroups(name = muscle)
        db.session.add(muscleGroup)
        db.session.commit()
        
        flash(f"added a muscle to muscle group: {muscle} ", category='success')
        updateLog(initialString)


def setRel(String):
    print('attempting to add a muscle')
    initialString = String
    String = String.rstrip().lower().split()
    exercise = String[0]
    print(exercise)
    String.pop(0)
    String.pop(0)
    
    musclesWorkedTemp = String
    musclesWorked = []
    for muscle in musclesWorkedTemp:
        if muscle.endswith(','):
            muscle = muscle[:-1]
        musclesWorked.append(muscle)
            
    print(musclesWorked)
        
    list_of_muscle_groups = []
    #cheking if the muscle do exist
    for muscle in musclesWorked:
        muscleFound = MuscleGroups.query.filter_by(name=muscle).first()
        if not muscleFound:
            print(f'{muscle} not found!')
            flash(f'{muscle} not found!', category = 'error')
            return -1
        else:
            list_of_muscle_groups.append(muscleFound)
            print(f'{muscle} found! proceding')

    

    #exercise search
    ex = ExerciseLib.query.filter_by(name=exercise).first()
    if not ex:
        print('Exercise not found!')
        flash('Exercise not found!', category = 'error')
        return -1
    else:
        #ora devo aprire la lista di esercizi associati nell'esercizio. 
        #ed aggiungerci le stringhe
        for muscle in list_of_muscle_groups:
            print('appending to the exercise_musclegroupList')
            ex.MuscleGroups_used.append(ExerciseLib_name = ex.name, MuscleGroups_name = muscle.name)
            db.session.commit()
            flash(f'added {muscle.name} to {ex.name}', category = 'success')

    updateLog(initialString)'''


