# Lib model klasifikasi
import tensorflow as tf

# Load pickle
import pickle

import pandas as pd
import numpy as np
import re
import os


# Lib transformers
import transformers as ts
import torch


import pathlib



model_inisialisasi = 0
"""
	Transformasi data
"""
def dataTransform(text):
	# Penghapusan spasi dan transformasi ke huruf kecil
	text = text.casefold().strip()

	# Penghapusan URL
	text = re.sub(r'https?://\S+|www\.\S+', '', text)

	# Penghapusan emoji
	text = re.sub("[^A-Za-z0-9\s.,']","",text)
	return text

class chatbot:
	def __init__(self, data):
		global model_inisialisasi
		"""
			Bila model telah diinisialisasi maka tidak akan dijalankan kembali
		"""
		if (model_inisialisasi == 0):
			# Mengambil tokens yang dibuaT pada saat training
			with open(os.getcwd()+'//model_development//model//qas//klasifikasi//tokenizerTextClassification.pickle','rb') as tokens:
				self.__tokenizerKlasifikasi = pickle.load(tokens)

			# Mengambil hasil tranining terbaik
			self.__tokenizerQAS = ts.BertTokenizer.from_pretrained(os.getcwd()+'//model_development//model//qas')

			# Mengambil model klasifikasi
			# self.__modelKlasifikasi = tf.keras.models.load_model(os.getcwd()+'//model_development//model//qas//klasifikasi/ClassificationLSTM.h5')
			"""
				Menggunakan model klasifikasi yang telah dikompress
			"""
			self.__modelKlasifikasi = tf.lite.Interpreter(model_path=str(pathlib.Path(os.getcwd()+'//model_development//model//qas//klasifikasi//')/"LSTMKlasifikasiKonteksQuants.tflite"))
			self.__modelKlasifikasi.allocate_tensors()

			# Mengambil model yang telah di training
			self.__modelQAS = ts.BertForQuestionAnswering.from_pretrained(os.getcwd()+'//model_development//model//qas')

			# Padding
			self.__maxPad = 20

			model_inisialisasi = 1

		self.__data = self.konfigurasiData(data)


	"""
		Pembuatan matriks sequence dan padding
		serta penentu indeks jawaban awal dan indeks jawaban akhir
	"""
	def questionAnswering(self, pertanyaan, text):
		hasil = ""

		inputIds = self.__tokenizerQAS.encode(pertanyaan, text)
		tokens = self.__tokenizerQAS.convert_ids_to_tokens(inputIds)
		nilaiSEP = inputIds.index(self.__tokenizerQAS.sep_token_id)
		segmen=[0]*(nilaiSEP+1) + [1]*(len(inputIds)-(nilaiSEP+1))

		outputLogits = self.__modelQAS(torch.tensor([inputIds]), token_type_ids=torch.tensor([segmen]))

		indexAwalJawaban = torch.argmax(outputLogits.start_logits)
		indexAkhirJawaban = torch.argmax(outputLogits.end_logits)

		if(indexAkhirJawaban >= indexAwalJawaban):
			hasil = tokens[indexAwalJawaban]
			for i in range(indexAwalJawaban+1, indexAkhirJawaban+1):
				if(tokens[i][0:2] == '##'):
					hasil += tokens[i][2:]
				else:
					hasil += ' ' + tokens[i]

			if hasil.startswith('[CLS]'):
				hasil ="Mohon maaf, kami tidak dapat menemukan jawaban."

			return hasil.capitalize().strip()

	"""
		Klasifikasi konteks pertanyaan yang merujuk pada tempat wisata
	"""
	def klasifikasiKonteks(self, pertanyaan):
		X = tf.keras.preprocessing.sequence.pad_sequences(self.__tokenizerKlasifikasi.texts_to_sequences([pertanyaan.casefold()]),self.__maxPad).astype(np.float32)

		# Klasifikasi Menggunakan TFLITE
		prediksi = []

		input_index = self.__modelKlasifikasi.get_input_details()[0]['index']
		output_index = self.__modelKlasifikasi.get_output_details()[0]['index']

		self.__modelKlasifikasi.set_tensor(input_index, X)
		self.__modelKlasifikasi.invoke()
		prediksi.append(np.argmax(self.__modelKlasifikasi.get_tensor(output_index))+1)
		
		# Klasifikasi Model Tanpa Optimisasi
		# prediksi = [i+1 for i in np.argmax(self.__modelKlasifikasi.predict(X), axis = 1)]
		return prediksi

	"""
		Pengambilan jawaban pertanyaan
	"""
	def getJawaban(self, pertanyaan):
		# Klasifikasi unutk mendapatkan konteks label pertanyaan
		label = self.klasifikasiKonteks(pertanyaan)

		print([label[0]])
		# Pengambilan konteks
		konteks = self.__data[self.__data.place_id == label[0]]['description'].values[0]

		# Prediksi jawaban
		return self.questionAnswering(pertanyaan.casefold(),konteks)

	def konfigurasiData(self, datas):
		df = pd.DataFrame({
			'place_id':[data.place_id for data in datas],
			'description':[data.description+" Tempat wisata ini memiliki Harga tiket sebesar "\
			+str(int(data.price))+" dan memiliki rating "+str(data.rating)\
			 for data in datas]
  			})

		print(df)
		print("\n\n\n")
		print(df['description'])
		df['description'] = df['description'].apply(dataTransform)
		print(df['description'])
		return df