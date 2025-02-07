import subprocess
import sys
from core.code_execution.setup_docker import image_tag_map

def run_code(language, code):
    image_tag = image_tag_map[language]

    output = None

    if language == "Python":
        output = run_python(code, image_tag)
    else:
        print("Error: Unsupported language to execute")
        sys.exit(1)

    return output

# 注意捕获编译错误和运行时错误

# executors for all languages

def run_python(code, image):
    try:
        # 使用 docker run 命令启动容器并执行 Python 代码
        result = subprocess.run(
            ["docker", "run", "--rm", "-i", image, "python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=20  # 设置超时，可以根据需要调整
        )

        # 检查执行结果并返回
        if result.returncode == 0:
            return result.stdout  # 返回标准输出
        else:
            return f"Error: {result.stderr}"  # 返回错误信息

    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out."
    except Exception as e:
        return f"Error running Python code in Docker: {e}"

    except subprocess.TimeoutExpired:
        print("Error: Code execution timed out.")
    except Exception as e:
        print(f"Error running Python code in Docker: {e}")