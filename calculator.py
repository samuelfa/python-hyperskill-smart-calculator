# write your code here
from string import ascii_letters
from collections import deque


class Terminate(Exception):
    pass


class UnknownCommand(Exception):
    pass


class InvalidIdentifier(Exception):
    pass


class InvalidAssignment(Exception):
    pass


class UnknownVariable(Exception):
    pass


class Calculator:
    def __init__(self):
        self.dictionary = {}
        self.operators = ['+', '-', '*', '/', '^']
        self.operators_priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 4, ')': 4}
        self.parenthesis = ['(', ')']

    @staticmethod
    def run_command(option):
        if option == '/help':
            print('The program calculates the sum or sub of numbers')
            return

        if option == '/exit':
            raise Terminate()

        raise UnknownCommand()

    def action(self):
        option = input().strip()
        if option == '':
            return

        if option.startswith('/'):
            self.run_command(option)
            return

        if "=" in option:
            self.store_variable(option)
            return

        self.execute_operation(option)

    def transform_infix_to_postfix(self, numbers):
        stack = deque()
        result = []

        for char in numbers:

            if char not in self.operators \
                    and char not in self.parenthesis:
                result.append(char)
                if len(stack) > 0 and stack[-1] != '(':
                    old_top = stack.pop()
                    if old_top != '(':
                        result.append(old_top)

            elif char == ')':
                if len(stack) == 0:
                    raise ValueError

                while len(stack) > 0:
                    old_top = stack.pop()
                    if old_top == '(':
                        break
                    result.append(old_top)

            elif len(stack) == 0 \
                    or stack[-1] == '(' \
                    or char == '(':
                stack.append(char)

            else:
                top = stack[-1]
                char_priority = self.operators_priority[char]
                top_priority = self.operators_priority[top]
                if char_priority > top_priority:
                    stack.append(char)
                else:
                    while char_priority <= top_priority \
                            and top != '(' \
                            and len(stack) > 0:

                        old_top = stack.pop()
                        result.append(old_top)

                        if old_top == ')' or \
                                len(stack) == 0:
                            continue

                        top = stack[-1]
                        top_priority = self.operators_priority[top]

                    stack.append(char)

        while len(stack) > 0:
            old_top = stack.pop()
            if old_top in self.parenthesis:
                raise ValueError
            result.append(old_top)

        return result

    @staticmethod
    def operation(number1, number2, operation):
        if operation == '+':
            return number1 + number2
        elif operation == '-':
            return number1 - number2
        elif operation == '*':
            return number1 * number2
        elif operation == '/':
            return number1 / number2
        elif operation == '^':
            return number1 ** number2
        else:
            raise SyntaxError

    def execute_operation(self, option):
        for operator in self.operators:
            option = self.prepare_operator(option, operator)
        for operator in self.parenthesis:
            option = self.prepare_operator(option, operator)

        self.simplify_duplicate_operators(option, '+', '+')
        self.simplify_duplicate_operators(option, '-', '+')

        numbers = option.split()

        numbers = self.transform_infix_to_postfix(numbers)

        stack = deque()

        for char in numbers:

            if char not in self.operators and char not in self.parenthesis:
                number = self.variable_value(char)
                stack.append(number)

            elif char in self.operators:
                number2 = stack.pop()
                if len(stack) == 0:
                    raise ValueError
                
                number1 = stack.pop()
                number_result = self.operation(number1, number2, char)
                stack.append(number_result)

        print(int(stack.pop()))

    def variable_value(self, variable):
        if variable.isnumeric():
            return int(variable)

        if not self.is_valid_identifier(variable):
            raise InvalidAssignment

        if variable not in self.dictionary:
            raise UnknownVariable

        return self.dictionary[variable]

    @staticmethod
    def simplify_duplicate_operators(option, operator, pair_operator):
        duplicates = []
        elements = option.split()
        final_list = []
        for element in elements:
            if element == operator:
                duplicates.append(element)
            else:
                if len(duplicates) > 0:
                    if len(duplicates) % 2 == 0:
                        final_list.append(pair_operator)
                    else:
                        final_list.append(operator)
                    duplicates = []

                final_list.append(element)

        return ' '.join(final_list)

    @staticmethod
    def prepare_operator(option, operator):
        option = option.replace(operator, f' {operator} ')
        while option.find(' ' * 2) != -1:
            option = option.replace(' ' * 2, ' ')

        return option

    def store_variable(self, option):
        option = option.replace(' ', '')
        if option.count("=") != 1:
            raise InvalidAssignment

        variable, value = option.split("=")
        if not self.is_valid_identifier(variable):
            raise InvalidIdentifier()

        self.dictionary[variable] = self.variable_value(value)

    @staticmethod
    def is_valid_identifier(variable):
        for letter in variable:
            if letter not in ascii_letters:
                return False
        return True

    def run(self):
        while True:
            try:
                self.action()
            except Terminate:
                print('Bye!')
                break
            except UnknownCommand:
                print("Unknown command")
            except ValueError:
                print("Invalid expression")
            except InvalidIdentifier:
                print("Invalid identifier")
            except InvalidAssignment:
                print("Invalid assigment")
            except UnknownVariable:
                print('Unknown variable')


calculator = Calculator()
calculator.run()
