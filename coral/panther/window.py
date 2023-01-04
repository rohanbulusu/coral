
import tkinter as tk
import time
from collections.abc import Sequence

from coral.utils import typename, chain, zeros, ones

from linal.vector import Vector
from linal.rotations import ThreeDimensionalRotation
from color import Color, WHITE, BLACK


class Point(Vector):

	def __init__(self, *coordinates):
		if len(coordinates) < 2:
			raise ValueError(f'Expected at least two components to construct a Point')
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

	def scale(self, *scale_factors):
		if len(scale_factors) != self.dim:
			raise ValueError(f'Expected {self.dim} arguments but recieved only {len(scale_factors)}')
		if not all(isinstance(factor, (int, float)) for factor in scale_factors):
			raise TypeError(f'Expected all scale factors to be either of type int or float')
		self.components = tuple([
			c*factor for c, factor in zip(self.components, scale_factors)
		])

	@staticmethod
	def dist(a, b):
		if not isinstance(a, Point):
			raise TypeError(f'Expected Point object, got {typename(a)}')
		if not isinstance(b, Point):
			raise TypeError(f'Expected Point object, got {typename(b)}')
		if not a.dim == b.dim:
			raise ValueError(f'Expected two Point objects of the same dimension')
		return sum((a[i]**2 - b[i]**2) for i in range(a.dim))**0.5

	def rotate3D(self, xy_angle, xz_angle, yz_angle):
		if self.dim != 3:
			raise ValueError(f'Expected Vector to have dimension at least three')
		self.components = tuple((
			Rot3.xy(xy_angle)*Rot3.xz(xz_angle)*Rot3.yz(yz_angle)*self
		).components)

	def translate3D(self, x_delta, y_delta, z_delta):
		self.components = tuple((self + Point(x_delta, y_delta, z_delta)).components)


class Line:

	def __init__(self, a, b):
		if not isinstance(a, Point):
			raise TypeError(f'Expected Point, not {typename(a)}')
		if not isinstance(b, Point):
			raise TypeError(f'Expected Point, not {typename(b)}')
		if a.dim != b.dim:
			raise TypeError(f'Expected both points to have the same dimension')
		self.a = a
		self.b = b
		self.dim = self.a.dim

	@property
	def length(self):
		return ((self.a[0] - self.b[0])**2 + (self.b[0]-self.a[0])**2)**0.5

	def scale(self, *scale_factors):
		if len(scale_factors) != self.dim:
			raise ValueError(f'Expected {self.dim} arguments but recieved only {len(scale_factors)}')
		if not all(isinstance(factor, (int, float)) for factor in scale_factors):
			raise TypeError(f'Expected all scale factors to be either of type int or float')
		self.a.scale(*scale_factors)
		self.b.scale(*scale_factors)


class EntityId:

	def __init__(self, entity, entity_id):
		if not isinstance(entity, Entity):
			raise TypeError(f'Expected Entity, not {typename(entity)}')
		if not isinstance(entity_id, int):
			raise TypeError(f'Expected int, not {typename(entity_id)}')
		self.entity = entity
		self.id = entity_id

	@property
	def tk(self):
		return str(self)

	def __repr__(self):
		return f'EntityId({self.id})'

	def __hash__(self):
		return self.id


class Entity:

	REGISTERED_ENTITY_IDS = []

	def __init__(self, points, lines, fill=BLACK, border=BLACK, point_width=2, point_color=BLACK):
		if not isinstance(points, Sequence):
			raise TypeError(f'Expected a Sequence of Point objects, not a {typename(points)}')
		if not all(isinstance(point, Vector) for point in points):
			raise TypeError(f'Expected all points to be of type Vector')
		if not all(point.dim >= 3 or point.dim == 0 for point in points):
			raise ValueError(f'Expected all points to have a dimension of at least three')
		if not all(point.dim == points[0].dim for point in points):
			raise ValueError(f'Expected all points to have the same dimension')
		if not isinstance(lines, Sequence):
			raise TypeError(f'Expected a Sequence of Line objects, not a {typename(lines)}')
		if not all(isinstance(line, Line) for line in lines):
			raise TypeError(f'Expected all lines to be of type Line')
		if not isinstance(fill, Color):
			raise TypeError(f'Expected Color, not {typename(fill)}')
		if not isinstance(border, Color):
			raise TypeError(f'Expected Color, not {typename(border)}')
		if not isinstance(point_width, int):
			raise TypeError(f'Expected int, not {typename(point_width)}')
		if not point_width >= 0:
			raise ValueError(f'Expected point width to be greater than 0, not {point_width}')
		if not isinstance(point_color, Color):
			raise TypeError(f'Expected Color, not {typename(point_color)}')
		self._set_entity_id()
		self.points = points
		self.lines = lines
		self.dimension = self.points[0].dim
		self.orientation = Vector(0, 1).pad_to(self.points[0].dim)
		self.center = Vector.average(*points)
		self.fill = fill.tk
		self.border = border.tk
		self.point_width = point_width
		self.point_color = point_color.tk
	# nothing
	def _set_entity_id(self):
		self.__id = EntityId(self, id(self))
		Entity.REGISTERED_ENTITY_IDS.append(self.__id)

	def scale(self, *scale_factors):
		if len(scale_factors) != self.dimension:
			raise ValueError(f'Expected {self.dimension} arguments but recieved only {len(scale_factors)}')
		if not all(isinstance(factor, (int, float)) for factor in scale_factors):
			raise TypeError(f'Expected all scale factors to be either of type int or float')
		# the only thing that needs to be scaled is the points,
		# since the lines are based on references to the points
		# already contained in self.points
		for point in self.points:
			point.scale(*scale_factors)

	@property
	def id(self):
		return self.__id

	@staticmethod
	def is_valid_entity_id(candidate):
		return candidate in Entity.REGISTERED_ENTITY_IDS


