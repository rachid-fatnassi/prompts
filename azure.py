import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = os.getenv("ENDPOINT_URL", "https://ocs.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "OCS")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://ocs.search.windows.net")
search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")
search_index = os.getenv("SEARCH_INDEX_NAME", "test-index")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default")
      
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)
      
completion = client.chat.completions.create(
    model=deployment,
    messages= [
    {
      "role": "user",
      "content": "What are the differences between Azure Machine Learning and Azure AI services?"
    }],
    max_tokens=800,
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
    extra_body={
      "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": "test-index",
            "semantic_configuration": "test-index-semantic-configuration",
            "query_type": "semantic",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": "You are an AI assistant that helps people find financial information informations on oddo bhf documents.\nAnd answer honestly that you don't know the answer if the question is out of the context of oddo's publications or of the stock market/investment advice field.",
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            }
          }
        }]
    }
)
print(completion.to_json())
