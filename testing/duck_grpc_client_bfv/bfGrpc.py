from enum import Enum
import inspect
from io import BytesIO
import struct


class GRPCController:
    def __init__(self, file: BytesIO | None = None):
        self.fp = file
        self.__total_size = 0

    def deserialize_bytes(
        self, data: bytes, what: type["gRPCMessage"]
    ) -> "gRPCMessage":
        self.fp = BytesIO()
        self.fp.write(data)
        self.fp.seek(0)
        output = self.deserialize(what)
        self.fp.seek(0)
        return output

    def serialize_bytes(self, what: "gRPCMessage | str") -> bytes:
        self.fp = BytesIO()
        self.serialize(what)
        self.fp.seek(0)
        return self.fp.read()

    def deserialize(self, what: type["gRPCMessage"]) -> "gRPCMessage":
        """
        Deserialize grpc packet into expected Class
        """
        self.__parseHeader()
        return self.__visitMessage(what, self.__total_size)

    def serialize(self, what: "gRPCMessage | str"):
        """
        Serialize class into grpc packet
        """
        b = BytesIO()
        s = self.__writeMessage(b, what)
        self.__total_size = s
        self.__writeHeader(self.__total_size)
        b.seek(0)
        self.fp.write(b.read())
        return

    def readMessage(self, msg_cls):
        size = self.__readVI32()
        return self.__visitMessage(msg_cls, size)

    def readFloat(self):
        t = self.readVarInt()
        e = 2 * (t >> 31) + 1
        n = t >> 23 & 255
        t &= 8388607
        if 255 == n:
            if t != 0:
                return None
            else:
                return 1 / 0 * e
        elif 0 == n:
            return e * pow(2, -149) * t
        else:
            return e * pow(2, n - 150) * (t + pow(2, 23))

    def readString(self) -> str:
        s = self.__readVI32()
        sb = self.fp.read(s)
        s = sb.decode("utf-8")
        return s  #''.join(map(chr, sb))

    def writeString(self, where, string) -> int:
        # I added the bytes in UTF-8. example: Gurizin Paulista ツ on the route /bf6/player
        if isinstance(string, bytes):
            data = string
        else:
            data = string.encode("utf-8")
        length = len(data)
        s = self.__writeVI32(where, length)
        if length > 0:
            where.write(data)
        # Returns the total written: bytes of length (s) + bytes of the string
        return s + length

    def readVarInt(self) -> int:
        return self.__readVI32()

    def readF32(self) -> float:
        return float(struct.unpack("f", self.fp.read(4))[0])

    def writeF32(self, where: BytesIO, v) -> float:
        where.write(struct.pack("f", v))
        return 4

    def writeVarInt(self, where: BytesIO, v) -> int:
        return self.__writeVI32(where, v)

    def writeVarInt64(self, where: BytesIO, v) -> int:
        return self.__writeVI64(where, v)

    def __readSplittedInt64(self):
        e = 128
        n = 0
        i = 0
        o = 0
        while 4 > o and 128 <= e:
            e = self.fp.read(1)[0]
            n |= (127 & e) << 7 * o
            o += 1

        if 128 <= e:
            e = self.fp.read(1)[0]
            n |= (127 & e) << 28
            k = (127 & e) >> 4

            if 128 <= e:
                o = 0
                while 5 > o and 128 <= e:
                    e = self.fp.read(1)[0]
                    i |= (127 & e) << ((7 * o) + 3)
                    o += 1

        if 128 > e:
            return i, n

        print("Wrong Var64")
        return None

    def readVarInt64(self) -> int:
        e, t = self.__readSplittedInt64()
        return self.__joinUint64(e, t)

    def readSignedVarInt64(self) -> int:
        e, t = self.__readSplittedInt64()
        return self.__joinInt64(e, t)

    def readZigzagVarInt64(self) -> int:
        e, t = self.__readSplittedInt64()
        return self.__joinZigzag64(e, t)

    def __joinUint64(self, e, t):
        return (e * 4294967296) + t

    def __joinInt64(self, e: int, t: int):
        n = 2147483648 & e
        if n != 0:
            e = ~e
            t = 1 + ~t
            if 0 == t:
                e = e + 1
        t = self.__joinUint64(e, t)
        if n != 0:
            return -t
        return t

    def __joinZigzag64(self, e: int, t: int):
        i = -(1 & t)
        return self.__joinInt64((t >> 1 | e << 31) ^ i, (e >> 1) ^ i)

    def writeNext(self, where: BytesIO, fid: int, wire: int):
        t = (wire & 7) | (fid << 3)
        i = self.__writeVI32(where, t)
        return i

    # def writeBytes(self, where, b):
    #     where.write(bytes([127 & low | 128]))
    #     return len(b)

    # Private

    def __writeVI32(self, where: BytesIO, t: int) -> int:
        if 2**31 > t >= -(2**31):
            return self.__writeVU32(where, t)
        else:
            i = 0
            while True:
                i += 1
                if t:
                    where.write(bytes([t & 0x7F | 128]))
                    t >>= 7
                else:
                    where.write(bytes([t]))
                    break
            return i

    def __writeVU32(self, where: BytesIO, t: int) -> int:
        i = 1
        while t >= 128:
            where.write(bytes([t & 127 | 128]))
            t >>= 7
            i += 1
        where.write(bytes([t & 127]))
        return i

    def __readVI32(self):
        b = self.fp.read(1)[0]
        n = b & 127
        n2 = n
        c = 1
        while b > 127:
            b = self.fp.read(1)[0]

            if c == 4:
                n2 |= (b & 15) << 7 * c

            else:
                n2 |= (b & 127) << 7 * c

            n |= (b & 127) << 7 * c
            c += 1

        return n

    def __writeVI64(self, where: BytesIO, t: int):
        high = int(t / 4294967296)
        low = t - high
        i = 1

        while 0 < high or 127 < low:
            where.write(bytes([127 & low | 128]))
            low = low >> 7 | high << 25
            high >>= 7
            i += 1

        where.write(bytes([low]))
        return i

    def __readNext(self):
        t = self.__readVI32()
        wire = t & 7
        fid = t >> 3
        return wire, fid

    def __skip_field(self, wire: int):
        if wire == 0:
            l = self.__readVI32()
        elif wire == 1:
            self.fp.read(8)
        elif wire == 2:
            to_skip = self.__readVI32()
            print(to_skip)
            self.fp.read(to_skip)
        elif wire == 5:
            self.fp.read(4)
        elif wire == 3:
            # f, w = self.__readNext()
            # if w == 4:
            print("We can't skip group yet!")
            pass
        return

    def __parseHeader(self):
        null = self.fp.read(1)
        sb = self.fp.read(4)
        self.__total_size = int.from_bytes(sb, "big")

    def __writeHeader(self, size: int):
        self.fp.write(b"\x00")
        self.fp.write(size.to_bytes(4, byteorder="big"))

    @classmethod
    def underlying_fields(cls, other: "gRPCMessage | str") -> set[str]:
        field_map = set()
        for class_member in inspect.getmembers(other):
            if class_member[0].startswith("_"):
                continue
            # If noraml grpc field
            if not inspect.ismethod(class_member[1]) and isinstance(
                class_member[1], TypedGRPC
            ):
                field_map.add(class_member[0])
        return field_map

    def __visitMessage(self, cls, size: int) -> "gRPCMessage":
        fields = self.underlying_fields(cls)
        start = self.fp.tell()
        inst = cls()
        while self.fp.tell() < start + size:
            w, f = self.__readNext()
            found = False
            for field_name in fields:
                field = getattr(cls, field_name)
                if field.field_id == f:
                    val = field.des(self)
                    if field.is_list():
                        if inst.has_rpc_value(field_name):
                            l = inst.get_rpc_value(field_name)
                            l.append(val)
                        else:
                            setattr(inst, "grpc_" + field_name, [val])
                    else:
                        setattr(inst, "grpc_" + field_name, val)
                    found = True
                    break
            if not found:
                print(f"Unresolved field {f} :[{w}] ({cls})")
                self.__skip_field(w)
        for field_name in fields:
            field = getattr(cls, field_name)
            if not inst.has_rpc_value(field_name) and field.default is not None:
                setattr(inst, "grpc_" + field_name, field.default)

        return inst

    def writeMessage(self, where: BytesIO, inst):
        buf = BytesIO()
        i = self.__writeMessage(buf, inst)
        v = self.__writeVI32(where, i)
        buf.seek(0)
        where.write(buf.read())
        return i + v

    def __writeMessage(self, where: BytesIO, inst: "gRPCMessage | str"):
        fields = self.underlying_fields(inst)
        i = 0
        for field_name in fields:
            field = getattr(inst, field_name)
            if not inst.has_rpc_value(field_name):
                continue
            value = inst.get_rpc_value(field_name)
            if value is None:
                continue
            if field.is_list():
                for item in value:
                    i += field.ser(self, where, item)
            else:
                i += field.ser(self, where, value)
        return i


