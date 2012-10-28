from operator import itemgetter
from math import log, floor, ceil

class Node:
  _childs = []

  def appendNode(self, node):
    self._childs.append(node)

  def child(self, i):
    return self._childs[i];

class LeafNode:
  def __init__(self, classlabel):
    self.classlabel = classlabel

class BinaryThresholdNode(Node):
  feature = None
  threshold = None

  def __init__(self, feature, threshold):
    self.feature = feature
    self.threshold = threshold
    print self.feature, '<=', self.threshold

  def apply(self, instance):
    if instance[self.feature] <= self.threshold:
      return self.child(0)
    else:
      return self.child(1)
    
class Tree:
  tree = None

  def classify(self, instance):
    node = self.tree
    while (not isinstance(node, LeafNode)):
      node = node.apply(instance)
    return node.classlabel

  def _find_binary_threshold(self, data, class_index, feature):
    min_v = float('inf')
    max_v = float('-inf')
    values =  []
    pre_distribution = {}
    for row in data:
      v = row[feature]
      c = row[class_index]
      if v > max_v:
        max_v = v
      if v < min_v:
        min_v = v
      values.append((v,c))
      
      if c in pre_distribution:
        pre_distribution[c] += 1
      else:
        pre_distribution[c] = 1

    classes = pre_distribution.keys()
    values = sorted(values, key=itemgetter(0))
    
    best_v = min_v
    best_distribution = {}
    min_score = float('inf')
    
    start = int(floor(min_v))
    stop = int(ceil(max_v))
    step = int(max([1,floor((max_v-min_v)/10.0)]))
    for v in range(start, stop, step):
      post_distribution = dict.fromkeys(classes,0)
      for value in values:
        if value[0] <= v:
          post_distribution[value[1]] += 1
        else:
          break
      entropy = 0
      s1 = sum(pre_distribution.values())
      s2 = sum(post_distribution.values())
      for c in post_distribution:
        p = (pre_distribution[c]-post_distribution[c])/float(s1-s2)
        if p > 0:
          entropy += -1*p*log(p,2)
      score = entropy*((s1-s2)/float(s1))
      entropy = 0
      for c in post_distribution:
        p = post_distribution[c]/float(s2)
        if p > 0:
          entropy += -1*p*log(p,2)
      score += entropy*(s2/float(s1))
        
      if score < min_score:
        min_score = score
        best_v = v
        best_distribution = post_distribution
    return (min_score, best_v, best_distribution)

class DecisionStump(Tree):

  def train(self, data, class_index):
    self.class_index = class_index
    size = data.size()
    features = range(size[1])
    features.remove(class_index)
    min_score = float('inf')
    best_v = None
    best_distribution = None
    best_feature = None
    for feature in features:
      if type(data[0][feature]) == type(0) or type(data[0][feature]) == type(0.0):
        print "finding splits on",feature
        split = self._find_binary_threshold(data,class_index,feature)

        if split[0] < min_score:
          min_score = split[0]
          best_v = split[1]
          best_distribution = split[2]
          best_feature = feature
    if type(data[0][best_feature]) == type(0) or type(data[0][best_feature]) == type(0.0):
      best_class = max(best_distribution.iteritems(), key=itemgetter(1))[0]
      del best_distribution[best_class]
      second_best_class = max(best_distribution.iteritems(), key=itemgetter(1))[0]
      node = BinaryThresholdNode(best_feature, best_v)
      node.appendNode(LeafNode(best_class))
      node.appendNode(LeafNode(second_best_class))
      self.tree = node;

