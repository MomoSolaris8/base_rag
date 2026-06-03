from langchain_chroma import Chroma
import config_data as config
from config_data import similarity_threshold
from dotenv import load_dotenv
import dashscope
load_dotenv()
import os
dashscope.base_http_api_url = os.getenv("DASHSCOPE_BASE_HTTP_API_URL")
class VectorStoreService(object):


    def __init__(self, embedding):
         self.embedding = embedding
         self.vector_store = Chroma(
             collection_name= config.collection_name,
             embedding_function= self.embedding,
             persist_directory = config.persist_directory,
         )

    def get_retriever(self):
         return self.vector_store.as_retriever(search_kwargs={"k": similarity_threshold})


if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    #res=retriever.invoke("我的体重180斤，尺码推荐")
    #print(res)