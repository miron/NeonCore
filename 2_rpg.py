from transformers import T5Tokenizer, T5ForConditionalGeneration 

# Load the T5 model
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

# Define the input text
input_text = 'What is cyberpunk?'

# Generate a response using the T5 model
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)

print(tokenizer.decode(outputs[0]))




