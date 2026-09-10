# LLM Embedded Diagnostics

LLM explanation layer for the embedded fault-detection research project.

The system receives structured telemetry and a rule-based diagnosis, then asks an LLM to explain the evidence, likely causes, and recommended engineering checks. The LLM is not used as the sole safety-critical fault classifier.

## Data flow
ESP32/STM32 -> telemetry -> rule-based diagnosis -> LLM explanation -> engineer

## Security
Never commit API keys. Use an environment variable such as `OPENAI_API_KEY`.
