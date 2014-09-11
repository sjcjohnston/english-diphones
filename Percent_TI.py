from __future__ import division
import os, re, sys, math
from numpy import zeros
from collections import defaultdict


class Calculator:
	def __init__(self, confusion_matrix):
		self.confusion_matrix = confusion_matrix

	def percent_ti(self):
		