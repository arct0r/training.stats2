from datetime import datetime, timedelta, date
from . import db, LoginManager
from .models import User, Cardio, Exercise, FitnessGoal, other
from flask import flash
from flask_login import current_user
from sqlalchemy import update

ex_muscle_groups = {
    'dips': ['chest', 'triceps', 'shoulders'],
    'ohp_kb' : ['shoulders', 'triceps'],
    'pullups' : ['back', 'biceps'],
    'chinups' : ['back', 'biceps'],
    'squat' : ['legs'],
    'deadlift' : ['legs', 'back'],
    'bent_over_rows' : ['back', 'biceps'],
    'triceps_extensions' : ['triceps'],
    'bicep_curl' : ['biceps'],
    'leg_curl' : ['legs'],
    'split_squats' : ['legs'],
    't_bar_rows' : ['back', 'biceps'],
    'leg_press' : ['legs'],
    'db_bench_press' : ['chest', 'triceps', 'shoulders'],
    '1arm_crossover' : ['chest'],
    'pullups_bw' : ['back', 'biceps']

}

MuscleGroups = {
    'chest' : 0,
    'shoulders' : 0,
    'triceps' : 0 ,
    'back' : 0 ,
    'biceps' : 0 ,
    'legs' : 0,
}

def pastDate(days):
    past_date = datetime.now() - timedelta(days=days)
    return past_date

def allExercisesTimeFrame(days, userId):
    #returns all the exercises done in the given timeframe for a given user

    pastdate = pastDate(days)
    currentDate = date.today()

    exList = Exercise.query.filter(
            Exercise.date > pastdate
        ).filter(
            Exercise.user_id == userId
        ).all()




    return exList


def weekly_ex_per_group():
    userId = current_user.id

    past_date = pastDate(7)
    exList = allExercisesTimeFrame(7, userId)

    for ex in exList:
        name = ex.name
        if ex_muscle_groups[name]:
            for muscle in ex_muscle_groups[name]:
                MuscleGroups[muscle] += 1

    muscle_Groups = {}
    
    for muscle in MuscleGroups: muscle_Groups[muscle] = MuscleGroups[muscle]
    for muscle in MuscleGroups: MuscleGroups[muscle] = 0

    return muscle_Groups


def strengthStats():
    #{'Dips' : [currentmax, goal, 30days imp, 90days imp, 180days imp]}
    # strengthStats = {
    #  'dips' : {'goal': y, '30days': y}
    # }
    userId = current_user.id
    
    strengthStats = {}

    goalList = FitnessGoal.query.filter_by(
        user_id = userId
    ).all()

    for goal in goalList:
        strengthStats[goal.name] = {
            'currentMax' : max_timeframe(180, goal.name),
            'goalMax' : [goal.weight, goal.reps],
            'days_30' : improvement(30, goal.name),
            'days_90' : improvement(90, goal.name),
            'days_180' : improvement(180, goal.name)

        }
    


    return strengthStats

def max_timeframe(days, exName, prior = False):
    userId = current_user.id
    past_date = pastDate(days)

    if prior == False:
        exercises = Exercise.query.filter(
            Exercise.name == exName
        ).filter(
            Exercise.date > past_date
        ).all()
    elif prior == True:
        exercises = Exercise.query.filter(
            Exercise.name == exName
        ).filter(
            Exercise.date < past_date
        ).all()
    
    bestEx = None
    for ex in exercises:
        if bestEx == None:
            bestEx = ex
        elif ex.oneRep() > bestEx.oneRep():
            bestEx = ex
            
    if bestEx == None:
        return [0, 0]
    
    return [bestEx.weight, bestEx.reps]

def oneRepMax(weight, reps):
        oneRepMax =  weight / ( 1.0278 - 0.0278 * reps )

        return int(oneRepMax)

def improvement(days, exName):
    maxPrior = max_timeframe(days+1, exName, True)
    maxPost = max_timeframe(days, exName)

    if 0 in [maxPrior[0], maxPrior[1], maxPost[0], maxPost[1]]:
        return 0
    
    increase = oneRepMax(maxPost[0], maxPost[1]) - oneRepMax(maxPrior[0], maxPrior[1])
    improvement = (increase / oneRepMax(maxPrior[0], maxPrior[1]))*100


    return int(improvement)


