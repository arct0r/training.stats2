from website import create_app
from website.stats import allExercisesTimeFrame
from flask_login import LoginManager, current_user


app = create_app()

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=5000, debug=True, threaded=True))

 