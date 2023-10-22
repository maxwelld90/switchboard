from client.ops.command_base import CommandBase

class Auth(CommandBase):
    """
    
    """
    command = 'auth'
    title = 'User Authentication'
    description = 'User authentication description'

    def __init__(self):
        super().__init__()

class Second(Auth):
    """
    
    """
    command = 'secondlevel'
    title = 'User Authentication Level 2'
    description = 'Second level description'

    def __init__(self):
        super().__init__()