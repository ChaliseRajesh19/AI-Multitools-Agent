"""Safe math expression evaluator for the calculator tool."""
import ast
import operator

def calculator(expression):
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }
    try:
        node = ast.parse(expression, mode='eval')
        return eval_node(node.body, allowed_operators)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def eval_node(node, allowed_operators):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        left = eval_node(node.left, allowed_operators)
        right = eval_node(node.right, allowed_operators)
        op = allowed_operators.get(type(node.op))
        if op:
            return op(left, right)
        else:
            raise ValueError(f"Unsupported operation: {type(node.op)}")
    else:
        raise ValueError(f"Unsupported node type: {type(node)}")