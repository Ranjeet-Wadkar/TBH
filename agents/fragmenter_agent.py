import os
from dotenv import load_dotenv
from autogen import ConversableAgent

load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")


def fragmentor_agent(tree, content, migration_strategy_from_agent):
    fragmentor_agent = ConversableAgent(
        "chatbot",
        # llm_config={"config_list": [{"model": "o1-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]},
        llm_config={
            "config_list": [
                {
                    "model": AZURE_OPENAI_DEPLOYMENT_NAME,
                    "api_key": AZURE_OPENAI_API_KEY,
                    "base_url": AZURE_OPENAI_ENDPOINT,
                    "api_type": "azure",
                    # "api_version": "2024-02-15-preview"
                    "api_version": AZURE_OPENAI_API_VERSION
                }
            ]},
        human_input_mode="NEVER",  # No manual intervention
    )


    messages_for_fragmentor  =  [

        {"role" : "system",
        "content" : ''' 

        You are an expert Code Fragmentation and Migration Specialist with deep expertise in analyzing, modularizing, and transforming legacy codebases into structured, modern architectures. Your task is to analyze the given migration strategy and full codebase and generate a structured fragmentation and migration report.
        
        ---
        
        Inputs Given to You:
        
        1. Migration Strategy:
        - A step-by-step migration strategy outlining how the project should be transformed.
        
        2. Complete Codebase (Before Migration):
        - Full source code of the existing legacy system.
        - Project directory structure, including all files, modules, and dependencies.
        
        
        Your Expected Output:
        
        1. Comprehensive Feature-Based Fragmentation Report:
        - Analyze the provided legacy codebase and break it down into logical feature-based fragments.
        - Identify total features in the system and categorize them by functionality, dependencies, and purpose.
        - Clearly define each feature's role in the system and the files associated with it.
        - Segment dependencies, services, and business logic while ensuring minimal coupling.
        - Ensure each module can be independently migrated and tested.
        
        
        
        '''
            },

            {"role": "user",
            "content" : f'''
        
                Migration Strategy: {migration_strategy_from_agent}
        '''
            },

            {"role": "user",
            "content" : f'''
                Code Structure: {tree}
                Code base : {content}
        '''},


    ]


    fragmented_output_from_agent = fragmentor_agent.generate_reply(messages= messages_for_fragmentor)
    return fragmented_output_from_agent
