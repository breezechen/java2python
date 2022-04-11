#!/usr/bin/env python
# -*- coding: utf-8 -*-
# java2python.config -> subpackage for run-time configuration.

from functools import reduce
from imp import load_source
from os import path


class Config(object):
    """ Config -> wraps multiple configuration modules. """

    def __init__(self, names):
        self.configs = [self.load(name) for name in names]

    def every(self, key, default=None):
        """ Returns the value at the given key from each config module. """
        return [getattr(config, key, default) for config in self.configs]

    def last(self, key, default=None):
        """ Returns the value at the key from the last config defining it. """
        return next(
            (
                getattr(config, key)
                for config in reversed(self.configs)
                if hasattr(config, key)
            ),
            default,
        )

    @staticmethod
    def load(name):
        """ Imports and returns a module from dotted form or filename. """
        return (
            load_source(str(hash(name)), name)
            if path.exists(name) and path.isfile(name)
            else reduce(getattr, name.split('.')[1:], __import__(name))
        )
