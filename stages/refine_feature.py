import os
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from rich.pretty import pprint

# Replace host and port
client = LlamaStackClient(base_url=f"{os.getenv('LLAMA_STACK_URL')}")

agent = Agent(
    client,
    # Check with `llama-stack-client models list`
    model="Llama3.2-3B-Instruct",
    instructions="You are a helpful assistant",
    # Enable both RAG and tool usage
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {"vector_db_ids": ["my_docs"]},
        },
        "builtin::code_interpreter",
    ],
    # Configure safety (optional)
    input_shields=["llama_guard"],
    output_shields=["llama_guard"],
    # Control the inference loop
    max_infer_iters=5,
    sampling_params={
        "strategy": {"type": "top_p", "temperature": 0.7, "top_p": 0.95},
        "max_tokens": 2048,
    },
)
session_id = agent.create_session("monitored_session")

# Stream the agent's execution steps
response = agent.create_turn(
    messages=[{"role": "user", "content": "Analyze this code and run it"}],
    documents=[
        {
            "content": "https://raw.githubusercontent.com/example/code.py",
            "mime_type": "text/plain",
        }
    ],
    session_id=session_id,
)

# Monitor each step of execution
for log in AgentEventLogger().log(response):
    log.print()

# Using non-streaming API, the response contains input, steps, and output.
response = agent.create_turn(
    messages=[{"role": "user", "content": "Analyze this code and run it"}],
    documents=[
        {
            "content": "https://raw.githubusercontent.com/example/code.py",
            "mime_type": "text/plain",
        }
    ],
    session_id=session_id,
)

pprint(f"Input: {response.input_messages}")
pprint(f"Output: {response.output_message.content}")
pprint(f"Steps: {response.steps}")
