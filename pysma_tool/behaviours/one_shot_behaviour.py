from .behaviour import Behaviour


class OneShotBehaviour(Behaviour):
    
    def done(self) -> bool:
        """Get the behaviour has completed its execution.
        
        Returns:
            bool: True everytime."""
        return True
