#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spark_api.py
@Time    :   2023/09/24 11:00:46
@Author  :   Logan Zou 
@Version :   1.0
@Contact :   loganzou0421@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   启动服务为本地 API
'''

from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys
# 导入功能模块目录
sys.path.append("../")
from qa_chain.QA_chain_self import QA_chain_self

# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

app = FastAPI() # 创建 api 对象

template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
{context}
问题: {question}
有用的回答:"""

# 定义一个数据模型，用于接收POST请求中的数据
class Item(BaseModel):
    prompt : str # 用户 prompt
    model : str = "gpt-3.5-turbo"# 使用的模型
    temperature : float = 0.1# 温度系数
    if_history : bool = False # 是否使用历史对话功能
    # API_Key
    api_key: str = None
    # Secret_Key
    secret_key : str = None
    # access_token
    access_token: str = None
    # APPID
    appid : str = None
    # APISecret
    Spark_api_secret : str = None
    # Secret_key
    Wenxin_secret_key : str = None
    # 数据库路径
    db_path : str = "/Users/lta/Desktop/llm-universe/data_base/vector_db/chroma"
    # 源文件路径
    file_path : str = "/Users/lta/Desktop/llm-universe/data_base/knowledge_db"
    # prompt template
    prompt_template : str = template
    # Template 变量
    input_variables : list = ["context","question"]
    # Embdding
    embedding : str = "m3e"
    # Top K
    top_k : int = 5
    # embedding_key
    embedding_key : str = None

@app.post("/")
async def get_response(item: Item):

    # 首先确定需要调用的链
    if not item.if_history:
        # 调用 Chat 链
        # return item.embedding_key
        if item.embedding_key == None:
            item.embedding_key = item.api_key
        chain = QA_chain_self(model=item.model, temperature=item.temperature, top_k=item.top_k, file_path=item.file_path, persist_path=item.db_path, 
                                appid=item.appid, api_key=item.api_key, embedding=item.embedding, template=template, Spark_api_secret=item.Spark_api_secret, Wenxin_secret_key=item.Wenxin_secret_key, embedding_key=item.embedding_key)

        response = chain.answer(question = item.prompt)
    
        return response
    
    # 由于 API 存在即时性问题，不能支持历史链
    else:
        return "API 不支持历史链"



if __name__ == '__main__':
    result = {}
    arg = [ { "故事设定": [ "一座艺术氛围浓厚的小城，近期发生多起离奇凶杀案", "凶手将受害者布置成艺术品，引发社会恐慌", "警方束手无策，一位神秘侦探主动请缨调查", "侦探有48小时破案，否则其妹妹将成为下一个受害者" ] }, { "人物设定": [ "男主陆临：冷静睿智的侦探，为救妹妹主动卷入案件", "女主苏沫：善良正义的警官，协助陆临调查", "反派艾伦：将杀人视为艺术创作的连环杀手", "陆茉：陆临的妹妹，被艾伦绑架作为人质" ] }, { "开端": [ "陆临接到艾伦的挑战信，得知妹妹被绑架", "陆临与苏沫组队，开始48小时的破案倒计时", "二人调查前几起案件，发现凶手模仿不同艺术流派" ] }, { "发展": [ "陆临推理出凶手的作案规律和下一个目标", "苏沫怀疑陆临另有所图，二人产生信任危机", "陆临故意成为'艺术品'，引诱艾伦现身", "艾伦察觉陷阱，反将陆临困在密室" ] }, { "高潮": [ "苏沫解开误会，及时营救陷入险境的陆临", "陆临与艾伦展开激烈的心理战和推理对决", "艾伦暴露出扭曲的艺术观，陆临巧妙说服他" ] }, { "结局": [ "艾伦被捕，陆茉获救，案件真相大白于天下", "陆临发现艾伦另有指使，暗示更大阴谋", "苏沫邀请陆临加入警队，二人携手对抗罪恶" ] } ]
    for item in arg:
        temp = ''
        idx = 1
        for key,value in item.items():
            for sub_item in value:
                temp = f'{temp}{idx}. {sub_item}\n'
                idx += 1
        result[key] = temp
    print(result)

