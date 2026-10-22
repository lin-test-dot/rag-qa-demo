from config import CHUNK_SIZE, CHUNK_OVERLAP
from chunker import split_text
from retriever import search
from rag import answer

# 1. 读取文件
try:
    with open("test.txt", 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("❌ 找不到 test.txt，请检查文件是否在项目根目录！")
    exit()

# 2. 切块
chunks = split_text(content, CHUNK_SIZE, CHUNK_OVERLAP)
print(f"✅ 文件读取成功，共切分为 {len(chunks)} 个文本块。")

# 3. 交互
print("\n🤖 知识库助手已上线！输入 '退出' 结束。")

while True:
    query = input("\n你: ").strip()
    if query == "退出":
        print("🤖: 拜拜！")
        break
    if not query:
        continue

    # 4. 检索
    matched_chunks = search(query, chunks)

    # 5. 生成
    if len(matched_chunks) > 0:
        print(f"🔍 找到 {len(matched_chunks)} 个相关文本块。")
        reply = answer(query, matched_chunks)
        print(f"🤖: {reply}")
    else:
        print("🤖: 抱歉，你的本地资料库里没有找到相关的内容，请换个关键词试试。")