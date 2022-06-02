from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

class asosiasiApriori:
	def __init__(self, min_threshold=1, metric='lift',min_support=0.7):
		self.__min_threshold = min_threshold
		self.__metric = metric
		self.__min_support = min_support

	def modelApriori(self, data):
		apriori(min_threshold=self.__min_threshold,min_support=self.__min_support,use_colnames=True)
		output = association_rules(apriori,min_threshold=self.__min_threshold,metric=self.__metric)
		return output
