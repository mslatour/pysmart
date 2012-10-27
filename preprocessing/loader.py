import csv
from pysmart.structures.matrix import Matrix2D

class CSVDataLoader:

  def load(self, src, dl=',', qc='"'):
    data = []
    with open(src, 'r') as csvfile:
      reader = csv.reader(csvfile, delimiter=dl, quotechar=qc)
      for datarow in reader:
        data.append(datarow)
    return Matrix2D(data)
