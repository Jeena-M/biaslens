import gensim.downloader as api 

# Small, fast embedding (50d)
embedding_model = api.load("glove-wiki-gigaword-50")

masc_words = ["rockstar", "dominate", "crush", "aggressive", "man", "take", "charge"]

import numpy as np

def is_masculine(text, threshold=0.6):
    words = text.lower().split()
    for w in words:
        for seed in masc_words:
            try:
                similarity = embedding_model.similarity(w, seed)
                if similarity > threshold:
                    return True, w, seed  # return word found and seed word
            except KeyError:
                continue  # word not in embedding
    return False, None, None
