#!/usr/bin/env python3
"""
个人理财助手启动脚本
"""

import subprocess
import sys
import os

def main():
    """启动Streamlit应用"""
    try:
        # 检查是否安装了依赖
        print("🚀 启动个人理财助手...")
        
        # 切换到项目目录
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
