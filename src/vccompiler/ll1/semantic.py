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
                operand_set.append((node, pos))
                if child.precedence == root.precedence:
                    new_operand_set = []
                    operators.append((child, new_operand_set))
                    dfs(child, new_operand_set)
                else:
                    descendants.append(child)
            else:
                dfs(child, operand_set)

    initial_operand_set = []
    operators.append((root, initial_operand_set))
    dfs(root, initial_operand_set)

    # left associative
    stack = []
    stack.extend(descendants[::-1])
    for op, operand_set in operators:
        for node, pos in operand_set:
            node.set_ith_child(stack.pop(), pos)
        stack.append(op)

    assert len(stack) == 1

    for child in descendants:
        parent = child.parent
        child_pos = child.child_pos
        parent.set_ith_child(left_to_right(child, precedences), child_pos)

    return stack.pop()


def cst_pruning(root):
    if isinstance(root.rule, str):
        return root.rule == ""
    if isinstance(root.rule, Token):
        return False
    not_null = []
    for i in range(len(root.children)):
        if not cst_pruning(root.children[i]):
            not_null.append(root.children[i])
    if len(not_null) == 0:
        return True
    if root.parent and len(not_null) == 1:
        node = not_null.pop()
        root.parent.set_ith_child(node, root.child_pos)
    return False
