
import tkinter as tk
import time
from collections.abc import Sequence

from coral.utils import typename, chain

from linal.vector import Vector


class Point(Vector):

	def __init__(self, *coordinates):
		super().__init__(*coordinates)

	def __iter__(self):
		return self

	def __next__(self):
		stack = list(self.components)
		for _ in range(len(stack)):
			yield stack.pop()
		raise StopIteration

	def __getitem__(self, index):
		if not isinstance(index, int):
			raise TypeError(f'Expected index of type int, not {typename(index)}')
		return self.components[index]


class Line:

	def __init__(self, a, b):
		if not isinstance(a, Point):
			raise TypeError(f'Expected Point, not {typename(a)}')
		if not isinstance(b, Point):
			raise TypeError(f'Expected Point, not {typename(b)}')
		self.a = a
		self.b = b


class Entity:

	REGISTERED_ENTITY_IDS = []

	def __init__(self, points, lines):
		if not isinstance(points, Sequence):
			raise TypeError(f'Expected a Sequence of Point objects, not a {typename(points)}')
		if not all(isinstance(Vector, point) for point in points):
			raise TypeError(f'Expected all points to be of type Vector')
		if not all(point.dim >= 3 or point.dim == 0 for point in points):
			raise ValueError(f'Expected all points to have a dimension of at least three')
		if not all(point.dim == points[0].dim for point in points):
			raise ValueError(f'Expected all points to have the same dimension')
		if not isinstance(lines, Sequence):
			raise TypeError(f'Expected a Sequence of Line objects, not a {typename(lines)}')
		if not all(isinstance(line, Line) for line in lines):
			raise TypeError(f'Expected all lines to be of type Line')
		self._set_entity_id()
		self.points = points
		self.lines = lines
		self.orientation = Vector(*[0 for _ in range(points[0].dim)])
		self.center = Vector.average(*points)

	def _set_entity_id(self):
		self.__id = id(self)
		REGISTERED_ENTITY_IDS.append(self.__id)

	@property
	def id(self):
		return self.__id

	@staticmethod
	def is_valid_entity_id(candidate):
		if not isinstance(candidate, int):
			return False
		return candidate in REGISTERED_ENTITY_IDS


class Window(tk.Canvas):

	def __init__(self, width, height):
		super().__init__(width=width, height=height)
		self.entities = []
		self.pack(fill=tk.BOTH, expand=tk.TRUE)

	def add_entities(self, *entities):
		if not all(isinstance(Entity, entity) for entity in entities):
			raise TypeError(f'Expected all entities to be of type {typename(Entity)}')
		self.entities = chain(self.entities, entities)

	def render_point(self, entity_id, point, point_diameter=8, **kwargs):
		if not Entity.is_valid_entity_id(entity_id):
			raise ValueError(f'Entity id {entity_id} is not a valid Entity id')
		if not isinstance(point, Point):
			raise TypeError(f'Expected Point, not {typename(point)}')
		radius = point_diameter // 2
		self.canvas.create_oval(
			point[0] - radius, point[1] - radius,
			point[0] + radius, point[1] + radius,
			**kwargs
		)

	def render_line(self, line, line_weight=1, **kwargs):
		if not isinstance(line, Line):
			raise TypeError(f'Expected Line, not {typename(line)}')
		self.canvas.create_line(
			line.a[0], line.a[1],
			line.b[0], line.b[1]
			width=line_weight,
			**kwargs
		)

	def render_parabolic_spline(self, points, n=12, **kwargs):
		if not isinstance(points, Sequence) and not all(isinstance(point, Point) for point in points):
			raise TypeError(f'Expected a Sequence of Point objects, not a {typename(points)}')
		if not all(isinstance(point, Point) for point in points):
			raise TypeError(f'Expected a Sequence of Point objects, not a Sequence of {typename(points[0])} objects')
		self.canvas.create_line(
			*chain(*[(point[0], point[1]) for point in points]),
			smooth=True, splinesteps=n, 
			**kwargs
		)

	def render_entity(self, entity):
		if not isinstance(entity, Entity):
			raise TypeError(f'Expected object of type Entity, not {typename(entity)}')
		for line in entity.lines:
			self.render_line(line)
		for point in entity.points:
			self.render_point(point)

	def render_all_entities(self):
		for entity in self.entities:
			self.render_entity(entity)

	def run(self):
		while True:
			self.render_all_entities()
			self.update_idletasks()
			self.update()


if __name__ == '__main__':

	w = Window(200, 200, background_color='#255000255')
	w.run()
	w.perpetuate = False

