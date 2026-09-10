# LLM Embedded Diagnostics

LLM explanation layer for the embedded fault-detection research project.

## Code
- `llm_diagnostic.py` — sends structured telemetry and an existing rule-based diagnosis to an LLM and returns an engineering explanation.
- `docs/CODE_EXPLANATION.md` — explains the prompt, inputs, API call, security model, command-line usage, architecture, and limitations.

## Data flow
ESP32/STM32 → telemetry → rule-based diagnosis → LLM explanation → engineer

## Role of the LLM
The deterministic rule-based classifier remains the primary experimental baseline. The LLM is used for explanation and decision support; it is not the sole safety-critical fault classifier.

## Run
Set the API key as an environment variable, then run:
```bash
python llm_diagnostic.py --temperature 37.2 --raw 462 --fault NORMAL
```

Optionally select a verified model identifier with `OPENAI_MODEL`.

## Security
Never commit API keys. Use an environment variable such as `OPENAI_API_KEY` and keep secrets out of source control.

## Research integrity
LLM explanations must not be presented as measured evidence. Keep measured telemetry, deterministic diagnosis, hypotheses, and generated explanations clearly separated in experiments and reports.
