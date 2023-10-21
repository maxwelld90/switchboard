from client.ops.command_base import CommandBase
from client.ops.command_hierarchy import CommandHierarchy

if __name__ == '__main__':
    hierarchy = CommandHierarchy(CommandBase, 'client.commands')

    print(hierarchy.query('CommandBase.Auth'))