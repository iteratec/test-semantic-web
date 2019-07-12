import os
import gensim
from gensim.models import fasttext, KeyedVectors

base_path = os.path.abspath('../data/cc.de.300')
w2v_path = base_path + '.w2v'
if not os.path.exists(w2v_path):
    bin_path = base_path + '.bin'
    model = fasttext.load_facebook_vectors(bin_path)

    model.save_word2vec_format(w2v_path, base_path + '.vocab', binary=True)
