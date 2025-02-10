import subprocess
import sys

def run_code(language, code):
    if language == "Python":
        output = run_python(code)
    else:
        print("Error: Unsupported language to execute")
        return None

    return output

def run_python(code):
    return "Test"