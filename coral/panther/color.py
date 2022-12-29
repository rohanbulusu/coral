
from coral.utils import typename

class Color:

	def __init__(self, r, g, b, a=255):
		self.__r = r
		self.__g = g
		self.__b = b
		self.__a = a

	@staticmethod
	def _format_rgb_value_as_hex_str(value):
		if not isinstance(value, int):
			raise TypeError(f'Expected int, not {typename(value)}')
		if not 0 <= value <= 255:
			raise ValueError(f'Expected rgb value to be between 0 and 255, not {value}')
		raw_hex = str(hex(value))[2:]
		if len(raw_hex) == 2:
			return raw_hex
		return '0' + raw_hex

	@property
	def r(self):
		return self.__r

	@property
	def g(self):
		return self.__g

	@property
	def b(self):
		return self.__b

	@property
	def a(self):
		return self.__a

	@property
	def tk(self):
		r_str = Color._format_rgb_value_as_hex_str(self.r)
		g_str = Color._format_rgb_value_as_hex_str(self.g)
		b_str = Color._format_rgb_value_as_hex_str(self.b)
		return '#' + r_str + g_str + b_str


WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
