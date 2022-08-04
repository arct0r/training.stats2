from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, flash
from .models import Cardio, other, Exercise
from website.stats import weekly_ex_per_group, strengthStats
from .interprete import addFocus, interString, addResistance, addCardio, setGoal
import markdown

views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def terminal():
    if request.method == "POST":
        command = request.form.get('command')
        print(command)
        if interString(command) == 'Resistance':
            print('adding resistance')
            addResistance(command, current_user.id)
        elif interString(command) == 'Cardio':
            print('adding Cardio')
            addCardio(command, current_user.id)
        elif interString(command) == 'setGoal':
            print('setting Goal')
            setGoal(command, current_user.id)
        elif interString(command) == 'Focus':
            print('adding focus')
            addFocus(command, current_user.id)
            '''elif interString(command) == 'addLib':
                print('adding to exercise lib')
                addLib(command)
            elif interString(command) == 'addMuscle':
                print('adding a muscle')
                addMuscle(command)
            elif interString(command) == 'setRel':
                print('setting a rel')
                setRel(command)'''
                
            #elif interString(command) == 'removeLast':
                #print('removed last entry')
        elif interString(command) == None:
            print('invalid input')
            flash('Invalid input.', category ='error')

    fOpen = open('website/md/eest.md', 'r')
    page = []
    for line in fOpen:
        page.append(markdown.markdown(line))
    
    return render_template('terminal.html', user = current_user, page = page, test = 'etchiù!')

@views.route('/stats')
@login_required
def stats():
    return render_template(
        'stats.html', user = current_user,
        muscleGroups = weekly_ex_per_group(),
        weeklyCardio = Cardio.weeklyCardio(),
        dailyFocus = other.dailyFocus(),
        yesterdayFocus = other.focusYesterday(),
        weeklyFocus = other.focusWeekly(),
        strengthStats = strengthStats(),
        weekWorkouts = Exercise.weekWorkouts()
        )

@views.route('/base4')
def base4():
    return render_template('base4.html')
    
