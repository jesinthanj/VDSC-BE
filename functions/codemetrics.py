import re

def calculate_code_metrics(code):
    metrics = {}

    metrics["empty_lines"] = len(re.findall(r'^\s*$', code, re.MULTILINE))
    metrics["lines_of_comments"] = len(re.findall(r'\/\/.*|\/\*(.|\n)*?\*\/', code))
    metrics["lines_of_program"] = len(re.findall(r'^(?!(\s*\/\/|\s*\/\*)).*$', code, re.MULTILINE))
    metrics["physical_lines"] = len(re.findall(r'.+', code))

    operators = re.findall(r'[+\-*/%=><!&|^~?:]', code)
    metrics["distinct_operators"] = len(set(operators))

    operands = re.findall(r'\b(?!(if|else|for|while|do|switch|case|int|float|char|void)\b)\w+\b', code)
    metrics["distinct_operands"] = len(set(operands))

    metrics["program_vocabulary"] = metrics["distinct_operators"] + metrics["distinct_operands"]

    metrics["total_operators"] = len(operators)
    metrics["total_operands"] = len(operands)

    metrics["program_length"] = metrics["total_operators"] + metrics["total_operands"]

    return metrics

# Example usage
# c_code = """#include <stdio.h>

# int main() {
#     int a = 5;
#     int b = 10;
#     int sum = a + b;
#     printf("Sum: %d", sum);
#     return 0;
# }"""

# result = calculate_code_metrics(c_code)
# print(result)
