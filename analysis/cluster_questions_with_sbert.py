"""
Use SentenceBERT encoding to find meaningful clusters in NL questions
"""
from os import path
import json
from sentence_transformers import SentenceTransformer
from sklearn import cluster

SPIDER_DATA_FOLDER = "spider_data"
TRAIN_JSON_FILENAME = "train_spider.json"
CLUSTER_COUNT = 15

embedder = SentenceTransformer('bert-base-nli-mean-tokens')


if __name__ == "__main__":
    with open(path.join(SPIDER_DATA_FOLDER, TRAIN_JSON_FILENAME), "r") as train_json:
        questions = [entry["question"] for entry in json.load(train_json)][:50]

    corpus_embeddings = embedder.encode(questions)

    # clustering_model = cluster.OPTICS(min_samples=3, min_cluster_size=0.1)
    clustering_model = cluster.AgglomerativeClustering(linkage="single", n_clusters=CLUSTER_COUNT)

    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = [[] for i in range(max(cluster_assignment)+1)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(questions[sentence_id])

    for i, cluster in enumerate(clustered_sentences):
        print("Cluster ", i + 1)
        print(cluster)
        print("")
        print("")
