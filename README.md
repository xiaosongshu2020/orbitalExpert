# 轨道专家 AI 助手

这是一个专业的航天器轨道力学专家AI助手，代号"小松鼠"。

## 功能特性

- 卫星轨道计算
- 文件操作和数据处理
- 与其他工具集成进行复杂任务处理

## 本地运行指南

### 1. 配置大语言模型API密钥

项目默认使用Qwen模型，您需要配置相应的API密钥。

#### Qwen API密钥配置

1. 访问[阿里云DashScope](https://dashscope.console.aliyun.com/)申请API密钥
2. 获取API密钥后，设置环境变量：

##### Windows (命令提示符)
```cmd
set QWEN_API_KEY=your_qwen_api_key_here
```

##### Windows (PowerShell)
```powershell
$env:QWEN_API_KEY="your_qwen_api_key_here"
```

##### Linux/macOS
```bash
export QWEN_API_KEY=your_qwen_api_key_here
```

#### 使用其他大语言模型

如果您想使用其他大语言模型，请修改`src/orbitalExpert.py`文件中的相应代码：

1. 注释掉Qwen相关的代码块
2. 取消注释并配置您选择的模型代码块（如DeepSeek）
3. 根据所选模型设置相应的API密钥环境变量

### 2. 创建虚拟环境并安装依赖

建议使用虚拟环境来隔离项目依赖：

```bash
# 创建虚拟环境
python -m venv orbitExpert-env

# 激活虚拟环境
# Windows (命令提示符)
orbitExpert-env\Scripts\activate
# Windows (PowerShell)
orbitExpert-env\Scripts\Activate.ps1
# Linux/macOS
source orbitExpert-env/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 安装uv工具

uv是一个极快的Python包和项目管理器。我们需要它来运行MCP服务：

```bash
# 使用pip安装uv
pip install uv
```

### 4. 安装mcp-server-satellite-orbit

这是一个开源的MCP服务器（作者将卫星轨道工具打包为MCP服务，作为一个独立的开源项目），用于卫星轨道计算：

```bash
# 克隆仓库
git clone https://github.com/xiaosongshu2020/mcp-server-satellite-orbit.git

# 进入目录
cd mcp-server-satellite-orbit

# 安装依赖
uv sync
```

### 5. 配置MCP服务器路径

项目现在会自动设置路径，无需手动修改。默认情况下，程序会假设mcp-server-satellite-orbit与orbitExpert项目在同一父目录下。

如果您将mcp-server-satellite-orbit克隆到了其他位置，请相应地修改`src/orbitalExpert.py`文件中的路径设置部分：

```python
"mcp-server-satOrbit": {
    "command": "uv",
    "args": [
        "--directory",
        "D:/home/projects/mcp-server-satellite-orbit/",  # 修改为您实际的路径
        "run",
        "run_server.py"
    ],
    "transport": "stdio"
},
```

### 6. 运行项目

确保您已激活虚拟环境并设置好API密钥，然后运行：

```bash
python src/orbitalExpert.py
```

## 注意事项

- 生成的数据默认保存在`./files/`目录中
- 调用工具时，文件名必须使用绝对路径
- 如果您修改了代码以使用其他大语言模型，请确保相应地设置环境变量
- 项目会自动创建所需的目录（如data和files目录）
- 默认情况下，程序会自动设置所有必要的路径，无需手动修改
