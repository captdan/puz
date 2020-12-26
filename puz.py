import sys

def read_str(f):
  res = []
  while True:
    c = f.read(1)
    if c == b'\x00':
      return b''.join(res).decode('latin-1')
    res.append(c)

class Board:
  def __init__(self, filename):
    # read file in binary format
    with open(filename, 'rb') as puz:
      # read header vals
      self.checksum = puz.read(2)
      self.magic = puz.read(12)
      self.cib_checksum = puz.read(2)
      self.masked_low_checksums = puz.read(4)
      self.masked_high_checksums = puz.read(4)
      self.version = puz.read(4)
      self.reserved_1c = puz.read(2)
      self.scrambled_checksum = puz.read(2)
      self.reserved_20 = puz.read(12)
      self.width = int.from_bytes(puz.read(1), "little")
      self.height = int.from_bytes(puz.read(1), "little")
      self.clues_count = int.from_bytes(puz.read(2), "little")
      self.unknown_bitmask = puz.read(2)
      self.scrambled_tag = puz.read(2)

      # read puzzle
      self.solution = []
      for i in range(self.height):
        self.solution.append([])
        for j in range(self.width):
          self.solution[i].append(puz.read(1).decode('latin-1'))

      self.state = []
      for i in range(self.height):
        self.state.append([])
        for j in range(self.width):
          self.state[i].append(puz.read(1).decode('latin-1'))

      # read strings
      self.description = []
      for i in range(3):
        self.description.append(read_str(puz))

      self.clues = []
      for i in range(self.clues_count):
        self.clues.append(read_str(puz))

      #TODO: handle special modes (GRBS, RTBL, LTIM, GEXT, RUSR)

  def __str__(self):
    res = []
    for i in self.state:
      for j in i:
        res += '■' if j == '.' else '□' if j == '-' else j
      res += '\n'
    return ''.join(res)

  def input(self, ch, coord):
    self.state[coord[0]][coord[1]] = ch

  def check(self, coord):
    return self.state[coord[0]][coord[1]] == self.solution[coord[0]][coord[1]]

  def check_row(self, r):
    res = []
    for i in range(self.width):
      res.append(self.check((i, r)))
    return res

  def check_column(self, c):
    res = []
    for i in range(self.height):
      res.append(self.check((c, i)))
    return res

b = Board(sys.argv[1])
b.input('x', (0, 0))
print(b)
print(b.check((0, 0)))
b.input('F', (0,0))
print(b.check((0, 0)))
