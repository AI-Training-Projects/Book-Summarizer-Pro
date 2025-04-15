# Core summarization logic
from transformers import pipeline
from utils import chunk_text
import torch
from flask import current_app
from typing import List, Dict

MODELS = {
    'bart': 'facebook/bart-large-cnn',
    'pegasus': 'google/pegasus-cnn_dailymail'
}

BATCH_SIZE = 4  # Process 4 chunks at a time

def get_device():
    if torch.cuda.is_available():
        device = "cuda:0"
        current_app.logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        current_app.logger.info("Using CPU for inference")
    return device

def calculate_max_length(text_length, ratio=0.3):
    """Calculate appropriate max_length for summarization.
    
    Rules:
    1. Output should be shorter than input (ratio * input_length)
    2. Minimum length of 50 tokens
    3. For very short inputs, use 75% of input length
    4. Never exceed input length
    """
    if text_length < 100:
        # For very short texts, use 75% of length
        max_len = max(50, int(text_length * 0.75))
    else:
        # Normal case: use the ratio but ensure it's shorter than input
        max_len = min(text_length - 1, int(text_length * ratio))
    
    # Ensure minimum of 50 tokens
    return max(50, min(text_length - 1, max_len))

def process_batch(summarizer, chunks: List[str], config: Dict, start_idx: int, total_chunks: int):
    """Process a batch of chunks together."""
    # Calculate max_length for each chunk in the batch
    chunk_lengths = [len(chunk.split()) for chunk in chunks]
    max_lengths = [calculate_max_length(length, config['summary_ratio']) for length in chunk_lengths]
    min_lengths = [max(30, max_len // 2) for max_len in max_lengths]

    # Log batch information
    for i, (chunk_len, max_len) in enumerate(zip(chunk_lengths, max_lengths)):
        batch_idx = start_idx + i
        progress = (batch_idx / total_chunks) * 100
        current_app.logger.info(f"Processing chunk {batch_idx}/{total_chunks} ({progress:.1f}%) - Input length: {chunk_len}, Max output: {max_len}")
        
        # Update progress in Flask session
        if hasattr(current_app, 'progress_callback'):
            current_app.progress_callback(progress)

    # Process the batch
    summaries = summarizer(chunks, 
                         max_length=max(max_lengths),  # Use maximum length in batch
                         min_length=min(min_lengths),  # Use minimum length in batch
                         do_sample=False)
    
    return [summary['summary_text'] for summary in summaries]

def summarize_document(text, config, output_folder):
    device = get_device()
    model_name = MODELS[config['model']]
    summarizer = pipeline('summarization', model=model_name, device=device)
    chunks = chunk_text(text, config['chunk_size'], config['chunk_overlap'])
    total_chunks = len(chunks)
    
    current_app.logger.info(f"Processing {total_chunks} chunks of text in batches of {BATCH_SIZE}")
    summaries = []
    
    # Process chunks in batches
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        batch_summaries = process_batch(summarizer, batch, config, i, total_chunks)
        summaries.extend(batch_summaries)

    full_summary = "\n\n".join(summaries)
    return full_summary, output_folder
