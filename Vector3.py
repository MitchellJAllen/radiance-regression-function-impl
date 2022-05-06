import math

class Vector3:
	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	# useful for print(str(myVector))
	def __str__(self):
		return f'<{self.x},{self.y},{self.z}>'

	# useful for print([myVector])
	def __repr__(self):
		return f'<{self.x},{self.y},{self.z}>'

	def __pos__(self):
		return Vector3(+self.x, +self.y, +self.z)

	def __neg__(self):
		return Vector3(-self.x, -self.y, -self.z)

	def __add__(self, vector):
		return Vector3(self.x + vector.x, self.y + vector.y, self.z + vector.z)

	def __sub__(self, vector):
		return Vector3(self.x - vector.x, self.y - vector.y, self.z - vector.z)

	def __mul__(self, scalar):
		return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

	def __truediv__(self, scalar):
		return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

	def __rmul__(self, scalar):
		return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

	def __iadd__(self, vector):
		self.x += vector.x
		self.y += vector.y
		self.z += vector.z

		return self

	def __isub__(self, vector):
		self.x -= vector.x
		self.y -= vector.y
		self.z -= vector.z

		return self

	def __imul__(self, scalar):
		self.x *= scalar
		self.y *= scalar
		self.z *= scalar

		return self

	def __itruediv__(self, scalar):
		self.x /= scalar
		self.y /= scalar
		self.z /= scalar

		return self

	def dot(self, vector):
		return (self.x * vector.x + self.y * vector.y + self.z * vector.z)

	def cross(self, vector):
		return Vector3(
			self.y * vector.z - self.z * vector.y,
			self.z * vector.x - self.x * vector.z,
			self.x * vector.y - self.y * vector.x
		)

	def length(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

	def normalize(self):
		inverseLength = (
			1 / math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
		)

		return Vector3(
			self.x * inverseLength, self.y * inverseLength,
			self.z * inverseLength
		)
