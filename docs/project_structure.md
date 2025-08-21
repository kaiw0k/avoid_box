# 项目目录结构

```
young_saint_of_war/
├── assets/          # 游戏资源目录
│   ├── fonts/      # 字体文件
│   ├── images/     # 图片资源
│   └── sounds/     # 音效和音乐文件
├── docs/           # 项目文档
│   └── project_structure.md  # 项目结构说明文档
├── src/            # 源代码目录
│   └── game/       # 主游戏包
│       ├── __init__.py
│       ├── core/   # 核心游戏逻辑
│       │   └── __init__.py
│       ├── entities/# 游戏实体
│       │   └── __init__.py
│       └── utils/  # 工具函数
│           └── __init__.py
├── tests/          # 测试文件夹
└── requirements.txt # 项目依赖文件

## 目录说明

- `assets/`: 存储所有游戏资源文件
  - `fonts/`: 游戏中使用的字体文件
  - `images/`: 游戏图片、精灵图和纹理等
  - `sounds/`: 游戏音效和背景音乐
- `docs/`: 项目文档，包含设计文档、API文档等
- `src/game/`: 游戏源代码
  - `core/`: 核心游戏逻辑，如游戏循环、状态管理等
  - `entities/`: 游戏实体类，如玩家、敌人、道具等
  - `utils/`: 工具函数和辅助类
- `tests/`: 单元测试和集成测试
- `requirements.txt`: Python项目依赖清单
