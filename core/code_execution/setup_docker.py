import subprocess
import platform
import os
import sys
from core.code_execution.load_config import load_config

image_map = {
    'Python': 'python:3.10-slim'
}

image_tag_map = {
    'Python': 'python-executor',
}

# 检测操作系统
def get_system():
    return platform.system().lower() # windows / ubuntu

# 检查 Docker 是否安装
def is_docker_installed():
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            # print("Docker is already installed")
            return True
        else:
            print("Docker is not installed")
            return False
    except FileNotFoundError:
        print("Docker is not installed")
        return False

# Windows系统下，提示用户安装 Docker Desktop
def prompt_for_docker_in_windows():
    print("Docker尚未安装，请安装Docker Desktop")

# Ubuntu 系统自动安装 Docker
def install_docker_ubuntu():
    try:
        print("Installing Docker on Ubuntu...")
        # 更新 apt 包索引
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        # 安装 Docker 所需的包
        subprocess.run(["sudo", "apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl",
                        "software-properties-common"], check=True)
        # 添加 Docker 官方的 GPG 密钥
        subprocess.run(
            ["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "|", "sudo", "gpg", "--dearmor", "-o",
             "/usr/share/keyrings/docker-archive-keyring.gpg"], check=True)
        # 添加 Docker 仓库
        subprocess.run(["echo",
                        "'deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable'",
                        "|", "sudo", "tee", "/etc/apt/sources.list.d/docker.list"], check=True)
        # 安装 Docker CE
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce"], check=True)
        print("Docker installed successfully on Ubuntu.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Docker on Ubuntu: {e}")
        sys.exit(1)

# 检查镜像是否已经存在
def check_image_exists(image):
    try:
        # 使用 `docker images` 命令检查是否已构建该镜像
        result = subprocess.run(
            ["docker", "images", "-q", image],
            capture_output=True,
            text=True
        )
        is_exist = bool(result.stdout.strip())
        if not is_exist:
            print(f"Docker image {image} not found.")
        # else:
        #     print(f"Docker image {image} already exists")
        return is_exist  # 如果返回非空，说明镜像存在
    except subprocess.CalledProcessError as e:
        print(f"Error checking if image exists: {e}")
        return False

def pull_base_image(image):
    try:
        print(f"Pulling base image {image}...")

        # 拉取镜像
        subprocess.run(
            ["docker", "pull", image],
            check=True
        )
        print(f"Base image {image} pulled successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error pulling or tagging base image {image}: {e}")

def set_image_tag(image, tag):
    try:
        # 使用 docker tag 命令为镜像添加新标签
        subprocess.run(
            ["docker", "tag", image, tag],
            check=True
        )
        print(f"Image {image} has been tagged as {tag}.")
    except subprocess.CalledProcessError as e:
        print(f"Error tagging image {image}: {e}")


def setup_docker():
    system = get_system()

    if not system == "windows" or system == "linux":
        print("Error: Unsupported system")
        sys.exit(1)

    if is_docker_installed():
        # 获取base镜像
        config = load_config("./core/code_execution/config.yaml")
        if config:
            url = config['docker']['url']
        else:
            print("Error loading config.yaml")
            sys.exit(1)

        if url:
            for language, image in image_map.items():
                if not check_image_exists(f"{url}/{image}"):
                    pull_base_image(f"{url}/{image}")
                    set_image_tag(f"{url}/{image}", image_tag_map[language])
        else:
            for language, image in image_map.items():
                if not check_image_exists(image):
                    pull_base_image(image)
                    set_image_tag(image, image_tag_map[language])

    else:
        # 没有安装 Docker
        if system == "windows":
            prompt_for_docker_in_windows()
        elif system == "linux":
            install_docker_ubuntu()