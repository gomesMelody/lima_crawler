from flask import Flask, json
import pandas as pd
df_articles = pd.read_csv("./humans.csv")
df_articles = df_articles['categories'].apply(tuple)
api = Flask(__name__)

@api.route('/articles', methods=['GET'])
def get_all_articles():

    message = "<h3>List of Articles Available:<br></h4>"
    for index, row in df_articles.iterrows():
        message += f"<br>{row['categories']}<br><a href='{row['link']}'>{row['headline']}</a><br>"

    return json.dumps(message)

@api.route('/articles/<label>', methods=['GET'])
def get_articles_by_label(label):

    message = f"<h3>List of Articles Available for <b>{label}</b>:<br></h4>"
    filtered_df = df_articles.loc[df_articles['categories'] == (label,)]
    for index, row in filtered_df.iterrows():
        message += f"<br>{row['categories']}<br><a href='{row['link']}'>{row['headline']}</a><br>"

    return json.dumps(message)

if __name__ == '__main__':
    api.run()