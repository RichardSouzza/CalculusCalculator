from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from sympy import diff, integrate, symbols, sympify
from sympy.core.sympify import SympifyError
from string import digits
from typing import Callable


class CalculatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CalculatorScreen, self).__init__(**kwargs)
        self.variables = ["x", "y"]
        self.constants = ["π", "e"]
        self.operators = ["+", "-", "×", "÷", "^"]
        self.special_operators = ["sqrt", "sin", "cos", "tan"]
        self._translation_table = None
        self._reverse_translation_table = None
    
    def calculate(self, method: Callable) -> None:
        function = self.formatter(self.ids.display.text)
        result = method(function)
        if type(result) == SympifyError:
            error_message = self.formatter(result.expr, reverse=True).capitalize()
            toast(error_message)
        else:
            result = self.formatter(result, reverse=True)
            self.show_result(result)
    
    def clear_display(self) -> None:
        self.ids.display.text = " "
    
    def del_last_value(self):
        display = self.ids.display.text[:-1]
        if len(display) == 0:
            display = " "
        self.ids.display.text = display

    @staticmethod
    def derivate(function: str) -> str:
        x, y = symbols("x y")
        try:
            function = sympify(function)
            derivative = str(diff(function, x))
            return derivative
        except Exception as error:
            return error
    
    @staticmethod
    def integrate(function: str) -> str:
        x, y = symbols("x y")
        try:
            function = sympify(function)
            derivative = str(integrate(function, x))
            return derivative
        except Exception as error:
            return error
    
    def formatter(self, function: str, reverse: bool = False) -> str:
        if not reverse:
            table = self.translation_table
            left_parenthesis = function.count("(")
            right_parenthesis = function.count(")")
            if left_parenthesis > right_parenthesis:
                function += ")" * (left_parenthesis - right_parenthesis)
            function = function.replace("[color=#0D47A1]", "").replace("[/color]", "")
        else:
            table = self.reverse_translation_table
        for key, value in table.items():
            function = function.replace(key, value)
        return function

    def insert_value(self, value: str) -> None:
        display = self.ids.display.text
        last_value = display[-1]
        last_point_index = display.rfind(".")
        last_operator_index = -1
        
        if value == ".":
            for operator in self.operators:
                operator_index = display.rfind(operator)
                if operator_index > last_operator_index:
                    last_operator_index = operator_index
            if last_point_index > last_operator_index:
                return

        if value in self.operators:
            if last_value in self.operators:
                display = self.ids.display.text[:-1]
        
        if value == "( )":
            if last_value in [" ", "("] + self.operators:
                value += "("
            elif ("(" in display and last_value not in self.operators and
                    display.count("(") > display.count(")")):
                value= ")"
            else:
                value = "×("
        
        display += value
        self.ids.display.text = self.markup(display)

    def markup(self, display: str) -> str:
        for operator in self.operators:
            display = display.replace(operator, f"[color=#0D47A1]{operator}[/color]")
        return display

    def show_result(self, result: str) -> None:
        self.ids.display.text = result
    
    @property
    def translation_table(self) -> dict:
        if self._translation_table ==  None:
            table = {"×": "*", "÷": "/", "^": "**"}
            for term in self.variables + self.constants:
                for digit in digits:
                    table.update({f"{digit}{term}": f"{digit}*{term}"})
                    for operator in self.special_operators:
                        table.update({f"{term}{operator}": f"{term}*{operator}"})
                        table.update({f"{digit}{operator}": f"{digit}*{operator}"})
            for variable in self.variables:
                for constant in self.constants:
                    table.update({f"{variable}{constant}": f"{variable}*{constant}"})
                    table.update({f"{constant}{variable}": f"{constant}*{variable}"})
            self._translation_table = table
        return self._translation_table

    @property
    def reverse_translation_table(self) -> dict:
        if self._reverse_translation_table == None:
            table = {"*": "×", "/": "÷", "××": "^"}
            for term in self.variables + self.constants:
                for digit in digits:
                    table.update({f"{digit}×{term}": f"{digit}{term}"})
            self._reverse_translation_table = table
        return self._reverse_translation_table
