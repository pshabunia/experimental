import pickle
import random

from os import path
from scipy.spatial import KDTree

FILE = 'servo_map.data'

class ServoMap:
	def __init__(self):
		self.kdtree = None
		if path.exists(FILE):
			with open(FILE, 'rb') as file:
				self.datamap = pickle.load(file)
				self.spatial_index = KDTree([[x,y] for (x,y) in self.datamap.keys()])

	def query(self, x, y):
		if self.spatial_index:
			_, index_arr = self.spatial_index.query([[x, y]])
			if index_arr:
				nearest_point = self.spatial_index.data[index_arr[0]]
				(xx, yy) = nearest_point
				return self.datamap[(xx, yy)]
		
		return (1500 + random.randrange(0, 200), 1650 + random.randrange(0,200))
