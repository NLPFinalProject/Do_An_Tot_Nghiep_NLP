from model import SiameseBiLSTM
from inputHandler import word_embed_meta_data, create_test_data
from config import siamese_config
import pandas as pd
import pickle
from operator import itemgetter
from keras.models import load_model


def ratio(lst1, lst2):
	df = pd.read_csv('data.csv')

	sentences1 = list(df['sentences1'])
	sentences2 = list(df['sentences2'])
	is_similar = list(df['is_similar'])
	del df

	tokenizer, embedding_matrix = word_embed_meta_data(sentences1 + sentences2,  siamese_config['EMBEDDING_DIM'])

	embedding_meta_data = {
	'tokenizer': tokenizer,
	'embedding_matrix': embedding_matrix
	}

	model_file = open('pretrained.model', 'rb')
	md = pickle.load(model_file)
	model = load_model(md)

	test_sentence_pairs = []
	for str1 in lst1:
		for str2 in lst2:
			test_sentence_pairs.append((str1, str2))

	test_data_x1, test_data_x2, leaks_test = create_test_data(tokenizer, test_sentence_pairs,  siamese_config['MAX_SEQUENCE_LENGTH'])
	preds = model.predict([test_data_x1, test_data_x2, leaks_test], verbose=1).ravel()

	return preds

