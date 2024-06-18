"""Composite behaviour module"""

from typing import Optional

from .behaviour import Behaviour
from ..exceptions.exceptions import BehaviourException 
from pygraph_tool import Graph, NodeException, GraphException, Node


class CompositeBehaviour(Behaviour):
    """Define CompositeBehaviour class inherits to Behaviour.
    
    Attributes:
        id_first_state (Optional[str]): The identifier of first behaviour. By
            default is None.
        id_last_state (Optional[str]): The identifier of last behaviour. By
            default is None.
        id_current_state (Optional[str]): The identifier of current behaviour.
            By default is None.
        children_graph (Graph): The graph of sub behaviours. By default is
            empty graph.
        is_termination (bool): True if CompositeBehaviour is terminated. By
            default False.
    """

    def __init__(self) -> None:
        """Instantiate CompositeBehaviour class."""
        super().__init__()
        self._id_first_state: Optional[str] = None
        self._id_last_state: Optional[str] = None
        self._id_current_state: Optional[str] = None
        self._children_graph: Graph = Graph()
        self._is_termination: bool = False

    @property
    def id_first_state(self) -> Optional[str]:
        """The identifier of first behaviour."""
        return self._id_first_state
    
    @id_first_state.setter
    def id_first_state(self, id_first_state: Optional[str]) -> None:
        self._id_first_state = id_first_state

    @property
    def id_last_state(self) -> Optional[str]:
        """The identifier of last behaviour."""
        return self._id_last_state
    
    @id_last_state.setter
    def id_last_state(self, id_last_state: Optional[str]) -> None:
        self._id_last_state = id_last_state

    @property
    def id_current_state(self) -> Optional[str]:
        """The identifier of current behaviour."""
        return self._id_current_state
    
    @id_current_state.setter
    def id_current_state(self, id_current_state: Optional[str]) -> None:
        self._id_current_state = id_current_state
        
    @property
    def children_graph(self) -> Graph:
        """The graph of sub behaviours."""
        return self._children_graph
    
    @children_graph.setter
    def children_graph(self, children_graph: Graph) -> None:
        self._children_graph = children_graph

    @property
    def is_termination(self) -> bool:
        """True if CompositeBehaviour is terminated."""
        return self._is_termination
    
    @is_termination.setter
    def is_termination(self, is_termination: bool) -> None:
        self._is_termination = is_termination

    def action(self) -> None:
        """CompositeBehaviour execution process."""
        current_node: Node = self._children_graph.get_node(
            self._id_current_state
        )

        if current_node.node_content.run() is None:
            return self.action()
        
        self.schedule_next()
        if self._is_termination:
            return
        return self.action()
    
    def schedule_first(self) -> None:
        """Determines the values of first, last and current states."""
        if len(self._children_graph.nodes) >= 1:
            self._id_first_state = self._children_graph.nodes[0].node_id
            self._id_last_state = self._children_graph.nodes[-1].node_id

        if not self._id_current_state:
            self._id_current_state = self._id_first_state
    
    def schedule_next(self) -> None:
        """Determines the value of next state."""
        current_node: Node = self._children_graph.get_node(
            self._id_current_state
        )
        index_current_node: int = self._children_graph.nodes.index(
            current_node
        )
        index_next_state: int = index_current_node + 1
        if index_next_state < len(self._children_graph.nodes):
            self._id_current_state = self._children_graph.nodes[
                index_next_state
            ].node_id
        else:
            self._is_termination = True

    def done(self) -> bool:
        """Get the behaviour has completed its execution.

        Returns:
            bool: True if the behaviour has completed its execution.
        """
        return self._is_termination

    def reset_children(self) -> None:
        """Restores all sub behaviours to their initial state."""
        for child in self._children_graph.nodes():
            child.node_content.reset()

    def add_sub_behaviour(
        self, behaviour: Behaviour, behaviour_id: str
    ) -> None:
        """Add a sub behaviour in graph.

        Args:
            behaviour (Behaviour): Behaviour to add.
            behaviour_id (str): Behaviour identifier.

        Raises:
            BehaviourException: If behaviour not inherits to Behaviour or
                if behaviour is impossible to add.
        """
        if not isinstance(behaviour, Behaviour):
            raise BehaviourException(
                "Parameter 'behaviour' must be Behaviour instance."
                f"Behaviour {behaviour_id} is impossible to add."
            )
        try:
            behaviour.parent = self
            self._children_graph.add_node(behaviour, behaviour_id)
        except (NodeException, GraphException) as error:
            raise BehaviourException(
                f"Behaviour {behaviour_id} is impossible to add: {error}"
            ) from error
    
    def remove_sub_behaviour(self, behaviour_id: str) -> None:
        """Remove one sub behaviour.

        Args:
            behaviour_id (str): The identifier of the behaviour to remove.
        """
        self._children_graph.remove_node(behaviour_id)

    def run(self) -> Optional[int]:
        """Run the behaviour.

        Returns:
            Optional[int]: The return of on_end method or None if not done.
        """
        self.schedule_first()
        return super().run()
