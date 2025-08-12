from typing import Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from typing_extensions import TypedDict
from typing import TypedDict, Annotated, List, Union, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os
from pathlib import Path
from datetime import datetime
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

# 从环境变量获取API密钥
QWEN_API_KEY = os.environ.get("QWEN_API_KEY")

# 如果环境变量中没有设置API密钥，则提示用户手动输入
if not QWEN_API_KEY:
    print("警告: 未设置QWEN_API_KEY环境变量")
    QWEN_API_KEY = input("请输入您的Qwen API密钥: ").strip()
    # 设置环境变量
    os.environ["QWEN_API_KEY"] = QWEN_API_KEY

# 采用ChatOpenAI调用示例
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="qwen3-coder-plus",
    openai_api_key=QWEN_API_KEY,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0
)

# 获取当前时间
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
# 获取documents目录（用户主目录下的Documents文件夹）
DOCUMENTS_DIR = Path.home() / "Documents"
# 确保必要的目录存在
FILES_DIR = PROJECT_ROOT / "files"
FILES_DIR.mkdir(exist_ok=True)

# 系统提示词
SYSTEM_PROMPT = f"""你是一个专业的航天器轨道力学专家AI助手，你的名字叫'小松鼠'。

当前时间：{current_time}
项目路径：{PROJECT_ROOT}

请遵循以下原则：
1. 优先借用工具来完成任务，如果工具不适用，再考虑手动计算；
2. 如果你不确定某个问题的答案，请诚实地告诉用户；
3. 生成的数据默认保存在'./files/'里；
4. 调用工具时，文件名必须使用绝对路径；
5. 请先给出思考过程，再调用工具或回答；
"""

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize async components
async def initialize_tools():
    """异步初始化工具"""
    client = MultiServerMCPClient(
        {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    str(PROJECT_ROOT),
                    str(DOCUMENTS_DIR)
                ],
                "transport": "stdio"
            },

            "memory": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-memory"
                ],
                "env": {
                    "MEMORY_FILE_PATH": str(FILES_DIR / "memory.json")
                },
                "transport": "stdio"
            },

            "sequential-thinking": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-sequential-thinking"
                ],
                "transport": "stdio" 
            },

            "mcp-server-satOrbit": {
                "command": "uv",
                "args": [
                    "--directory",
                    "D:/projects_d/mcp-server-satellite-orbit/",
                    "run",
                    "run_server.py"
                ],
                "transport": "stdio"
            },
        }
    )

    # Get MCP tools
    tools_mcp = await client.get_tools()

    # Properly combine tools into a flat list
    tools = []

    # Handle the case where tools_mcp might be a single tool or a list of tools
    if isinstance(tools_mcp, list):
        tools.extend(tools_mcp)
    else:
        tools.append(tools_mcp)

    # Print tool information
    print(f"Total tools loaded: {len(tools)}")
    for i, tool in enumerate(tools):
        if hasattr(tool, 'name'):
            print(f"  {i+1}. {tool.name}")
        else:
            print(f"  {i+1}. {type(tool).__name__}")

    return tools

# Initialize tools
tools = asyncio.run(initialize_tools())

# bind tools for llm
llm_with_tools = llm.bind_tools(tools)

async def chatbot(state: State):
    """异步处理对话的主函数，包含系统提示词"""
    # 获取当前消息
    messages = state["messages"]
    
    # 检查是否需要添加系统提示词（只在第一次对话时添加）
    has_system_message = any(isinstance(msg, SystemMessage) for msg in messages)
    
    if not has_system_message:
        # 在消息列表开头插入系统提示词
        system_message = SystemMessage(content=SYSTEM_PROMPT)
        messages_with_system = [system_message] + messages
    else:
        messages_with_system = messages
    
    # 调用LLM
    response = await llm_with_tools.ainvoke(messages_with_system)
    
    return {"messages": [response]}

# Build graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# Create async tool node
async def async_tool_node(state: State):
    """异步工具节点"""
    tool_node = ToolNode(tools=tools)
    return await tool_node.ainvoke(state)

graph_builder.add_node("tools", async_tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Create memory saver
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# Build the graph
graph = graph_builder.compile(checkpointer=memory)
# Configuration for the memory saver and recursion limit
config = {"configurable": {"thread_id": "1"},
          "recursion_limit": 100
          }

async def async_stream_graph_updates(user_input: str):
    """异步处理用户输入并显示结果"""
    async for event in graph.astream(
        {"messages": [{"role": "user", "content": user_input}]}, 
        config):
        
        for node_name, value in event.items():
            print(f"\n--- {node_name} ---")
            if "messages" in value:
                value["messages"][-1].pretty_print()
            print("-" * 40)

def stream_graph_updates(user_input: str):
    """同步包装器"""
    asyncio.run(async_stream_graph_updates(user_input))

def main():
    """主程序"""
    print("轨道专家 AI 助手")
    print("输入 'bye' 退出程序")
    print("-" * 40)
    
    # 对话循环
    while True:
        try:
            user_input = input("用户: ")
            
            if user_input.lower() in ["quit", "exit", "q", "bye"]:
                print("助手: 再见！")
                break
                
            if user_input.strip():  # 确保输入不为空
                stream_graph_updates(user_input)
            else:
                print("请输入有效的问题或指令")
                
        except KeyboardInterrupt:
            print("\n助手: 程序被用户中断，再见！")
            break
        except EOFError:
            print("\n助手: 输入结束，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            print("请重试或输入其他指令")

if __name__ == "__main__":
    main()