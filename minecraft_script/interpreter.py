from .text_additions import text_error, text_underline


class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_node)
        return method(node)

    def visit_NumberNode(self, node) -> int:
        return node.get_value()

    def visit_BinaryOperationNode(self, node) -> int:
        operator = node.operator.value
        left_expression = self.visit(node.left_node)
        right_expression = self.visit(node.right_node)
        result = 0

        if operator == '+':
            result = left_expression + right_expression
        elif operator == '-':
            result = left_expression - right_expression
        elif operator == '*':
            result = left_expression * right_expression
        elif operator == '/':
            result = left_expression // right_expression
        elif operator == '%':
            result = left_expression % right_expression

        return result

    def visit_UnaryOperationNode(self, node):
        print('Unary node')

    def no_visit_node(self, node):
        print(text_error(f'No visit method defined for {text_underline(type(node).__name__)}'))

if __name__ == '__main__':
    Interpreter()
