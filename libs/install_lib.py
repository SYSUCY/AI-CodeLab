import importlib
import subprocess
import sys
from typing import Optional

def is_package_installed(package_name: str) -> bool:
    """
    检查指定包是否已安装

    Args:
        package_name (str): 要检查的包名

    Returns:
        bool: 如果包已安装返回 True，否则返回 False
    """
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        print(f"package {package_name} not installed")
        return False


def install_package(package_name: str, version: Optional[str] = None) -> bool:
    """
    安装指定的 Python 包

    Args:
        package_name (str): 要安装的包名
        version (Optional[str]): 指定版本号，默认为最新版

    Returns:
        bool: 安装成功返回 True，失败返回 False
    """
    print(f"installing package {package_name}")

    install_cmd = [sys.executable, "-m", "pip", "install"]
    if version:
        package_spec = f"{package_name}=={version}"
    else:
        package_spec = package_name

    install_cmd.append(package_spec)

    try:
        subprocess.check_call(install_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"package {package_name} successfully installed")
        return True
    except subprocess.CalledProcessError:
        print(f"package {package_name} not installed successfully")
        return False
