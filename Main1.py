from base64 import b64decode as b64d, b64encode as b64e
from json import loads, dumps
from zlib import compress, decompress

def enocde_n_to_m_base(n: int, base: int = 2):
    n, m = divmod(n, base)
    ar = [m]
    while n >= 1:
        n, m = divmod(n, base)
        ar += [m]
    return ar[::-1]


def decode_n_from_m_base(iterable, base=2):
    n = 0
    exp = -1
    for i in iterable[::-1]:
        exp += 1
        n += int(i) * (base ** exp)
    return n

class Tile:
    def __init__(self, block_index, rotation, x, y, tags):
        self.block_index = block_index
        self.rotation = rotation
        self.x = x
        self.y = y
        self.tags = tags

    def __repr__(self):
        return f"{self.block_index} at {self.y} {self.x}"

    def get(self):
        return self.tags["blocks"][self.block_index], self.rotation, self.x, self.y

class Block:
    def __init__(self, block, rotation):
        self.block = block
        self.rotation = rotation

    def __repr__(self):
        return f"{self.block} {self.rotation}"

class Array2D:
    # ik this is retarded, but hey looks nice (jk)
    def __init__(self, width, height, empty_space=None):
        # self.data = [[empty_space] * width] * height  # cant do this, else assigment will point to same object and things will dupicate
        self.data = [[empty_space for n in range(width)] for n in range(height)]
        self.w = width
        self.h = height

    def __repr__(self):
        return str(self.data).replace("],", "],\n")

    def __getitem__(self, item):
        if type(item) is not tuple:
            return self.data[item]
        else:
            x, y = item
            return self.data[y][x]

    def __setitem__(self, key, value):
        if type(key) is not tuple:
            self.data[key] = value
        else:
            x, y = key
            self.data[y][x] = value

class SchematicLoader:
    def __init__(self, schematic):
        self.Schematic = schematic
        self.__s = None

    def __read_first_n(self, n):
        r = self.__s[:n]
        self.__s = self.__s[n:]
        return r

    __r = __read_first_n

    def __readUTF(self, header_type_short=True, nodecode=False):
        if header_type_short:
            n = self.__readBin(2)
        else:
            n = self.__readBin(4)

        out = self.__r(n)
        out = out if nodecode else out.decode()

        return out

    def __readBin(self, n):
        return decode_n_from_m_base(self.__r(n), 256)

    def __readByte(self):
        return self.__readBin(1)

    def __readShort(self):
        return self.__readBin(2)

    def __readInt(self):
        return self.__readBin(4)

    def load(self):
        self.__s, tags = b64d(self.Schematic), {}
        tags["header"] = self.__r(4)
        tags["version"] = self.__r(1)[0]

        self.__s = decompress(self.__s)

        tags["width"] = self.__readShort()
        tags["height"] = self.__readShort()

        # reads the "tags" dict
        tmp = {}
        for n in range(self.__readByte()):
            key = self.__readUTF()
            value = self.__readUTF()
            tmp[key] = value
        tags["tags"] = tmp

        # reads the "blocks" array
        blocks = []
        for n in range(self.__readByte()):
            blocks += [self.__readUTF()]
        tags["blocks"] = blocks

        tags["tags"]["labels"] = loads(tags["tags"]["labels"])

        # reads the "tiles" positions and rotations
        tiles = []
        n = self.__readInt()
        for n in range(n):
            b = self.__readByte()

            y = self.__readShort()
            x = self.__readShort()

            sync_b = self.__readByte()  # just to synchronize (i think)
            r = self.__readByte()
            tiles += [Tile(b, r, x, y, tags)]

        if self.__s:
            # reads the microprocessors code
            _3_byt = self.__readByte(), self.__readByte(), self.__readByte()  # sync bytes ?
            print(_3_byt, decode_n_from_m_base(_3_byt, 256))
            self.__s = decompress(self.__s)

            sync_b = self.__readByte()  # sync bytes ?

            code =  self.__readUTF(False).split("\n")
            sync_i = self.__readInt()  # empty int ?

            tags["code"] = code
            print(code)

        return tags, tiles

