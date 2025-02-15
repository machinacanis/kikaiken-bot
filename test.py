import os

from langchain_core.messages import SystemMessage, HumanMessage

from kikaiken.core.llm import ChatDeepSeekOnSiliconFlow

os.environ["SILICONFLOW_API_KEY"] = "sk-gieepgmupqffgtcquwsfqnqwfkaqnullpvfzzsuknkzpicys"
llm = ChatDeepSeekOnSiliconFlow(model="deepseek-ai/DeepSeek-V3")

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

res = llm.invoke(messages)
print(res.content)
