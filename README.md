# 大肥鱼桌宠 🐋

> 一个可爱的桌面宠物，DeepSeek V4 Pro 二创形象「鲸鱼娘·大肥鱼」的透明桌面陪伴。

基于三视图素材（正面 / 侧面 / 背面），用 Python + PySide6 实现，无边框透明置顶窗口。

## ✨ 功能特点

- **三视图行走**：左右走用侧面（自动镜像）、向上走用背面、向下走用正面
- **三种模式**：自由散步 / 跟随鼠标 / 原地待着（右键菜单切换）
- **丰富的互动**：
  - 左键按住拖拽：侧身朝向拖动方向，松手会说话
  - 单击：蹦跳 + 回嘴互动台词 + 弹出聊天面板
  - 双击：喂食面板（小鱼干 / 蛋糕 / 棒棒糖 / 团子 / 钻石）
  - 右键：完整菜单（模式 / 大小 / 喂食 / 说句话 / 显示/隐藏 / 鼠标穿透 / 置顶 / 开机自启 / 退出）
- **台词系统**：日常随机台词 + 互动回嘴 + 思维链心声，全部取材自社区 DeepSeek 梗
- **动画细节**：呼吸 / 摇摆 / 蹦跳 / 进食动画、转向交叉淡化、加减速惯性、散步自动休息

## 🤖 AI 对话

- 点击 🗨️ 图标弹出聊天输入框
- 调用 DeepSeek API（`deepseek-chat` 模型）
- 每句话不超过 25 字，风格贱兮兮但可爱
- 对话历史保留最近 40 条上下文

## 🌤️ 天气查询

- 右键菜单「查看天气」→ 调用 `wttr.in` 获取当前城市天气
- 鱼会气泡播报：「汕头今天 26°，天气多云」

## 📦 运行方式

### 方式一：便携版（推荐）

直接下载 release 或复制本仓库，双击 `启动桌宠.bat` 即可运行。
**无需安装 Python**，runtime 已内置。

### 方式二：源码运行

```bash
git clone https://github.com/z4cp8pxqzj-hash/dsh---dsh-.git
cd dsh---dsh-
pip install -r requirements.txt
python pet.py
```

需要 **Python 3.10+** 和 PySide6。

### 方式三：打包成 exe

```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name 大肥鱼桌宠 --add-data "sprites;sprites" --icon sprites/icon.png pet.py
```

产物在 `dist/大肥鱼桌宠.exe`，对方双击即用。

## 🎨 更换形象

把新的三视图（白底）放到程序目录，然后运行预处理脚本：

1. 准备正面.png / 侧面.png / 背面.png
2. 运行 `python preprocess.py` —— 白底抠图 + 统一高度
3. 运行 `python preprocess2.py` —— 边缘去污 + 预乘 alpha 缩放出各尺寸精灵

## 📂 项目结构

| 文件/目录 | 说明 |
|-----------|------|
| `pet.py` | 主程序（全部逻辑） |
| `secure_key.py` | API Key 加密工具 |
| `preprocess.py` | 白底三视图抠图脚本 |
| `preprocess2.py` | 精灵边缘去污 + 多尺寸生成 |
| `sprites/` | 精灵图（正面/侧面/背面 各尺寸 + 图标） |
| `start.bat` | 启动脚本 |
| `启动桌宠.bat` | Windows 启动脚本 |
| `runtime/` | 便携 Python 环境（Git LFS） |
| `config.json` | 本地配置（不入仓库） |
| `LICENSE` | MIT 协议 |

## ⚠️ 注意事项

- `config.json` 含 API Key，**不要提交到仓库**
- 杀毒软件可能对 PyInstaller 产物误报，加信任即可
- 首次运行需要在设置中输入 DeepSeek API Key

## 🙏 致谢

- 原始桌宠项目：[dafeiyu-pet](https://github.com/1190fasheqi/dafeiyu-pet)
- AI 对话 / 天气查询功能由社区贡献
- 台词梗来源：DeepSeek / 鲸鱼娘 / 大肥鱼社区整活

## 📄 协议

MIT License - 可自由使用、修改、分发，保留版权声明即可。