class SchematicSaver:
    def __init__(self, schematic):
        self.s: Schematic = schematic
        self.__b = b""

    def __BinaryWriter(self, n, bit_len):
        cn = enocde_n_to_m_base(n, 256)
        if len(cn) != bit_len:
            cn = [0] * (bit_len - len(cn)) + cn

        cn = cn[::-1][:bit_len][::-1]

        self.__b += bytes(cn)

    def __writeInt(self, n: int):
        self.__BinaryWriter(n, 4)

    def __writeShort(self, n: int):
        self.__BinaryWriter(n, 2)

    def __writeByte(self, n: int):
        self.__BinaryWriter(n, 1)

    def __writeUTF(self, text: str):
        if type(text) is not str:
            text = dumps(text)

        self.__writeShort(len(text))
        self.__b += text.encode()

    def save(self):
        # no header here bc isnt compressed

        # self explaining
        self.__writeShort(self.s.width)
        self.__writeShort(self.s.height)

        # writes "tags"
        #  need restruxturizing so this is automated mby, but this will do
        tags = {
            "name": self.s.name,
            "description": self.s.description,
            "labels": self.s.labels
        }
        self.__writeByte(len(tags))
        for t in tags:
            self.__writeUTF(t)
            self.__writeUTF(tags[t])

        # i think this is -s-a-v-i-n-g- processing the block positions (not sure)
        # god blow me
        block_set = []
        tiles = []
        cx = 0
        cy = -1
        for ty in self.s.tiles:
            cy += 1
            for b in ty:
                if b:
                    b: Block
                    if b.block not in block_set:
                        block_set += [b.block]
                    tiles += [Tile(block_set.index(b.block), b.rotation, cx, cy, None)]
                cx += 1
            cx = 0
        del cx, cy

        # this is creating the blocks array
        self.__writeByte(len(block_set))
        for b in block_set:
            self.__writeUTF(b)

        # this is saving the meta data for them like x, y, rotation, block_index in array
        self.__writeInt(len(tiles))
        for t in tiles:
            t: Tile
            i, r, x, y = t.block_index, t.rotation, t.x, t.y

            self.__writeByte(i)
            self.__writeShort(x)
            self.__writeShort(y)
            self.__writeByte(0)
            self.__writeByte(r)

        # compresses -> adds header -> b64 encodes -> decodes to str -> computer goes BUM
        return b64e(b"msch\x01" + compress(self.__b)).decode()

class Schematic:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.labels = []

        self.height = 1
        self.width = 1
        self.raw = {}
        self.tiles = Array2D(1, 1)

    @staticmethod
    def loads(base64_encoded_schematic: str):
        tags, blocks = SchematicLoader(base64_encoded_schematic).load()

        s = Schematic()
        s.blocks = blocks

        name = tags["tags"]["name"]
        description = tags["tags"]["description"]
        labels = tags["tags"]["labels"]
        width = tags["width"]
        height = tags["height"]

        """s.raw = dict()
        s.raw["height"] = tags["height"]
        s.raw["width"] = tags["width"]
        s.raw["name"] = tags["tags"]["name"]
        s.raw["description"] = tags["tags"]["description"]
        s.raw["labels"] = tags["tags"]["labels"]
        s.raw["header"] = tags["header"]
        s.raw["version"] = tags["version"]
        s.raw["raw"] = {}
        s.raw["raw"]["blocks"] = tags["blocks"]
        s.raw["raw"]["tags"] = tags"""

        s.name = name
        s.description = description
        s.labels = labels
        s.width = width
        s.height = height

        s.tiles = Array2D(s.width, s.height)
        for b in blocks:
            bl, br, bx, by = b.get()
            s.tiles[by, bx] = Block(bl, br)

        return s

    def saves(self):
        return SchematicSaver(self).save()

    def __repr__(self):
        return "Schematic: " + self.name



