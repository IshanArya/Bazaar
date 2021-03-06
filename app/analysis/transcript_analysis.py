import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import json
import os


def update_analyisis():
    module_url = (
        "https://tfhub.dev/google/universal-sentence-encoder/2"
    )  # @param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

    # Import the Universal Sentence Encoder's TF Hub module
    embed = hub.Module(module_url)

    # Compute a representation for each message, showing various lengths supported.
    s1 = "Hey!, how much for the thingy"
    s2 = "That's way too much, I can only do 50"
    s3 = "Alright then, I'll do 55, but I'm not happy about it"

    messages = [s1, s2, s3]

    # Reduce logging output.
    tf.logging.set_verbosity(tf.logging.ERROR)

    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        # message_embeddings = session.run(embed(messages))

        # input_messages = tf.placeholder(dtype=tf.string, shape=[None])

        haggle_messages = [
            "That's way too much, I can only do 50",
            "I'll give you 20 for it",
            "I can only do 26",
            "Would 34 be enough for the bike?",
            "I can't go that high",
            "Come on man, cut me some slack",
            "There's no way it's worth that much" "This is ridiculous",
            "Can you please go a little lower?",
            "I might be able to pay 70, but thats the most I can do",
        ]
        print("embedding training phrases")
        haggle_embeddings = session.run(embed(messages))
        print("training data generated")

        # print(haggle_embeddings)
        def attitude_score(embedding, attitude_embeddings):
            max_score = 0
            for attitude_embeddings in attitude_embeddings:
                max_score = max(max_score, np.inner(embedding, attitude_embeddings))
            return max_score

        # def haggle_score(text):
        #     print("ERBGEBGEFSG", attitude_score(session.run(embed([text]))[0], haggle_embeddings))

        objects = {}
        embedded_objects = {}
        scores = {}
        with open(os.getcwd() + "/app/analysis/transcript.json", "r") as fp:
            objects = json.load(fp)

        print(objects)
        for obj in objects.keys():
            embedded_objects[obj] = session.run(embed(objects[obj]))

        print(embedded_objects)

        for obj in objects.keys():
            phrase_scores = [
                attitude_score(embedding, haggle_embeddings)
                for embedding in embedded_objects[obj]
            ]
            score = sum(phrase_scores) / len(phrase_scores)
            suggestion = "lower the price" if score > 0.5 else "raise the price"
            scores[obj] = {"suggestion": suggestion, "haggle_score": score * 100}

        animals = {
            "cat": "Catty Cabbage",
            "dog": "Doggy Daikons",
            "fish": "Fishy Flaxseeds",
            "bird": "Birdy Broad Beans",
            "elephant": "Elephanty Endives",
            "ostrich": "Ostrichy Oats",
            "hippo": "Hippo Honeydew",
            "tiger": "Tigery Turnips",
            "alligator": "Alligator Aubergine",
            "walrus": "Walrus Watercress",
            "raccoon": "Raccoon Rhubarb",
        }
        new_scores = {}
        for animal in scores.keys():
            new_scores[animals[animal]] = scores[animal]
        scores = new_scores
        print(scores)
        with open(os.getcwd() + "/app/analysis/scores.json", "w") as fp:
            json.dump(scores, fp)
