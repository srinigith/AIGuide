import torch
from transformers import LLaMAForConversation, LLaMAIndex

# Initialize the LLaMA model and index
model = LLaMAForConversation.from_pretrained("llama-index-base")
index = LLaMAIndex("llama-index-base")

# Define the conversation history
conversation_history = [
    {"user": "I'm looking for remote job opportunities."},
    {"assistant": "Here are some reliable job portals for finding Work-From-Home (WFH) or Remote job opportunities..."},
    {"user": "That's great! But I'm specifically looking for freelance writing opportunities."}
]

# Convert the conversation history to a format compatible with the RAG model
input_ids = []
attention_masks = []
for turn in conversation_history:
    input_id = torch.tensor([turn["user"]])
    attention_mask = torch.tensor([[1]])
    input_ids.append(input_id)
    attention_masks.append(attention_mask)

input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)

# Use the RAG model to generate a new query
output = model.generate(input_ids, attention_masks, max_length=50)

# Get the generated query
generated_query = output[0]["generated_text"]

print("Generated Query:", generated_query)

# Use the generated query to retrieve relevant information from the knowledge base
results = index.search(generated_query)

print("Results:", results)
