
from math import sin, cos

from .matrix import Matrix


class TwoDimensionalRotation:

	def __new__(cls, theta):
		"""Angle units in radians"""
		return Matrix(
			[cos(theta), -sin(theta)],
			[sin(theta), cos(theta)]
		)


class ThreeDimensionalRotation:
	
	@staticmethod
	def xy(theta):
		return Matrix(
			[cos(theta), -sin(theta), 0],
			[sin(theta), cos(theta), 0],
			[0, 0, 1]
		)

	@staticmethod
	def xz(theta):
		return Matrix(
			[cos(theta), 0, -sin(theta)],
			[0, 1, 0],
			[sin(theta), 0, cos(theta)]
		)

	@staticmethod
	def yz(theta):
		return Matrix(
			[0, cos(theta), -sin(theta)],
			[0, sin(theta), cos(theta)],
			[1, 0, 0]
		)

