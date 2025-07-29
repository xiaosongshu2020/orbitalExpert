# 轨道专家 AI 助手

这是一个专业的航天器轨道力学专家AI助手，代号"小松鼠"。

## 功能特性

- 卫星轨道计算
- 文件操作和数据处理
- 与其他工具集成进行复杂任务处理

## 环境配置

### API密钥设置

本项目支持两种大语言模型：DeepSeek和Qwen。您需要根据选择的模型设置相应的API密钥。

#### 使用DeepSeek模型（默认）

1. 设置`DEEPSEEK_API_KEY`环境变量（推荐）

##### Windows (命令提示符)
```cmd
set DEEPSEEK_API_KEY=your_api_key_here
```

##### Windows (PowerShell)
```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

##### Linux/macOS
```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

2. 直接运行程序时手动输入API密钥（程序会提示您输入）

#### 使用Qwen模型

1. 设置`QWEN_API_KEY`环境变量（推荐）

##### Windows (命令提示符)
```cmd
set QWEN_API_KEY=your_api_key_here
```

##### Windows (PowerShell)
```powershell
$env:QWEN_API_KEY="your_api_key_here"
```

##### Linux/macOS
```bash
export QWEN_API_KEY=your_api_key_here
```

2. 直接运行程序时手动输入API密钥（程序会提示您输入）

注意：如果未设置环境变量，程序会在首次运行时提示您输入API密钥，并将其保存在当前会话中，避免重复输入。

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python src/orbitExpert_mcp.py
```

### 模型选择

默认情况下，程序使用DeepSeek模型。如果您想使用Qwen模型，可以通过设置`MODEL_TYPE`环境变量来切换：

#### Windows (命令提示符)
```cmd
set MODEL_TYPE=qwen
python src/orbitExpert_mcp.py
```

#### Windows (PowerShell)
```powershell
$env:MODEL_TYPE="qwen"
python src/orbitExpert_mcp.py
```

#### Linux/macOS
```bash
export MODEL_TYPE=qwen
python src/orbitExpert_mcp.py
```

要使用DeepSeek模型，可以设置`MODEL_TYPE=deepseek`，或者不设置该环境变量（默认即为deepseek）。

## 注意事项

- 生成的数据默认保存在`./files/`目录中
- 调用工具时，文件名必须使用绝对路径
