class Matrix2D:
  data = []
  rows = 0
  cols = 0

  def __init__(self, raw):
    self.data = raw
    self.rows = len(raw)
    if self.rows > 0:
      self.cols = len(raw[0])

  def vslice(self, indices):
    indices_len = len(indices)
    sliced = [[None for col in range(indices_len)] for row in range(self.rows)]
    for row in range(self.rows):
      for col in range(indices_len):
        sliced[row][col] = self.data[row][indices[col]]
    return Matrix2D(sliced)

  def __getitem__(self, ind):
    if type(ind) == type(0):
      return Vector(self.data[ind])
    elif isinstance(ind, slice):
      if ind.step is None:
        ind = range(ind.start, ind.stop)
      else:
        ind = range(ind.start, ind.stop, ind.step)

    ind_len = len(ind)
    sliced = [[None for col in range(self.cols)] for row in range(ind_len)]
    for row in range(ind_len):
      for col in range(self.cols):
        sliced[row][col] = self.data[ind[row]][col]
    return Matrix2D(sliced)

  def __len__(self):
    return self.rows

  def size(self, dim=None):
    if dim is None:
      return (self.rows, self.cols)
    elif dim == 1:
      return self.rows
    else:
      return self.cols
  
  def indices(self):
    return range(len(self))

  def __iter__(self):
    for i in range(len(self)):
      yield self[i]

  def get_raw(self):
    return self.data

class Vector(Matrix2D):
  def __init__(self, raw):
    Matrix2D.__init__(self, [raw])
 
  def __getitem__(self, ind):
    if type(ind) == type(0):
      return self.data[0][ind]
    elif isinstance(ind, slice):
      if ind.step is None:
        ind = range(ind.start, ind.stop)
      else:
        ind = range(ind.start, ind.stop, ind.step)
    
    ind_len = len(ind)
    sliced = [None for row in range(ind_len)]
    for col in range(ind_len):
      sliced[col] = self.data[0][ind[col]]
    return Vector(sliced)

  def __len__(self):
    return self.cols
