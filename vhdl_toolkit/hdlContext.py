from vhdl_toolkit.hdlObjects.reference import VhdlRef 
from vhdl_toolkit.nonRedefDict import NonRedefDict
from vhdl_toolkit.types import VHDLType, Unconstrained


class RequireImportErr(Exception):
    def __init__(self, reference):
        super(RequireImportErr, self).__init__()
        self.reference = reference
        self.fileName = None
    
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if self.fileName:
            fileName = 'file %s' % self.fileName
        else:
            fileName = '' 
        return "<RequireImportErr %s require to import %s first>" % (fileName, str(self.reference))
    
class HDLParseErr(Exception):
    pass

def mkType(name, width, minimum=None):
    t = VHDLType()
    t.name = name
    t.width = width
    t.min = minimum
    return t


class BaseVhdlContext():
    integer = mkType("integer", int)
    positive = mkType("positive", int, 1)
    natural = mkType("natural", int, 0)
    boolean = mkType("boolean", bool)
    string = mkType("string", str)
    float = mkType("float", float)
   
    @classmethod
    def importFakeLibs(cls, ctx):
        BaseVhdlContext.importFakeIEEELib(ctx)
        BaseVhdlContext.importFakeUnisim(ctx)

    @classmethod
    def importFakeUnisim(cls, ctx):
        ctx.insert(VhdlRef(["unisim", "vcomponents", 'ramb4_s16']), None)   
   
    @classmethod 
    def importFakeIEEELib(cls, ctx):
        ctx.insert(FakeStd_logic_1164.std_logic_vector_ref, FakeStd_logic_1164.std_logic_vector)
        ctx.insert(FakeStd_logic_1164.std_logic_ref, FakeStd_logic_1164.std_logic)
        ctx.insert(VhdlRef(['ieee', 'std_logic_unsigned', 'CONV_INTEGER']), None)
        ctx.insert(VhdlRef(['ieee', 'std_logic_arith', 'IS_SIGNED']), None)
        ctx.insert(FakeStd_logic_1164.numeric_std_ref, FakeStd_logic_1164.numeric_std)
    
    @classmethod
    def getBaseCtx(cls):
        d = HDLCtx(None, None)
        for n in [cls.integer, cls.positive, cls.natural,
                   cls.boolean, cls.string, cls.float]:
            d[n.name] = n
        d['true'] = True
        d['false'] = False
        return d

class HDLCtx(NonRedefDict):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.entities = NonRedefDict()
        self.architectures = []
        self.packages = NonRedefDict()
        
    def importLibFromGlobal(self, ref):
        """
        Import for example lib.package to local context
        """
        top = self
        while top.parent is not None:
            top = top.parent
        try:
            toImport = top
            for n in ref.names:
                toImport = toImport[n]
            if ref.all:
                for n in toImport:
                    self[n] = toImport[n]
            else:
                raise NotImplementedError()
        except KeyError:
            raise RequireImportErr(ref)
    def lookupGlobal(self, ref):
        p = self
        n = ref.names[0]  # [TODO]
        while p.parent is not None:
            p = p.parent
        if p is None:
            raise RequireImportErr(ref)
        try:
            for n in ref.names:
                p = p[n]
            return p
        except KeyError:
            raise RequireImportErr(ref)
        
    def lookupLocal(self, locRef):
        p = self
        n = locRef.names[-1]  # [TODO]
        while p is not None:
            try:
                return p[n]
            except KeyError:
                p = p.parent
        
        raise Exception("Identificator %s not defined" % n)
    
    def insert(self, ref, val):
        c = self
        for n in ref.names[:-1]:
            c = c.setdefault(n, HDLCtx(n, c))
        c[ref.names[-1]] = val    
    def __str__(self):
        return "\n".join([
                    "\n".join([str(e) for _, e in self.entities.items()]),
                    "\n".join([str(a) for a in self.architectures]),
                    "\n".join([str(p) for p in self.packages]),
                    ])
class FakeStd_logic_1164():
    std_logic_vector = mkType("std_logic_vector", Unconstrained)
    std_logic_vector_ref = VhdlRef(["ieee", "std_logic_1164", "std_logic_vector"])
    std_logic = mkType("std_logic", 1)
    std_logic_ref = VhdlRef(["ieee", "std_logic_1164", "std_logic"])
    numeric_std_ref = VhdlRef(["ieee", "numeric_std"])
    numeric_std = HDLCtx('numeric_std', None) 
        