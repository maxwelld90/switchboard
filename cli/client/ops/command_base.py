
class CommandBase(object):
    """
    
    """
    command = None
    title = None
    description = None
    
    def __init__(self):
        """
        
        """
        if None in (self.command, self.title, self.description) and not type(self) is CommandBase:
            raise NotImplementedError('Subclasses must define command, title, and description.')
    
    def __str__(self):
        return self.command