from utils import load_file
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Select device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model
model_name  = "gpt2" # "gpt2-xl" for larger version
tokenizer   = AutoTokenizer.from_pretrained(model_name)
model       = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Load input text from data/input.txt
input_text = load_file("input.txt")

# Tokenize input
input_ids = tokenizer(input_text, return_tensors="pt")["input_ids"].to(device)

def generate_text(input_ids, max_length=128, **generation_kwargs):
    output = model.generate(input_ids,max_length=max_length,**generation_kwargs)
    return tokenizer.decode(output[0])

# Greedy search
output_greedy = generate_text(input_ids,do_sample=False)
print("\n === Greedy Search === \n")
print(output_greedy)

# Beam search
output_beam = generate_text(input_ids,num_beams=5,do_sample=False)
print("\n === Beam Search === \n")
print(output_beam)

# Beam search + n-gram penalty
output_n_gram = generate_text(input_ids, num_beams=5, do_sample=False, no_repeat_ngram_size=2)
print("\n === Beam Search + N-gram Penalty === \n")
print(output_n_gram)

# Top-k sampling
output_top_k = generate_text(input_ids, do_sample=True, top_k=50)
print("\n === Top-k Sampling === \n")
print(output_top_k)

# Top-p sampling
output_top_p = generate_text(input_ids, do_sample=True, top_p=0.90)
print("\n === Top-p Sampling === \n")
print(output_top_p)

