from sys import argv

from client.ops.command_base import CommandBase
from client.ops.command_hierarchy import CommandHierarchy

if __name__ == '__main__':
    hierarchy = CommandHierarchy(CommandBase, 'client.commands')

    command_chain = argv[1:]
    print(hierarchy.query(command_chain))