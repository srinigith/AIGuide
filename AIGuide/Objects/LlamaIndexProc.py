import groq
from llama_index.core import prompts, query_engine
import nest_asyncio
from decouple import config
import os
import json
#from groq import Groq
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings, SimpleDirectoryReader,VectorStoreIndex,SummaryIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_parse import LlamaParse
from llama_index.core.query_engine import MultiStepQueryEngine, RouterQueryEngine
from llama_index.core.indices.struct_store import JSONQueryEngine
from llama_index.core import Document
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)

nest_asyncio.apply()
os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")

#docs_12thChem = LlamaParse(result_type="text",api_key="llx-iO5--------------------------KzaFQ").load_data("data/12th_Chemistry_Vol_2.pdf")
#docs_12thChem = SimpleDirectoryReader(input_files=["data/12th_Chemistry_Vol_2.pdf"]).load_data()

#response = llm.complete("Give an introduction on IONIC EQUILIBRIUM from loaded pdf document in html format.")


#index = VectorStoreIndex.from_documents(docs_12thChem)
#query_engine = index.as_query_engine(similarity_top_k=3)

"""
sum_index = SummaryIndex.from_documents(docs_12thChem)
vector_tool = QueryEngineTool(index.as_query_engine(),
                              metadata=ToolMetadata(
                                  name='vector_search',
                                  description='Useful for searching for specific facts.')
                              )
summary_tool = QueryEngineTool(sum_index.as_query_engine(response_mode="tree_summarize"),
                               metadata=ToolMetadata(
                                   name='summary',
                                   description='Useful for summarizing an entire document.')
                               )

query_engine = RouterQueryEngine.from_defaults(
    [vector_tool,summary_tool],select_multi=False,verbose=True,llm=llm_70b)
"""

def GetGroqResponse(prompt):
    client = groq.Groq(api_key=config("GROQ_API_KEY"))    
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=prompt,
        temperature=1,
        #max_tokens=10240,
        top_p=1,
        stream=True,
        stop=None
    )
    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""
    return result

def GetQueryResponse(query, parsedData = None, filePath = "", router = True):
    if filePath is not None and filePath != "":        
        parsedData = LlamaParse(result_type="html",api_key=config("LLMINDEX_API_KEY")).load_data(filePath)
    else:
        #evalJson = eval(parsedData)
        text_list = [str(parsedData),]
        documents = [Document(text=t) for t in text_list]
        parsedData = documents
    
    llm = Groq(model="llama3-8b-8192")
    #llm_70b = Groq(model="llama3-70b-8192")
    #embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embed_model = HuggingFaceEmbedding(model_name="google/Gemma-Embeddings-v1.0")

    Settings.llm = llm
    Settings.embed_model = embed_model

    """    
    index = VectorStoreIndex.from_documents(parsedData)
    query_engine = index.as_query_engine(similarity_top_k=3)
    """
    index = VectorStoreIndex.from_documents(parsedData)
    sum_index = SummaryIndex.from_documents(parsedData)

    result = ""

    if router == True:
        vector_tool = QueryEngineTool(index.as_query_engine(),
                                  metadata=ToolMetadata(
                                      name='vector_search',
                                      description='Useful for searching for specific facts.')
                                  )
    
        summary_tool = QueryEngineTool(sum_index.as_query_engine(response_mode="tree_summarize"),
                                   metadata=ToolMetadata(
                                       name='summary',
                                       description='Useful for summarizing an entire document.')
                                   )

        query_engine = RouterQueryEngine.from_defaults(
        [summary_tool,vector_tool],select_multi=False,verbose=True,llm=llm)

        response = query_engine.query(query)
        result = response.response
    else:
        query_engine = index.as_query_engine(similarity_top_k=3,llm=llm)
        response = query_engine(query)
        result = response.response

    return result

def GetQueryMultyResp(query, parsedData):
    llm = Groq(model="llama3-8b-8192")
    text_list = [str(parsedData),]
    documents = [Document(text=t) for t in text_list]
    index = VectorStoreIndex.from_documents(documents)
    step_decompose_transform = StepDecomposeQueryTransform(llm, verbose=True)
    query_engine = index.as_query_engine()
    query_engine = MultiStepQueryEngine(
        query_engine, query_transform=step_decompose_transform
    )

    response = query_engine.query(
        query,
    )
    return response
