# Lib model klasifikasi
import tensorflow as tf

# Load pickle
import pickle

import pandas as pd
import numpy as np

# Lib transformers
import transformers as ts
import torch

class chatbot:
	def __init__(self, data):

		# Mengambil tokens yang dibuaT pada saat training
		with open('model/qas/klasifikasi/tokenizerTextClassification.pickle','rb') as tokens:
			self.tokenizerKlasifikasi = pickle.load(tokens)

		# Mengambil hasil tranining terbaik
		self.tokenizerQAS = ts.BertTokenizer.from_pretrained('model/qas/best_save_model')

		# Mengambil model klasifikasi
		self.modelKlasifikasi = tf.keras.models.load_model('model/qas/klasifikasi/ClassificationLSTM.h5')

		# Mengambil model yang telah di training
		self.modelQAS = ts.BertForQuestionAnswering.from_pretrained('model/qas/best_save_model')

		# Padding
		self.maxPad = 20

		self.data=pd.read_csv('data/data_QAS2.csv')

	"""
		Pembuatan matriks sequence dan padding
		serta penentu indeks jawaban awal dan indeks jawaban akhir
	"""
	def questionAnswering(self, pertanyaan, text):
		hasil = ""

		inputIds = self.tokenizerQAS.encode(pertanyaan, text)
		tokens = self.tokenizerQAS.convert_ids_to_tokens(inputIds)
		nilaiSEP = inputIds.index(self.tokenizerQAS.sep_token_id)
		segmen=[0]*(nilaiSEP+1) + [1]*(len(inputIds)-(nilaiSEP+1))

		outputLogits = self.modelQAS(torch.tensor([inputIds]), token_type_ids=torch.tensor([segmen]))

		indexAwalJawaban = torch.argmax(outputLogits.start_logits)
		indexAkhirJawaban = torch.argmax(outputLogits.end_logits)

		if(indexAkhirJawaban > indexAwalJawaban):
			hasil = tokens[indexAwalJawaban]
			for i in range(indexAwalJawaban+1, indexAkhirJawaban+1):
				if(tokens[i][0:2] == '##'):
					hasil += tokens[i][2:]
				else:
					hasil += ' ' + tokens[i]

		if hasil.startswith('[CLS]'):
			hasil ="Mohon maaf, kami tidak dapat menemukan jawaban."

		return hasil.capitalize()

	"""
		Klasifikasi konteks pertanyaan yang merujuk pada tempat wisata
	"""
	def klasifikasiKonteks(self, pertanyaan):
  		X = pad_sequences(tokenizer.texts_to_sequences([pertanyaan.casefold()]),self.maxPad=20)

  		prediksi = [i+1 for i in np.argmax(self.modelKlasifikasi.predict(X), axis = 1)]
  		return prediksi


  	"""
		Pengambilan jawaban pertanyaan
  	"""
  	def getJawaban(self, pertanyaan, label):
  		# Klasifikasi unutk mendapatkan konteks label pertanyaan
  		label = klasifikasiKonteks(pertanyaan)

  		# Pengambilan konteks
  		konteks = data[data.Place_Id == label[0]]['Description'].values[0]

  		# Prediksi jawaban
  		return self.questionAnswering(pertanyaan.casefold(),konteks)