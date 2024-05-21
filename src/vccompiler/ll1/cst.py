import logging
from vccompiler.ll1.rule import Rule
from vccompiler.ll1.semantic import left_to_right, cst_pruning


logger = logging.getLogger(__name__)


class CSTNode:
    """
    Initialize a CSTNode.

    Args:
        id: The unique identifier for the node.
        rule: The associated rule (optional).
    """
    def __init__(self, id, rule=None):
        self.id = id
        self.rule = rule
        self.children = []
        self.parent = None
        self.child_pos = None

    def set_ith_child(self, child, i):
        """
        Set the i-th child of the node.

        Args:
            child: The child node to set.
            i: The index of the child.
        """
        self.children[i] = child
        child.parent = self
        child.child_pos = i

    def add_child(self, *children):
        """
        Add one or more children to the node.

        Args:
            children: The child nodes to add.
        """
        for child in children:
            self.children.append(child)
            child.parent = self
            child.child_pos = len(self.children) - 1

    @property
    def semantics(self):
        """
        Get the semantics associated with the node's rule.

        Returns:
            dict: A dictionary containing semantic information.
        """
        return self.rule.semantics if isinstance(self.rule, Rule) else {}

    @property
    def precedence(self):
        """
        Get the precedence of the node.

        Returns:
            int: The precedence value.
        """
        return -1 if "op_prec" not in self.semantics else self.semantics["op_prec"]

    @property
    def operands(self):
        """
        Get the operand indices associated with the node.

        Returns:
            list: A list of operands.
        """
        return [] if "op" not in self.semantics else self.semantics["op"]

    def __str__(self):
        return f"Node({self.id}, {self.rule})"


class CST:
    def __init__(self, semantics=None):
        self.N = 0
        self.root = self.new_node()
        if semantics is None:
            self.semantics = {}
        else:
            self.semantics = semantics

    def new_node(self):
        self.N += 1
        return CSTNode(self.N)

    def left_to_right(self):
        return left_to_right(self.root, self.semantics["left_to_right"])

    def prune(self):
        return cst_pruning(self.root)

    def format(self, engine):
        return engine.format(self.root)

    def draw(self, path):
        try:
            import networkx as nx
        except ImportError:
            logger.error("Parse tree export requires networkx and pydot to be installed")
            return

        G = nx.Graph()

        def dfs(node):
            for i, child in enumerate(node.children):
                G.add_edge(node, child)
                assert child.parent == node
                dfs(child)

        dfs(self.root)
        nx.nx_pydot.write_dot(G, path)
