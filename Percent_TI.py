from __future__ import division
import os, re, sys, math
from numpy import zeros
from collections import defaultdict


class Calculator:
	def __init__(self, confusion_matrix):
		self.confusion_matrix = confusion_matrix
		#obtains the total number of rows
		self.i_len = len(self.confusion_matrix)
		#obtains the total number of columns
		self.j_len = len(self.confusion_matrix[1])
		#establishes data-structures for future functions
		self.init_prob_matrix = zeros(shape=(self.i_len,self.j_len))
		self.t_vector = []
		self.h_vector = []


	def percent_ti(self):

		self.initial_probability_matrix()
		self.sigma_calculations()
		for t in self.t_vector:
			if math.isnan(t):
				self.t_vector[self.t_vector.index(t)] = 0
		self.calculate_percent_ti()


	def initial_probability_matrix(self):
		self.i_count = 0
		for i in self.init_prob_matrix:
			self.j_count = 0
			for j in self.init_prob_matrix[1]:
				self.init_prob_matrix[self.i_count,self.j_count] = self.confusion_matrix[self.i_count,self.j_count]/self.confusion_matrix[self.i_len-1,self.j_len-1]

				self.j_count += 1
			
			self.i_count+=1


	def sigma_calculations(self):
		self.i = 0
		for i in self.init_prob_matrix:
			if self.i == self.i_count-1:
				break
			self.j = 0
			for j in self.init_prob_matrix[self.i]:
				if self.j == self.j_count-1:
					#calculate p_i times the log2 of p_i; append to vector to be summed
					try:
						self.h_vector.append(self.init_prob_matrix[self.i,self.j]*math.log(self.init_prob_matrix[self.i,self.j],2))
					except ValueError as e:
						self.h_vector.append(0)
					break
				#calc the log2 of (the product of p_i & p_j, divided by p_ij), multiplied by p_ij; append to vector to be summed
				self.t_vector.append(float(self.init_prob_matrix[self.i,self.j]*math.log(self.init_prob_matrix[self.i,self.j_count-1]*self.init_prob_matrix[self.i_count-1,self.j]/self.init_prob_matrix[self.i,self.j],2)))

				self.j += 1

			self.i += 1


	def calculate_percent_ti(self):
		self.perc_ti = float(sum(self.t_vector)/sum(self.h_vector))
		print "Percent TI = " + str(self.perc_ti)
		self.final_values = [sum(self.t_vector), sum(self.h_vector), self.perc_ti]