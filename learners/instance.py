from operator import itemgetter

class KNearestNeighbor:

  k = 1   
  weighted = True
  data = []
  cols = []
  class_index = 0

  def __init__(self, k=1, weighted=True):
    self.k = k
    self.weighted = weighted

  def train(self, data, class_index):
    self.data = data
    self.cols = range(len(data[0]))
    self.cols.remove(class_index)

  def classify(self,instance):
    # Calculate distances from each train point
    neighbors = []
    for row in self.data:
      dist = 0;
      for col in range(len(instance)):
        dist += abs(row[self.cols[col]] - instance[col])
      neighbors.append((dist, row[self.class_index]))
    # Sort neighbors on their distance
    neighbors = sorted(neighbors, key=itemgetter(0))
    # Count the votes of the k best neighbors
    class_votes = {}
    for n in range(0,self.k):
      if not neighbors[n][1] in class_votes:
        class_votes[neighbors[n][1]] = 0

      if self.weighted:
        class_votes[neighbors[n][1]] += neighbors[n][0]
      else:
        class_votes[neighbors[n][1]] += 1
    # Find the classification with the most votes
    max_class = None
    max_vote = 0
    for c in class_votes:
      if class_votes[c] > max_vote:
        max_class = c
        max_vote = class_votes[c]
    return max_class
