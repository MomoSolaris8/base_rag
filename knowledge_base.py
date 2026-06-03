import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from dotenv import load_dotenv
import dashscope

load_dotenv()
dashscope.base_http_api_url = os.getenv("DASHSCOPE_BASE_HTTP_API_URL")

def check_md5(md5_str: str):
    """Check whether the incoming MD5 string has
  already been processed."""
    if not os.path.exists(config.md5_path):
       open(config.md5_path, 'w',encoding='utf-8').close()
       return False
    else:
        for line in open(config.md5_path, 'r',encoding='utf-8').readlines():
             line = line.strip()
             if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    with open(config.md5_path,'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str:str, encoding='utf-8'):
    return hashlib.md5(input_str.encode(encoding)).hexdigest()



class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name= config.collection_name,
            embedding_function= DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory = config.persist_directory,
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size= config.chunck_size,
            chunk_overlap= config.chunk_overlap,
            separators= config.separators,
            length_function=len,
        )

    def upload_by_str(self,data: str, filename):
        md5_hex= get_string_md5(data)
        if check_md5(md5_hex):
            return "Already uploaded"
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks =[data]

        metadata = {
            "source": filename,
            "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"Momo",
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata  for _ in knowledge_chunks],
        )
        save_md5(md5_hex)
        return "Upload success"


if __name__ == '__main__':
   #print(check_md5("26307ecc02f0e3cb30346d1f28d4c225"))
   service = KnowledgeBaseService()
  # service.upload_by_str("hello world,Momo", "test")
   #result = service.upload_by_str("hello world,Momo2", "test")
  # print(result)
