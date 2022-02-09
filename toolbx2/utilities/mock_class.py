# Setup Mock classes
class Matrix:
  def __init__(self, id):
    self.id = id
class Bank:
  def __init__(self):
     self._matrices = []
  def matrix(self, id):
    for m in self._matrices:
      if m.id == id:
        return m
    return None
  def add_matrix(self, id):
    self._matrices.append(Matrix(id))
# Initialize the databank for te
_bank = Bank()
_bank.add_matrix("mf1")
_bank.add_matrix("mf3")
_bank.add_matrix("mf5")
# Test code
mtx_name = "demand"
transit_classes = [
  {"demand":"mf1"},
  {"demand":"mf2"},
  {"demand":"mf3"},
]
mtx_list = [
            _bank.matrix(tc[mtx_name])
            if tc[mtx_name] == "mf0" or _bank.matrix(tc[mtx_name]).id == tc[mtx_name]
            else print("This is an exception.")
            for tc in transit_classes
]