class TypedGRPC(object):
    def __init__(self, field_id: int, cls: type, default=None, ignore=False):
        self.field_id = field_id
        self._cls = cls
        self.default = default
        self.ignore = ignore

    def is_msg(self) -> bool:
        return issubclass(self._cls, gRPCMessage)

    def is_flat(self) -> bool:
        return issubclass(self._cls, gRPCMessageFlat)

    def is_list(self) -> bool:
        return isinstance(self, TypedGRPCList)

    def des(self, context: "GRPCController"):
        if self._cls == str:
            return context.readString()
        elif self._cls == gRPCInt64:
            return context.readVarInt64()
        elif self._cls == gRPCSignedInt64:
            return context.readSignedVarInt64()
        elif self._cls == gRPCZigzagInt64:
            return context.readZigzagVarInt64()
        elif self._cls == gRPCFloat32:
            return context.readF32()
        elif self._cls == int:
            return context.readVarInt()
        elif issubclass(self._cls, Enum):
            return self._cls(context.readVarInt()).name
        elif self._cls == bool:
            return context.readVarInt() != 0
        elif self._cls == float:
            return context.readFloat()
        elif self.is_msg():
            return context.readMessage(self._cls)
        else:
            return None

    def ser(self, context: "GRPCController", where: BytesIO, value):
        i = 0
        if self._cls == str:
            i += context.writeNext(where, self.field_id, 2)
            i += context.writeString(where, value)
        elif self._cls == gRPCInt64:
            i += context.writeNext(where, self.field_id, 0)
            i += context.writeVarInt64(where, value)
        elif self._cls == gRPCFloat32:
            i += context.writeNext(where, self.field_id, 5)
            i += context.writeF32(where, value)
        elif self._cls == int:
            i += context.writeNext(where, self.field_id, 0)
            i += context.writeVarInt(where, value)
        elif issubclass(self._cls, Enum):
            i += context.writeNext(where, self.field_id, 0)
            i += context.writeVarInt(where, self._cls(value).value)
        elif self._cls == bool:
            bool_v = 1 if value else 0
            i += context.writeNext(where, self.field_id, 0)
            i += context.writeVarInt(where, bool_v)
        elif self.is_msg():
            i += context.writeNext(where, self.field_id, 2)
            i += context.writeMessage(where, value)
        return i


