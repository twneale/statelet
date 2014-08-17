import types
import contextlib
from collections import ChainMap

from hercules import (
    CachedAttr, CachedClassAttr, DictSetDefault, NoClobberDict)


class ChainedLookup:
    '''Wrapped values get lookup in the ancestor ChainMap objects. Setting
    this attributes sets the value in the instance's own ChainMap.
    '''
    def __init__(self, key):
        self.key = key

    def __get__(self, inst, owner=None):
        self.on_get(inst, owner)
        val = inst.chainmap.get(self.key)
        if val is None and hasattr(self, 'get_value'):
            val = self.get_value(inst, owner)
            inst.chainmap[self.key] = val
        return val

    def __set__(self, inst, value):
        self.on_set(inst, value)
        inst.chainmap[self.key] = value

    def on_get(self, inst, owner):
        '''Gets called before value is returned.
        '''
        pass

    def on_set(self, inst, value):
        '''Gets called before value is set.
        '''
        pass


class StateletMixin:
    '''Lookups for these attributes on subtypes will fail over
    to whatever object's ChainMap the object's own ChainMap was derived
    from, and on up the chain, all the way back down the original object.
    '''
    @property
    def chainmap(self):
        '''This property manages the instance's ChainMap objects.
        '''
        chainmap = getattr(self, '_chainmap', None)
        if chainmap is not None:
            return chainmap
        else:
            chainmap = ChainMap()
            self._chainmap = chainmap
            return chainmap

    @chainmap.setter
    def chainmap(self, chainmap):
        self._chainmap = chainmap

    def set_parent_chainmap(self, chainmap):
        '''Set `chainmap` as the parent of self.chainmap.
        '''
        self.chainmap = ChainMap(self.chainmap.maps[0], *chainmap.maps)

    def provide_chainmap_to(self, has_child_chainmap):
        '''Set self.chainmap as the parent of child's chainmap.
        '''
        has_child_chainmap.set_parent_chainmap(self.chainmap)
        return has_child_chainmap

    def inherit_chainmap_from(self, has_parent_chainmap):
        '''Set this object as the chainmap parent of has_child_chainmap.
        '''
        self.set_parent_chainmap(has_parent_chainmap.chainmap)
        return has_parent_chainmap

    def make_child(self, child_type, *child_args, **child_kwargs):
        '''Invoke the passed in type with the args/kwargs, then provide
        self.chainmap to it, basically making it a child context.
        '''
        child = child_type(*child_args, **child_kwargs)
        return self.provide_chainmap_to(child)