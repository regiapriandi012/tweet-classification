from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=['POST', 'GET'])
def result():
    import pymongo
    import pandas as pd
    import urllib

    CONNECTION_STRING = "mongodb+srv://regiapriandi012:" + urllib.parse.quote(
        "@Sinheul24.") + "@cluster0.4ti9q.mongodb.net/database0?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.database0

    blibli = pd.DataFrame(list(db['blibli'].find()))
    tokopedia = pd.DataFrame(list(db['tokopedia'].find()))
    shopee = pd.DataFrame(list(db['shopee'].find()))
    lazada = pd.DataFrame(list(db['lazada'].find()))
    bukalapak = pd.DataFrame(list(db['bukalapak'].find()))

    bukalapak_tweet = bukalapak["tweet"].tolist()
    tokopedia_tweet = tokopedia["tweet"].tolist()
    lazada_tweet = lazada["tweet"].tolist()
    shopee_tweet = shopee["tweet"].tolist()
    blibli_tweet = blibli["tweet"].tolist()

    all_tweet = bukalapak_tweet + tokopedia_tweet + lazada_tweet + shopee_tweet + blibli_tweet
    labels = [0] * len(bukalapak_tweet) + [1] * len(tokopedia_tweet) + [2] * len(lazada_tweet) + [3] * len(shopee_tweet) + [4] * len(blibli_tweet)

    from sklearn.model_selection import train_test_split

    train_data, test_data, train_labels, test_labels = train_test_split(all_tweet, labels, train_size=0.8, test_size=0.2, random_state=1)

    from sklearn.feature_extraction.text import CountVectorizer

    counter = CountVectorizer()
    counter.fit(train_data, train_labels)

    train_counts = counter.transform(train_data)
    test_counts = counter.transform(test_data)

    from sklearn.naive_bayes import MultinomialNB

    classifier = MultinomialNB()
    classifier.fit(train_counts, train_labels)

    prediction = classifier.predict(test_counts)

    tweet = request.form['inputan']

    tweet_counts = counter.transform([tweet])

    prediksi = classifier.predict(tweet_counts)

    hasil = ""

    if prediksi == [0]:
        hasil += "Bukalapak"
    elif prediksi == [1]:
        hasil += "Tokopedia"
    elif prediksi == [2]:
        hasil += "Lazada"
    elif prediksi == [3]:
        hasil += "Shopee"
    elif prediksi == [4]:
        hasil += "Blibli"

    return render_template("index.html", hasil=hasil, tweet=tweet)

if __name__ == "__main__":
    app.run(debug=True)