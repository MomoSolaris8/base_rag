from operator import itemgetter

from git.config import needs_values
from jinja2.runtime import new_context
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from vector_stores import VectorStoreService
import config_data as config
from langchain_community.chat_models.tongyi import ChatTongyi

from file_history_store import get_history

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagService(object):
    def __init__(self):

        self.vector_store = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "以我提供的已知参考资料为主，简洁和专业地回答用户问题。"
                    "参考资料：{context}"
                ),
                ("system", "并且我提供用户的历史记录，如下："),
                 MessagesPlaceholder("history"),
                ("user", "请回答用户提问{input}")
            ]
        )
        self.chat_model = ChatTongyi(model= config.chat_model_name)

        self.chain = self.__get_chain()

    def __get_chain(self):

        retriever = self.vector_store.get_retriever()


        def format_document(docs: list[Document]):
            if not docs:
                return "no relevant documents found"

            formatted_docs = ""
            for doc in docs:
                formatted_docs += f"split document from: {doc.page_content}\n metadata: {doc.metadata} \n\n"
            return formatted_docs

        #test
        def temp1(value):
            print("---------",value)
            return value

 # 这里可以直接用RunnablePassthrough()的assign()方法，输出原来哥是的字典，不用自己写forma团，
        # （RunnablePassthrough.assign(context = itemgetter("input")|         def temp2(value):
        #            # print("---------",value)
        #            new_value = {}
        #            new_value["input"] = value["input"]["input"]
        #            new_value["context"] = value["context"]
        #            new_value["history"] = value["input"]["history"]
        #            return value

        chain=(
                RunnablePassthrough.assign(
                    context=itemgetter("input") | retriever | format_document
                )| self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain= RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == "__main__":
    res = RagService().chain.invoke({"input": "我体重170cm，尺码推荐"},config.session_config)
    print(res)
