import argparse
import os

from openai import OpenAI


SYSTEM_PROMPT = """You are an embedded-systems diagnostic assistant.
Explain the supplied measurements and an existing rule-based diagnosis to an engineer.
Do not invent measurements, components, tests, or certainty.
Clearly distinguish measured evidence from hypotheses.
Give practical inspection steps and a safety note.
"""


def explain(temperature, raw, fault):
    """Ask the LLM to explain an already-created rule-based diagnosis."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY before using the LLM layer.")

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

    prompt = (
        f"Temperature: {temperature} C\n"
        f"ADC raw: {raw}\n"
        f"Rule-based classification: {fault}\n\n"
        "Explain the diagnosis, measured evidence, possible causes, "
        "recommended checks, and safety considerations."
    )

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    return response.output_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLM explanation layer for embedded diagnostics"
    )
    parser.add_argument("--temperature", type=float, required=True)
    parser.add_argument("--raw", type=int, required=True)
    parser.add_argument("--fault", required=True)
    args = parser.parse_args()

    try:
        print(explain(args.temperature, args.raw, args.fault))
    except Exception as exc:
        raise SystemExit(f"LLM diagnostic error: {exc}") from exc
