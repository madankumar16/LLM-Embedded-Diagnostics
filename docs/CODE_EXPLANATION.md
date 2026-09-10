# LLM Embedded Diagnostics — Code Explanation

## Purpose

`llm_diagnostic.py` is the explanation layer of the embedded diagnostics architecture. It receives measurements and an already-generated rule-based classification, then asks an LLM to explain the evidence, possible causes, and practical engineering checks.

The LLM is intentionally not the sole fault classifier. This separation keeps the primary diagnosis deterministic and inspectable.

## 1. Imports

```python
import os
import argparse
from openai import OpenAI
```

- `os` reads the API key and optional model name from environment variables.
- `argparse` provides a simple command-line interface.
- `OpenAI` is used to call the OpenAI API.

## 2. Diagnostic system prompt

`SYSTEM_PROMPT` instructs the model to:

- explain supplied measurements and the existing rule-based diagnosis;
- avoid inventing measurements, components, tests, or certainty;
- distinguish measured evidence from hypotheses;
- provide practical inspection steps; and
- include a safety note.

This is an engineering guardrail, not a substitute for experimental validation.

## 3. API-key protection

Before creating the client, the code checks for `OPENAI_API_KEY`. The key must be supplied through the environment and must never be committed to GitHub.

Example environment setup on Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

Example on Linux/macOS:

```bash
export OPENAI_API_KEY="your_key_here"
```

## 4. Inputs

`explain(temperature, raw, fault)` accepts:

- `temperature`: measured temperature in °C;
- `raw`: ADC raw value;
- `fault`: the result of the deterministic rule-based classifier.

The prompt explicitly labels the rule-based classification so the LLM explains an existing diagnosis rather than silently replacing it.

## 5. Model call

The model is selected from `OPENAI_MODEL`, with a default value in the source code. Before using this project for a real experiment, verify the model identifier against the current OpenAI documentation and account availability.

The response text is returned through `response.output_text`.

## 6. Command-line usage

```bash
python llm_diagnostic.py --temperature 37.2 --raw 462 --fault NORMAL
```

## 7. Complete architecture

```text
ESP32 / STM32
      ↓
Structured telemetry
      ↓
Rule-based diagnosis
      ↓
Fault + evidence
      ↓
LLM explanation layer
      ↓
Engineer review
```

## Important research limitation

The LLM output is generated from the supplied inputs and should be treated as decision support. It must not be described as measured evidence, validated diagnostic accuracy, or an autonomous safety controller without appropriate testing and validation.
