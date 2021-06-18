from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from .twitter_data_model import User
import pandas as pd


def get_most_likely_handle(usernames, tweet_to_classify, nlp):
    vects = []
    for username in usernames:
        user = User.query.filter(User.name == username).one()
        user_vects = pd.DataFrame([tweet.vect for tweet in user.tweets])
        user_vects['name'] = username
        vects.append(user_vects)
    df = pd.concat(vects)
    le = LabelEncoder()
    y_train = le.fit_transform(df['name'])
    X_train = df[[c for c in df.columns if not c == 'name']]
    X_pred = [nlp(tweet_to_classify).vector]
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_pred)[0]

    return usernames[y_pred - 1]