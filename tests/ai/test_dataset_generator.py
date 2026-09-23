import pytest
from app.ai.training.dataset_generator import synthetic_dataset_generator
from app.ai.training.fine_tune_pipeline import lora_fine_tune_pipeline

def test_ai_synthetic_dataset_pair_generation():
    ast_ctx = {"dasha": "Venus-Venus", "house": 10, "planet": "Sun"}
    pair = synthetic_dataset_generator.generate_instruction_pair("Career & Authority", ast_ctx, "Sun exalted in 10th house")

    assert pair["zero_hallucination_verified"] is True
    assert "Career & Authority" in pair["instruction"]
    assert "Venus-Venus" in pair["output"]

def test_ai_lora_fine_tuning_pipeline():
    res = lora_fine_tune_pipeline.execute_lora_fine_tuning("dataset.jsonl")

    assert res["training_status"] == "COMPLETED"
    assert res["quantization_format"] == "GGUF_4BIT_Q4_K_M"
    assert res["zero_hallucination_accuracy"] > 99.0
