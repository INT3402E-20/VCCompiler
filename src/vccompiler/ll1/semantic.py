from vccompiler.lexer.token import Token


def left_to_right(root, precedences: set[int]):
    if root.precedence not in precedences:
        for i, child in enumerate(root.children):
            root.set_ith_child(left_to_right(child, precedences), i)
        return root

    descendants = []
    operators = []

    # recursively retrieve tree nodes
    def dfs(node, operand_set):
        for pos, child in enumerate(node.children):
            if pos in node.operands:
                # for operand edges: check if the child has the same precedence as the root
                operand_set.append((node, pos))
                if child.precedence == root.precedence:
                    # assign a new operator
                    new_operand_set = []
                    operators.append((child, new_operand_set))
                    dfs(child, new_operand_set)
                else:
                    # append to descendant list, and skip this child
                    descendants.append(child)
            else:
                # this child belongs to the current operator, keep searching
                dfs(child, operand_set)

    initial_operand_set = []
    operators.append((root, initial_operand_set))
    dfs(root, initial_operand_set)

    # left associative
    stack = []
    stack.extend(descendants[::-1])
    for op, operand_set in operators:
        # assign the children with the top of the stack
        for node, pos in operand_set:
            node.set_ith_child(stack.pop(), pos)
        stack.append(op)

    assert len(stack) == 1

    for child in descendants:
        # for descendant (non-operators or operator with different precedence)
        parent = child.parent
        child_pos = child.child_pos
        parent.set_ith_child(left_to_right(child, precedences), child_pos)

    return stack.pop()


def cst_pruning(root):
    """
    Prunes the root, and returns True if the subtree is null
    :param root:
    :return:
    """
    if isinstance(root.rule, str):
        return root.rule == ""
    if isinstance(root.rule, Token):
        return False
    not_null = []
    for i in range(len(root.children)):
        # check if the child isn't null
        if not cst_pruning(root.children[i]):
            not_null.append(root.children[i])
    if len(not_null) == 0:
        return True
    if root.parent and len(not_null) == 1:
        # if there's only one non-null children, prune
        node = not_null.pop()
        root.parent.set_ith_child(node, root.child_pos)
    return False
