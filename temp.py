import subprocess
import os

def run_command(command):
    """运行命令并返回输出，错误时抛出异常"""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"命令执行出错: {' '.join(e.cmd)}")
        print(e.stderr.decode('utf-8'))
        raise

# 仓库的 URL
repo_url = "https://github.com/oceanbase/oceanbase-doc"

# 克隆到的目录名
repo_name = "oceanbase-doc"

# 尝试克隆整个仓库的默认分支
try:
    run_command(["git", "clone", repo_url])
except Exception as e:
    print(f"无法克隆仓库: {repo_url}")
    exit(1)

# 获取所有分支
try:
    branches_output = run_command(["git", "-C", repo_name, "branch", "-r"])
except Exception as e:
    print("无法获取分支列表")
    exit(1)

# 提取分支名称
branches = [
    branch.strip().split("/")[1]
    for branch in branches_output.strip().split("\n")
    if "->" not in branch and branch.strip()
]

# 克隆每个分支
for branch in branches:
    # 创建目标目录
    target_dir = f"{repo_name}-{branch}"
    os.makedirs(target_dir, exist_ok=True)
    
    # 克隆特定分支
    try:
        run_command(["git", "clone", "-b", branch, repo_url, target_dir])
        print(f"分支 {branch} 已克隆到 {target_dir}")
    except Exception as e:
        print(f"分支 {branch} 克隆失败")
