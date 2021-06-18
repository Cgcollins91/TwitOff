from flask import Flask, request, render_template
from .twitter_data_model import User, DB
import spacy
from .predict import get_most_likely_handle
from .twitter_database_functions import insert_user_or_update
import os.path


# pdb.set_trace()
#
# key = os.getenv('TWITTER_API_KEY')
# secret = os.getenv('TWITTER_API_KEY_SECRET')


def create_app():
    app = Flask(__name__)
    # app.debug = True
    # DATABASE_URI = os.getenv('DATABASE_URI')
    # conn = psycopg2.connect(DATABASE_URI, sslmode='require')
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///twitter_db.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    # pdb.set_trace()

    nlp_path = os.path.join('/'.join(os.path.abspath(__file__).split('/')[:-1]), 'my_model')
    nlp = spacy.load(nlp_path)

# Create Landing Page and SQL DB
    @app.route('/')
    def root():
        sql_path = "twitoff/twitter_db.sqlite3"
        if not os.path.isfile(sql_path):
            DB.create_all()

        return render_template('base.html', title="Home", users=User.query.all())

    # Take Twitter handle input in form and add to DB and update form
    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(handle=None, message=''):
        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        handle = handle or request.values['twitter_handle']
        try:
            if request.method == 'POST':
                insert_user_or_update(handle, 'insert')
                message = "User {} Succesfully added!".format(handle)

            tweets = User.query.filter(User.name == handle).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(handle, e)

            tweets = []
        print('{}\'s tweets added to the database: {}'.format(handle, ', '.join([t.text for t in tweets])))
        return render_template("user.html", title=handle, tweets=tweets, message=message, users=User.query.all())

    # Refresh tweet DB for users shown in current form
    @app.route('/update')
    def update():
        current_users = DB.session.query(User.name)
        current_name = current_users[0]
        try:
            tweets = []
            for name in current_users:
                insert_user_or_update(name, 'update')
                tweets += User.query.filter(User.name == name).one().tweets
                current_name = name
            message = "Successfully Updated All Users"
        except Exception as e:
            message = "Error updating {}: {}".format(current_name, e)
        return render_template("base.html", title="Updated Users", tweets=tweets, message=message, users=User.query.all())

    # Predict which user would be more likely to tweet given input
    @app.route('/compare', methods=["POST"])
    def predict():
        tweet_to_classify = request.values['tweet_text']
        handles = [user.name for user in User.query.all()]
        most_likely_handle = get_most_likely_handle(handles, tweet_to_classify, nlp)
        message = "'{}' is more likely to have said {}".format(most_likely_handle, tweet_to_classify)
        return render_template("prediction.html", title="Prediction", message=message)

    # Handle 404 Error
    @app.errorhandler(404)
    def error_handler(e):
        return 'this is not here: {}'.format(e), 404

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset Database")
    return app

# return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run()
