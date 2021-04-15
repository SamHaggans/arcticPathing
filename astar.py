import math

def findPath(start, end):
    start = Node(start[0], start[1], None, getThickness(start), 0, distance(start, end))
    
    nodes = [start]
    checkNodes = [start]

    while len(checkNodes) > 0:
        
        current = getBestNode(checkNodes)
        if (distance(current.getCoords(), end) ==0):
            return getPath(current)

        checkNodes.remove(current)

        neighbors = getNeighbors(current, nodes)

        for node in neighbors:
            newG = current.getG() + distance(current.getCoords(), node.getCoords()) * weight(current, node)
            if newG < node.getG():
              node.setG(newG)
              node.setF(newG + distance(node.getCoords(), end))
              node.setParent(current)
              checkNodes.append(node)
    print("No path found")
def distance(location1, location2):
  a = location2[0] - location1[0]
  b = location2[1] - location1[1]
  return math.sqrt(a**2 + b**2)

def weight(node1, node2):
  c1 = node1.getCoords()
  c2 = node2.getCoords()
  t1 = getThickness(c1)
  t2 = getThickness(c2)
  return (t1+t2)/2

def getPath(node):
  path = []
  currentNode = node
  while True:
    path.append(currentNode.getCoords())
    currentNode = currentNode.getParent()
    if currentNode == None:
      break
  return path[::-1]#Return the reversed path


class Node:
    def __init__(self, x, y, parent, val, g, f):
        self.x = x
        self.y = y
        self.parent = parent
        self.val = val
        self.g = g
        self.f = f

    def getCoords(self):
        return [self.x, self.y]

    def getParent(self):
        return self.parent

    def getVal(self):
        return self.val
    
    def getG(self):
        return self.g
    
    def getF(self):
        return self.f
    
    def setG(self, g):
        self.g = g
        
    def setF(self, f):
        self.f = f

    def setParent(self, parent):
        self.parent = parent
    
def getThickness(location):
  x = location[0]
  y = location[1]
  return data[y][x]


def getBestNode(nodes):
    minVal = nodes[0].getF()
    minNode = nodes[0]
    for node in nodes:
        if node.getF() < minVal:
            minNode = node
            minVal = node.getF()
    return minNode


def getNeighbors(node, nodes):
  x = node.getCoords()[0]
  y = node.getCoords()[1]
  spaces = []
  spaces.append([x-1, y-1])
  spaces.append([x, y-1])
  spaces.append([x+1, y-1])
  spaces.append([x-1, y])
  spaces.append([x+1, y])
  spaces.append([x-1, y+1])
  spaces.append([x, y+1])
  spaces.append([x+1, y+1])
  neighbors = []

  for s in spaces:
      if s[0] >= 0 and s[1] >= 0 and s[0] < len(data[0]) and s[1] < len(data):
        neighbors.append(getNode(s[0], s[1], nodes, node))
  return neighbors


def getNode(x, y, nodes, parent):

    for node in nodes:
        if node.getCoords()[0] == x and node.getCoords()[1] == y:
            return node
    nodes.append(Node(x, y, parent, getThickness([x, y]), float('inf'), float('inf')))

    return Node(x, y, parent, getThickness([x, y]), float('inf'), float('inf'))

def showPath(path, maxDimension):
  for col in range(maxDimension):
    for row in range(maxDimension):
      if [row, col] in path:
        print("+", end="")
      else:
        print("=", end="")
    print("")

if __name__ == '__main__':
  """
  data = [
  [1, 5, 1, 1, 1],
  [1, 5, 1, 1, 1],
  [1, 1, 5, 1, 1],
  [1, 1, 1, 5, 1],
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1],
  ]
  start = [0,0]
  end = [4, 9]

  path = findPath(start, end)
  showPath(path, 10)
  """

  data = [
  [1, 9, 1, 1, 1],
  [1, 3, 1, 1, 1],
  [1, 9, 1, 9, 1],
  [1, 1, 1, 2, 1],
  [1, 1, 1, 9, 1],
  ]
  start = [0,0]
  end = [4, 4]

  path = findPath(start, end)
  showPath(path, 5)
