from pysmart.structures.matrix import *

class TypeConverter:
  @staticmethod
  def cast_matrix(matrix, types):
    size = matrix.size()
    casted = Matrix2D.genmat(size[0],size[1],None).get_raw()
    for row in range(size[0]):
      for col in range(size[1]):
        casted[row][col] = {
          'int': int,
          'float': float,
          'string': str
        }[types[col]](matrix[row][col])
    return Matrix2D(casted)
