from .text_additions import text_error, text_underline
from .types import Number


class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_node)
        return method(node)

    def visit_NumberNode(self, node) -> int:
        return node.get_value()

    def visit_BinaryOperationNode(self, node) -> int:
        operator = node.operator.value
        left_expression = Number(self.visit(node.left_node))
        right_expression = Number(self.visit(node.right_node))
        result = 0

        if operator == '+':
            result = left_expression.add(right_expression)
        elif operator == '-':
            result = left_expression.subtract(right_expression)
        elif operator == '*':
            result = left_expression.multiply(right_expression)
        elif operator == '/':
            result = left_expression.divide(right_expression)
        elif operator == '%':
            result = left_expression.modulus(right_expression)

        return result

    def visit_UnaryOperationNode(self, node) -> int:
        operator = node.operator.value
        right_node = Number(self.visit(node.right_node))
        result = 0

        if operator == '+':
            result = Number(0).add(right_node)
        elif operator == '-':
            result = Number(0).subtract(right_node)

        return result

    def no_visit_node(self, node):
        print(text_error(f'No visit method defined for {text_underline(type(node).__name__)}'))

if __name__ == '__main__':
    Interpreter()