class Window(tk.Canvas):

	def __init__(self, width, height, fill=WHITE):
		if not isinstance(width, int):
			raise TypeError(f'Expected width to be an int, not a {typename(width)}')
		if not width > 0:
			raise ValueError(f'Expected width to be greater than 0')
		if not isinstance(height, int):
			raise TypeError(f'Expected height to be an int, not a {typename(height)}')
		if not height > 0:
			raise ValueError(f'Expected height to be greater than 0')
		if not isinstance(fill, Color):
			raise TypeError(f'Expected fill to be a Color, not a {typename(fill)}')
		super().__init__(width=width, height=height, bg=fill.tk)
		self.entities = []
		self.window_dimensions = (self.winfo_reqwidth(), self.winfo_reqwidth())
		self.pack(fill=tk.BOTH, expand=tk.TRUE)

	@property
	def width(self):
		return self.winfo_width()

	@property
	def height(self):
		return self.winfo_height()

	def center_to_window(self, point_vector):
		if not isinstance(point_vector, Point):
			raise TypeError(f'Expected a Point, not a {typename(point_vector)}')
		return point_vector + Vector(self.width/2, self.height/2).pad_to(point_vector.dim)

	def add_entities(self, *entities):
		if not all(isinstance(entity, Entity) for entity in entities):
			raise TypeError(f'Expected all entities to be of type {typename(Entity)}')
		self.entities = chain(self.entities, entities)

	def render_point(self, entity_id, point, **kwargs):
		if not Entity.is_valid_entity_id(entity_id):
			raise ValueError(f'Entity id {entity_id} is not a valid Entity id')
		if not isinstance(point, Point):
			raise TypeError(f'Expected Point, not {typename(point)}')
		radius = entity_id.entity.point_width // 2
		p = self.center_to_window(point)
		self.create_oval(
			p[0] - radius, p[1] - radius,
			p[0] + radius, p[1] + radius,
			fill=entity_id.entity.point_color,
			outline=entity_id.entity.point_color,
			**kwargs,
			tags=[entity_id.tk]
		)

	def render_line(self, entity_id, line, **kwargs):
		if not Entity.is_valid_entity_id(entity_id):
			raise ValueError(f'Entity id {entity_id} is not a valid Entity id')
		if not isinstance(line, Line):
			raise TypeError(f'Expected Line, not {typename(line)}')
		self.render_line_from_points(entity_id, line.a, line.b, **kwargs)

	def render_line_from_points(self, entity_id, a, b, line_weight=1, **kwargs):
		if not Entity.is_valid_entity_id(entity_id):
			raise ValueError(f'Entity id {entity_id} is not a valid Entity id')
		if not isinstance(a, Point):
			raise TypeError(f'Expected Point, not {typename(a)}')
		if not isinstance(b, Point):
			raise TypeError(f'Expected Point, not {typename(b)}')
		A = self.center_to_window(a)
		B = self.center_to_window(b)
		self.create_line(
			A[0], A[1],
			B[0], B[1],
			width=line_weight,
			fill=entity_id.entity.border,
			**kwargs,
			tags=[entity_id.tk]
		)

	def render_entity(self, entity):
		if not isinstance(entity, Entity):
			raise TypeError(f'Expected object of type Entity, not {typename(entity)}')
		for line in entity.lines:
			self.render_line(entity.id, line)
		for point in entity.points:
			self.render_point(entity.id, point)

	def render_all_entities(self):
		for entity in self.entities:
			self.render_entity(entity)

	def _on_window_resize(self, event):
		x_scale_factor = self.width / self.window_dimensions[0]
		y_scale_factor = self.height / self.window_dimensions[1]
		self.scale('all', 0, 0, x_scale_factor, y_scale_factor)
		for entity in self.entities:
			entity.scale(x_scale_factor, y_scale_factor, *ones(entity.dimension-2))
		self.window_dimensions = (self.width, self.height)

	def _on_B1_drag(self, event):
		...

	def _on_B2_drag(self, event):
		...

	def clear_entities(self):
		self.delete('all')

	def run(self):
		self.bind('<Configure>', self._on_window_resize)
		self.bind('<B1-Motion>', self._on_B1_drag)
		self.bind('<B2-Motion>', self._on_B2_drag)
		while True:
			self.clear_entities()
			self.render_all_entities()
			self.update_idletasks()
			self.update()


if __name__ == '__main__':

	a, b, c, d = [Point(-100, 0, 0), Point(100, 0, 0), Point(0, 100, 0), (Point(0, 0, 100))]

	e = Entity(
		[a, b, c, d],
		[Line(a, b), Line(a, c), Line(b, c), Line(a, d), Line(b, d), Line(c, d)],
		point_width=0,
		point_color=WHITE
	)

	w = Window(500, 500)
	w.add_entities(e)
	w.run()
	w.perpetuate = False
