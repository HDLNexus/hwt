from hwt.hdl.statements import isSameHVal
from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import GenericSerializer_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.serializer.hwt.context import HwtSerializerCtx


class HwtSerializer_value(GenericSerializer_Value):

    @classmethod
    def Bits_valAsHdl(cls, dtype, val: BitsVal, ctx: HwtSerializerCtx):
        isFullVld = val._is_full_valid()
        if not ctx._valueWidthRequired:
            if isFullVld:
                return "0x%x" % val.val
            elif val.vld_mask == 0:
                return "None"

        if isFullVld:
            vld_maskStr = ""
        else:
            vld_maskStr = ", vld_mask=0x%x" % (val.vld_mask)

        return "%s.from_py(0x%x%s)" % (
            cls.HdlType_bits(dtype, ctx, declaration=False),
            val.val, vld_maskStr)

    @classmethod
    def RtlSignal(cls, s: RtlSignalBase, ctx, declaration=False):
        return cls.SignalItem(s, ctx, declaration=declaration)

    @classmethod
    def SignalItem(cls, si: SignalItem, ctx: HwtSerializerCtx, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            # elif isinstance(si, SignalItem) and si._const:
            #    return cls.Value(si._val, ctx)
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin, ctx)
            else:
                return "%s" % si.name

    @classmethod
    def Value_try_extract_as_const(cls, val, ctx: HwtSerializerCtx):
        # try to extract value as constant
        try:
            consGetter = ctx.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not val._is_full_valid() and not isinstance(val._dtype, HEnum):
            return consGetter(val)

    @classmethod
    def Integer_valAsHdl(cls, t, i, ctx: HwtSerializerCtx):
        if i.vld_mask:
            return "%d" % i.val
        else:
            return "None"

    @classmethod
    def Dict_valAsHdl(cls, val, ctx: HwtSerializerCtx):
        sep = (",\n" + getIndent(ctx.indent + 1))

        def sItem(i):
            k, v = i
            return "%d: %s" % (k, cls.Value(v, ctx))

        return "{%s}" % sep.join(map(sItem, val.items()))

    @classmethod
    def HArrayValAsHdl(cls, t, val: HArrayVal, ctx: HwtSerializerCtx):
        if not val.vld_mask:
            return "None"
        else:
            if len(val.val) == val._dtype.size:
                allValuesSame = True
                values = iter(val.val.values())
                reference = next(values)
                for v in values:
                    if allValuesSame:
                        allValuesSame = isSameHVal(reference, v)
                    else:
                        break
                if allValuesSame:
                    # all values of items in array are same, use generator
                    # exression
                    return "[%s for _ in range(%d)]" % (cls.Value(reference, ctx))

        # if value can not be simplified it is required to serialize it item
        # by item
        return cls.Dict_valAsHdl(val.val, ctx)

    @classmethod
    def Slice_valAsHdl(cls, t, val: SliceVal, ctx: HwtSerializerCtx):
        if val._is_full_valid():
            return "%d:%d" % (int(val.val.start),
                              int(val.val.stop))
        else:
            return "SliceVal(slice(%s, %s, %s), SLICE, %d)" % (
                cls.Value(val.val.start),
                cls.Value(val.val.stop),
                cls.Value(val.val.step),
                val.vld_mask)

    @classmethod
    def HEnumValAsHdl(cls, t, val: HEnumVal, ctx: HwtSerializerCtx):
        return "%s.%s" % (t.name, val.val)

    @classmethod
    def condAsHdl(cls, cond: RtlSignalBase, ctx: HwtSerializerCtx):
        return cls.asHdl(cond, ctx)
