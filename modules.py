
modules = ("test", )

from interpreter import prepare_module

for mod in modules:
    prepare_module(mod + ".py")

import __source_test as test