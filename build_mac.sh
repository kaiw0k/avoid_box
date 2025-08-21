#!/bin/bash
# 自动打包 Python 游戏为 macOS 独立可执行文件
# 使用 PyInstaller，包含资源文件

set -e

# 1. 安装依赖
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# 2. 检查 PyInstaller 是否安装
if ! command -v pyinstaller &> /dev/null; then
    pip install pyinstaller
fi

# 3. 设置资源文件参数（如有 assets 文件夹）
ADD_DATA=""
if [ -d "assets" ]; then
    ADD_DATA="--add-data assets:assets"
fi

# 4. 设置图标（如有 assets/images/icon.icns）
ICON_ARG=""
if [ -f "assets/images/icon.icns" ]; then
    ICON_ARG="--icon=assets/images/icon.icns"
fi

# 5. 执行打包
pyinstaller --onefile --windowed ${ADD_DATA} ${ICON_ARG} src/main.py

# 6. 打包结果提示
if [ -f dist/main ]; then
    echo "打包成功！可执行文件在 dist/main"
else
    echo "打包失败，请检查错误信息。"
fi

# 7. macOS 权限和隔离处理
chmod +x dist/main || true
xattr -d com.apple.quarantine dist/main || true

echo "如需 .app 格式，可用 pyinstaller --windowed src/main.py 或用 Automator 创建应用包。"
