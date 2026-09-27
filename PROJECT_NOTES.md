# 大肥鱼桌宠 - 项目记录
## 任务与决策
1. 文字截断修复
   - 新增 _wrap_bubble_text() 方法，正确处理 \n 和像素宽度
   - 移除 80 字符硬截断，由气泡分片系统处理长文本

2. 气泡防打断机制（2026-08-30）
   - say() 增加 force 参数
   - 气泡显示期间（未过期），非 force=True 的消息自动跳过
   - AI 回复、错误提示、用户交互用 force=True
   - 随机内心独白、天气、知识分享不用 force（不打断）

3. 气泡最小停留时间（2026-08-30）
   - 每个气泡最低 1 秒
   - 单片默认 2 秒，队列后续片也是 2 秒
   - 使用 hold = max(hold, 1.0) 确保下限

4. 配置项名修复（2026-08-30）
   - 原代码 cfg["size"] 与 config.json 的 window_size_multiplier 不匹配
   - 改为 cfg.get("window_size_multiplier", 0.9) 兼容读取
   - 写入时同步改为 window_size_multiplier

5. load_json 默认值合并修复（2026-08-30）
   - 原 load_json 直接返回 json.load(f)，不合并默认值
   - 导致 config.json 缺失的键（mode、size、topmost 等）报错 KeyError
   - 修复：加载后遍历 default.items()，缺失的键自动补全

6. 功能按钮横排（2026-08-30）
   - _Menu 面板从 QVBoxLayout 改为 QHBoxLayout
   - 三个按钮 🗨️💻👀 横排显示，尺寸 164x68

7. 本地 Ollama 兜底链路移除（2026-09-27）
   - 所有模型调用只走在线 Agnes API，统一入口 _agnes_chat()
   - 删除本地调度/故障切换/断网探测/模型卸载等逻辑与相关配置项
   - 无网或接口失败时直接气泡提示，不再切换本地模型
   - 人设提示词常量 OLLAMA_SYSTEM 更名为 PET_SYSTEM

## 关键文件
- `d:\dafeiyu-pet-main\pet.py` - 主程序
- `d:\dafeiyu-pet-main\config.json` - 配置
- `d:\dafeiyu-pet-main\启动桌宠.bat` - 启动脚本