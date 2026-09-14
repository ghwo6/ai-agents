import os
from dotenv import load_dotenv
from openai import OpenAI


dotenv_dir = "./../.env"

load_dotenv(dotenv_path=dotenv_dir,override=True)  # loading and setting the api key can be done in one step

if not os.getenv("Base_url"):
    os.environ["Base_url"] = "Your_Base_url"
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "Your_OPENAI_API_KEY"

if os.getenv("Base_url") != "Your_Base_url":
    print("✅ Base_url 로드됨")
    Base_url = os.getenv("Base_url")
else:
    print("❌ Base_url 로드 실패")
if os.getenv("OPENAI_API_KEY") != "Your_OPENAI_API_KEY":
    print("✅ OPENAI_API_KEY 로드됨")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
else:
    print("❌ OPENAI_API_KEY 로드 실패")


# Example function to query ChatGPT
def prompt_llm(messages,model = "gpt-5-mini",base_url=None,api_key=""):
    if base_url:
        #Azure or local LLM deployment
        client = OpenAI(base_url=base_url)
    else:
        #OpenAI deployment, api key set in environment variable
        client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        )
    
    return response.chices[0].message.content

def prompt_llm_modified(message,model = "gpt-5-mini",base_url="",api_key=""):
    prompt_llm(messages=message,model=model,base_url=Base_url,api_key=OPENAI_API_KEY)