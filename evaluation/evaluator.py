class BasicEvaluator:
  # Confusion matrix
  cmatrix = []
  classes = []
  c_len = 0

  def __init__(self, classes):
    c_len = len(classes)
    self.cmatrix = [[0 for col in range(c_len)] for row in range(c_len)]
    self.classes = classes
    self.c_len = c_len

  def evaluate_by_testset(self, classifier, testset, class_index):
    self.clear_confusion_matrix()
    if len(testset) > 0:
      indices = range(len(testset[0]))
      indices.remove(class_index)
      for instance in testset:
        c = self.classes.index(classifier.classify(instance[indices]))
        r = self.classes.index(instance[class_index])
        self.cmatrix[r][c] += 1
  
  def clear_confusion_matrix(self):
    self.cmatrix = [[0 for col in range(self.c_len)] for row in range(self.c_len)]

  def get_confusion_matrix(self):
    return self.cmatrix

  def accuracy(self):
    c = self.cmatrix
    return (c[0][0]+c[1][1])/float(sum(c[0])+sum(c[1]))
