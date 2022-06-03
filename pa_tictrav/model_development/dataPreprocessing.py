import pandas as pd
import numpy as np 

from sklearn.model_selection import train_test_split

class DataPreprocessing:
	def __init__(self,data):
		self.__data = pd.DataFrame(data)

		"""
			Terdapat dua opsi, yaitu ekstraksi fitur berdasarkan Category, atau Place_Name
		"""

	def dropNull(self,axis=1):
		data = self.__data.dropna(axis=axis)
		return data 

	def dropColumns(self,axis=1,columns=[]):
		data = self.__data.drop(columns, axis=axis)
		return data 

	"""
    	Alternatif dapat menggunakan matriks transpose
	"""
	def transformDataByTarget(self,target=None,value=None,dropby=[]):
	    
	    # Pengecekan apakah target dan value tidak kosong
	    if(not (target or value)):
	        return None
	    
	    # Pengubahan data tourism place menjadi kolom, dan menghapus kolom place_name
	    data_transform = pd.get_dummies(self.data.copy(), columns=[target])
	    
	    # Mendapatkan index target dan value yang akan dimasukan ke dalam target
	    indexValue = list(data_transform.columns).index(value)
	    indexTarget = list(self.data.columns).index(target)
	    
	    # Inisialisasi index user
	    currentIndexUser = 0
	    
	    for i in range(self.data.shape[0]):
	        """
	            Akan dilakukan pengecekan user_id, bila sama, maka data yang akan dimodifikasi
	            adalah index pertama dari user tersebut, bila berbeda, maka data tersebut perlu diambil
	            namanya untuk mendapatkan index pertama dari user tersebut
	        """
	        if(data_transform.iloc[currentIndexUser,0] == self.data.iloc[i,0]):
	            data_transform.iloc[currentIndexUser,data_transform.columns.get_loc(f'{target}_{self.data.iloc[i,indexTarget]}')]=data_transform.iloc[i,indexValue]
	        else:
	            currentIndexUser = self.data[self.data.User_Id == data_transform.iloc[i,0]].iloc[0,:].name
	            data_transform.iloc[currentIndexUser,data_transform.columns.get_loc(f'{target}_{self.data.iloc[i,indexTarget]}')]=data_transform.iloc[i,indexValue]
	    
	    # Penghapusan duplikasi data berdasarkan nilai dropby dan penghapusan kolom value
	    data_transform = data_transform.drop_duplicates(subset=dropby)
	    data_transform.drop([value],axis=1,inplace=True)
	    return data_transform


	def splitTrainTest(self,features=[],target=[],test_size=0, random=0):
		X, y = self.__data[features],self.__data[target]
		return train_test_split(X, y, test_size=test_size, random_state=random)

