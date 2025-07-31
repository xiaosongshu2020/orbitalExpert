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
# 创建虚拟环境, 进入虚拟环境
...

# 安装依赖
pip install -r 'requirements.txt'
```

### 3. 安装npx
项目中的部分MCP服务需要借助npx安装到本地，访问 Node.js官网 (https://nodejs.org/) 下载 LTS（长期支持版） 并安装, 安装时默认会包含 npm 和 npx.

### 4. 安装mcp-server-satellite-orbit

这是一个开源的MCP服务器（作者将卫星轨道工具打包为MCP服务，作为一个独立的开源项目），用于卫星轨道计算：

```bash
# 克隆仓库
git clone https://github.com/xiaosongshu2020/mcp-server-satellite-orbit.git

# 进入目录
cd mcp-server-satellite-orbit

```

安装MCP, 参考该项目的README.md. 

### 5. 配置MCP服务器路径

请相应地修改`src/orbitalExpert.py`文件中的路径设置部分：

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
