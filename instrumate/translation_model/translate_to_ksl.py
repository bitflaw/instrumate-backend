from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import os



# Generate translation

def eng_to_ksl_translator(input):
    # Sample input sentence
    model_path = os.path.join(os.path.dirname(__file__), 'instrumate-english-ksl-model')
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    model.eval()
    ksl_input = f"translate English to KSL: {input}"  # Replace this
    # Tokenize
    inputs = tokenizer(ksl_input, return_tensors="pt", max_length=128, truncation=True)
    with torch.no_grad():
        # Ensure the inputs are on the same device as the model
        device = model.device
        # inputs = {k: v.to(device) for k in inputs.keys()} # Corrected iteration

        inputs = {k: v.to(device) for k, v in inputs.items()} # Original code

        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=128,
            num_beams=5
        )

    # Decode and print
    translation = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return translation

def ksl_to_eng_translator(input):
    # Sample input sentence
    model_path = os.path.join(os.path.dirname(__file__), 'instrumate_ksl_to_english_model')
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    model.eval()
    ksl_input = f"translate KSL to English: {input}"  # Replace this
    # Tokenize
    inputs = tokenizer(ksl_input, return_tensors="pt", max_length=128, truncation=True)
    with torch.no_grad():
        # Ensure the inputs are on the same device as the model
        device = model.device
        # inputs = {k: v.to(device) for k in inputs.keys()} # Corrected iteration

        inputs = {k: v.to(device) for k, v in inputs.items()} # Original code

        output_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=128,
            num_beams=5
        )

    # Decode and print
    translation = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return translation


