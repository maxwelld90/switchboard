from pkgutil import walk_packages
from importlib import import_module

class CommandHierarchy(object):

    def __init__(self, base_class, package_name):
        self.base_class = base_class
        self.package_name = package_name
        self.tree = {}

        self.import_classes()
        self.build_tree(base_class)
    
    def build_tree(self, current_class, parent_tree=None):
        if parent_tree is None:
            parent_tree = self.tree
        
        parent_tree[current_class] = {}

        for subclass in current_class.__subclasses__():
            self.build_tree(subclass, parent_tree[current_class])
    
    def import_classes(self):
        package = import_module(self.package_name)

        for _, module_name, _ in walk_packages(package.__path__, f'{package.__name__}.'):
            module = import_module(module_name)
    
    def query(self, command_chain):
        current_level = self.tree[self.base_class]

        for level in command_chain:
            if level in current_level:
               current_level = current_level[level]
               continue

            return f'Unrecognised command. Available commands: {current_level.keys()}'
        
        return [key for key in current_level.keys()]