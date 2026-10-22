import dashscope
import chromadb
from config import API_KEY

dashscope.api_key = API_KEY


# 把文字变成向量
def get_embedding(text):
    try:
        resp = dashscope.TextEmbedding.call(
            model="text-embedding-v2",
            input=text
        )
        return resp.output['embeddings'][0]['embedding']
    except Exception as e:
        print(f"❌ 向量化失败: {e}")
        return None


def search(query, chunks):
    # 1. 使用持久化客户端（数据存硬盘）
    #它是一个“轻量级”的 Python 包（库）。你不需要单独安装什么软件，只要 pip install chromadb，
    # 然后在代码里 import 一下，它就在你的代码运行空间里直接启动了一个数据库，甚至能把数据直接存成你项目文件夹里的一个文件
    client = chromadb.PersistentClient(path="./chroma_db")

    # 2. 获取或创建集合
    collection = client.get_or_create_collection(name="my_kb")

    # 3. 核心判断：如果库里没有数据，才进行向量化！
    if collection.count() == 0:
        print("⏳ 首次运行，正在将文本块转换为向量并写入硬盘...")
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            if embedding:
                collection.add(
                    embeddings=[embedding],
                    documents=[chunk],
                    ids=[str(i)]
                )
        print("✅ 向量化入库完成！")
    else:
        # 如果库里有数据，直接跳过，一秒钟都不耽误
        print(f"✅ 已从硬盘读取本地知识库，共 {collection.count()} 条数据，无需重新向量化！")

    # 4. 把用户的问题变成向量
    query_embedding = get_embedding(query)
    if not query_embedding:
        return []

    # 5. 去库里查
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    return results['documents'][0]
