import zlib
from base64 import b64decode as b64d, b64encode as b64e
from json import loads, dumps
from zlib import compress, decompress
from lib import *

# 1x1 titan_wall name:a
SCHEM = "bXNjaAF4nGNgZGBkZmDJS8xNZWBMZOBOSS1OLsosKMnMz2NgYGDLSUxKzSlmYIqOZWTgLcksSczLLM3VLU/MyQHKMjKAATMAH8IPSQ=="
# 1x2 titan_wall name:aa
SCHEM = "bXNjaAF4nGNgZGBiZmDJS8xNZWBKTGTgTkktTi7KLCjJzM9jYGBgy0lMSs0pZmCKjmVk4C3JLEnMyyzN1S1PzMkByjIxgAEziGBkYAYApOoPsQ=="
# wired
SCHEM = "bXNjaAF4nGNgZmBiZmDJS8xNZWBJBAIG7pTU4uSizIKSzPw8BgYGtpzEpNScYgam6FhGBt6SzJLEvMzSXN3yxJwcoCwLAxgwgwhGEMUI4TGBeADBRBCD"

# moar wired
SCHEM = "bXNjaAF4nDWLSw6FIAxFL2LewM8edAHu4+3AgXGA2hiSCgQwbl8Ise3NPWdQSEiJ2qiL0P2J2Q6z9XyMaA8Ku9cuamsA/FhtxAHVskr0UUdl9H1Nj2JGu1vnyBdpwu1PKpzeUEakVPlEXpEZ+DxVgheTHhvK"

# very complex
SCHEM = "bXNjaAF4nDVOyw7DIAxLQ2iZdtpH7NgvmnZgFK2VWKnoHtrfD2ItEjHYTjAdyBqS1T8i9bMWHae4h7JszyWvRNQnf4tpJ75chVzI6zt+cyGZ/ZLITK9Mp5C3LZbx41Maky/3WMfOpNWhKTDAAOQvc6cG0xpXtd2hCab0MGiGhWFhWIzSFQxegv1KCkgBafGnRSQLi4XFwtK3vVyhpjEVGKRqA7RBk1ZQ0iGgQ0CHbK6l+QFVTxpf"

# cmd (processor)
SCHEM = "bXNjaAF4nGNgZGBkZmDJS8xNZWBOzk1h4E5JLU4uyiwoyczPY2BgYMtJTErNKWZgio5lZODPzUwuytctKMpPTi0uzi8CyjMygAAfEOtWzElOSUgI0NE4dUY7MMBL+5R/+COm4ktFXt3GIkXB3d3Cl4N5dzZ0STAwSXD/ZgYAenYikw=="

# cmd (KOMPLEX)
SCHEM = "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"

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
        header = b"msch\x01"

        self.__writeShort(self.s.width)
        self.__writeShort(self.s.height)

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

        self.__writeByte(len(block_set))
        for b in block_set:
            self.__writeUTF(b)

        self.__writeInt(len(tiles))
        for t in tiles:
            t: Tile
            i, r, x, y = t.block_index, t.rotation, t.x, t.y

            self.__writeByte(i)
            self.__writeShort(x)
            self.__writeShort(y)
            self.__writeByte(0)
            self.__writeByte(r)

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

"""
schematic = Schematic.loads(SCHEM)
x = schematic.saves()

S2 = Schematic.loads(x)
print(S2.raw)
print(schematic)
print(SCHEM)
print(x)
print(S2.saves())"""

s = Schematic.loads(SCHEM)


