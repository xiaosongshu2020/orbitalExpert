from typing import Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from typing_extensions import TypedDict
from typing import TypedDict, Annotated, List, Union, Dict, Any
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os
import time
import sys
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

# #######################  use deepseek  #########################
# # 从环境变量获取API密钥
# DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# # 如果环境变量中没有设置API密钥，则提示用户手动输入
# if not DEEPSEEK_API_KEY:
#     print("警告: 未设置DEEPSEEK_API_KEY环境变量")
#     DEEPSEEK_API_KEY = input("请输入您的DeepSeek API密钥: ").strip()
#     # 设置环境变量
#     os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

# # Create LLM
# from langchain_deepseek import ChatDeepSeek
# llm = ChatDeepSeek(model="deepseek-chat", api_key=DEEPSEEK_API_KEY)

#######################  use qwen  #########################
# 从环境变量获取API密钥
QWEN_API_KEY = os.environ.get("QWEN_API_KEY")

# 如果环境变量中没有设置API密钥，则提示用户手动输入
if not QWEN_API_KEY:
    print("警告: 未设置QWEN_API_KEY环境变量")
    QWEN_API_KEY = input("请输入您的Qwen API密钥: ").strip()
    # 设置环境变量
    os.environ["QWEN_API_KEY"] = QWEN_API_KEY

# # 选择使用的模型（默认使用deepseek）
#采用ChatOpenAI调用示例
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    model="qwen3-coder-plus",
    openai_api_key=QWEN_API_KEY,
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0
)

#######################  use other LLMs  #########################
# see https://langchain-ai.github.io/langgraph/agents/models/

# 系统提示词
SYSTEM_PROMPT = """你是一个专业的航天器轨道力学专家AI助手，你的名字叫'小松鼠'。

请遵循以下原则：
1. 优先借用工具来完成任务，如果工具不适用，再考虑手动计算；
2. 如果你不确定某个问题的答案，请诚实地告诉用户；
3. 生成的数据默认保存在'./files/'里；
4. 调用工具时，文件名必须使用绝对路径；
5. 请先给出思考过程，再调用工具或回答；
"""

class State(TypedDict):
    messages: Annotated[list, add_messages]

def print_welcome():
    """显示欢迎信息"""
    welcome_text = """
╔════════════════════════════════════════════════════════════════╗
                     🚀 轨道专家 AI 助手 🚀                     
                                                                
  我是您的轨道专家助手<小松鼠>，能够帮助您：                              
  • 卫星轨道计算                                             
  • 文件操作和数据处理                                           
  • ...
                                                                
  输入 'bye' 退出程序                   
╚════════════════════════════════════════════════════════════════╝
"""
    print(welcome_text)

def typewriter_print(text, delay=0.02):
    """打字机效果打印文本"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # 换行

def print_section_divider():
    """打印分隔线"""
    print("\n" + "═" * 60 + "\n")

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
# 获取documents目录（用户主目录下的Documents文件夹）
DOCUMENTS_DIR = Path.home() / "Documents"

# 确保必要的目录存在
FILES_DIR = PROJECT_ROOT / "files"
FILES_DIR.mkdir(exist_ok=True)

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
                    "D:/home/projects/mcp-server-satellite-orbit/",  # run_server.py所在的路径
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

    # Debug: Print tool information
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
    tool_called = False
    
    async for event in graph.astream(
        {"messages": [{"role": "user", "content": user_input}]}, 
        config):
        
        for node_name, value in event.items():
            if node_name == "tools":
                # 处理工具调用
                tool_called = True
                last_message = value["messages"][-1]
                
                # 打印工具名
                if hasattr(last_message, 'name'):
                    print(f"\n >>>>> 🔧 工具调用: {last_message.name}")
                else:
                    print(f"\n >>>>> 🔧 工具调用")

                # 显示工具执行结果
                if hasattr(last_message, 'content') and last_message.content:
                    print("\n >>>>> 🔧 工具执行结果:")
                    print(f"   {last_message.content}")
                    print("─" * 50)
                    
            elif node_name == "chatbot":
                # 处理助手回复
                last_message = value["messages"][-1]
                
                # 检查是否要调用工具
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    print(last_message.tool_calls)
                    continue  # 如果要调用工具，先不显示回复
                
                # 显示助手的最终回复
                if hasattr(last_message, 'content') and last_message.content:
                    if tool_called:
                        print("\n✨ 助手: ")
                    else:
                        print("\n✨ 助手: ")
                    
                    # 使用打字机效果显示回复
                    typewriter_print(last_message.content, delay=0.01)

def stream_graph_updates(user_input: str):
    """同步包装器"""
    asyncio.run(async_stream_graph_updates(user_input))

def main():
    """主程序"""
    # 显示欢迎信息
    print_welcome()
    
    # 对话循环
    while True:
        try:
            print_section_divider()
            user_input = input("😊 用户: ")
            
            if user_input.lower() in ["quit", "exit", "q", "bye"]:
                print("\n✨ 助手: 👋 再见！")
                break
                
            if user_input.strip():  # 确保输入不为空
                stream_graph_updates(user_input)
            else:
                print("⚠️  请输入有效的问题或指令")
                
        except KeyboardInterrupt:
            print("\n✨ 助手: 👋 程序被用户中断，再见！")
            break
        except EOFError:
            print("\n✨ 助手: 👋 输入结束，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print("🔄 请重试或输入其他指令")

if __name__ == "__main__":
    main()
