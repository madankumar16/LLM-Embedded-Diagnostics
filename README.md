<h1 align="center">🤖 LLM Embedded Diagnostics</h1>

<p align="center">
  Turns a sensor fault from my STM32 / ESP32 boards into a clear,<br>
  step-by-step explanation an engineer can act on.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/OpenAI-API-412991?style=flat-square&logo=openai&logoColor=white">
  <img src="https://img.shields.io/badge/Hardware-STM32%20%7C%20ESP32-03234B?style=flat-square">
</p>

---

## 💡 The idea

A microcontroller can tell you **"SENSOR_LOW_OR_DISCONNECTED"**. It can't tell you *why* or *what to check first*.

This tool takes the reading and the fault label, and asks an LLM to explain:

- what the numbers mean
- the likely causes
- what to inspect, step by step
- any safety concerns

---

## 🔁 How it fits together

```text
 ESP32 / STM32  ──►  temperature + raw ADC value
                          │
                          ▼
              Rule-based check  (fixed, testable rules)
                          │   e.g. "SENSOR_HIGH_OR_SHORT"
                          ▼
              LLM explanation   (this repo)
                          │
                          ▼
                 Engineer reads a clear report
```

### Why the rules still decide

The **fixed rules** decide what the fault is. The **LLM only explains it**.
That keeps the safety decision predictable and testable, while still giving a human-friendly report.
The prompt also tells the model not to invent measurements, and to keep facts separate from guesses.

---

## ✨ Features

- ✅ Checks inputs first — the temperature must be a real number, the raw ADC value 0–4095, and the fault label must be one of the six rule-engine names
- 🔐 Reads the API key from an environment variable, so it never sits in the code
- 🔄 You can swap the model with `OPENAI_MODEL`
- 🖥️ Simple command-line use

---

## 🚀 Quick start

```bash
pip install -r requirements.txt
```

Set your key (never commit it):

```bash
# Linux / macOS
export OPENAI_API_KEY="your-key"

# Windows PowerShell
$env:OPENAI_API_KEY="your-key"
```

Run it:

```bash
python llm_diagnostic.py --temperature 37.2 --raw 462 --fault NORMAL
python llm_diagnostic.py --temperature 37.2 --raw 0   --fault SENSOR_LOW_OR_DISCONNECTED
```

`--fault` must be one of the rule engine's fault names:
`NORMAL`, `LOW_TEMPERATURE`, `HIGH_TEMPERATURE`, `TEMPERATURE_OUT_OF_RANGE`, `SENSOR_LOW_OR_DISCONNECTED`, `SENSOR_HIGH_OR_SHORT`.
Anything else is rejected before the API is called, so free text can't slip into the prompt.

The default model is `gpt-5.6-luna`. Set `OPENAI_MODEL` to use a different model.

| Option | Meaning |
|---|---|
| `--temperature` | Reading in °C |
| `--raw` | Raw 12-bit ADC value (0–4095) |
| `--fault` | Label from the rule-based check (one of the six names above, any case) |

---

## 🧪 Testing

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The tests mock the OpenAI client, so they need no API key and no internet. They check that:

- bad inputs (NaN temperature, raw value outside 0–4095, empty or unknown fault names such as free text) are rejected before any API call
- a missing `OPENAI_API_KEY` raises an error
- the prompt sent to the model has the temperature and the fault name in upper case, plus the fixed system instructions

---

## 📁 Files

| File | What's inside |
|---|---|
| `llm_diagnostic.py` | Input checks, the prompt, and the API call |
| `requirements.txt` | Needs only the OpenAI Python SDK (pinned version) |
| `tests/` | Unit tests — no API key or internet needed |
| `docs/CODE_EXPLANATION.md` | Line-by-line walkthrough of the code |

---

## ⚠️ Honest limits

- An LLM explanation is **not a measurement**. Treat it as advice, not proof.
- It needs internet access and an API key.
- The hardware and the rule-based check live in [STM32-Temperature-Detection](https://github.com/madankumar16/STM32-Temperature-Detection).

---

<p align="center">Made by <a href="https://github.com/madankumar16">Madan Kumar S</a> · ECE, VTU '28</p>