class TypedGRPCList(TypedGRPC):
    pass


class gRPCMessage:
    def get_rpc_value(self, name: str) -> "gRPCMessage | None":
        if self.has_rpc_value(name):
            return getattr(self, "grpc_" + name)
        else:
            return None

    def has_rpc_value(self, name: str) -> bool:
        return hasattr(self, "grpc_" + name)

    def set_rpc_value(self, name: str, value) -> None:
        setattr(self, "grpc_" + name, value)

    def to_dict(self) -> dict:
        return self._as_dict()

    def _as_dict(self) -> dict:
        output = {}
        fields = GRPCController.underlying_fields(self)
        for f in fields:
            field = getattr(self, f)
            it = self.get_rpc_value(f)
            if field.ignore:
                break
            if field.is_msg():
                if field.is_list():
                    output[f] = []
                    if it is not None:
                        for item in it:
                            idi = item.to_dict()
                            if field.is_flat():
                                ws = False
                                for k, idi_k in idi.items():
                                    if idi_k.__class__ == str:
                                        output[f].append(idi_k)
                                        ws = True
                                        break
                                if not ws:
                                    output[f].append(idi)
                            else:
                                output[f].append(idi)
                elif it is None:
                    output[f] = None
                elif field.is_flat():
                    output.update(it.to_dict())
                else:
                    output[f] = it.to_dict()
            else:
                output[f] = it
        return output


class gRPCInt64(int):
    pass


class gRPCFloat32(float):
    pass


class gRPCFloat64(float):
    pass


class gRPCSignedInt64(int):
    pass


class gRPCZigzagInt64(int):
    pass


class gRPCMessageFlat(gRPCMessage):
    pass


class gRPCMessageEnum(gRPCMessage):
    def to_dict(self) -> dict:
        out = dict()
        for key, val in self._as_dict().items():
            if val is not None:
                out[key] = val
                break
        return out
