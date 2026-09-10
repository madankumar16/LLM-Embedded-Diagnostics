import os
import argparse
from openai import OpenAI

SYSTEM_PROMPT = '''You are an embedded-systems diagnostic assistant. Explain supplied measurements and an existing rule-based diagnosis to an engineer. Do not invent measurements, components, tests, or certainty. Clearly distinguish measured evidence from hypotheses. Give practical inspection steps and a safety note.'''

def explain(temperature, raw, fault):
    if not os.getenv('OPENAI_API_KEY'):
        raise RuntimeError('Set OPENAI_API_KEY before using the LLM layer.')
    client = OpenAI()
    prompt = f'''Temperature: {temperature} C\nADC raw: {raw}\nRule-based classification: {fault}\n\nExplain the diagnosis, evidence, possible causes, and recommended checks.'''
    response = client.responses.create(
        model=os.getenv('OPENAI_MODEL', 'gpt-5.6-mini'),
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    return response.output_text

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--temperature', type=float, required=True)
    p.add_argument('--raw', type=int, default=0)
    p.add_argument('--fault', required=True)
    a = p.parse_args()
    print(explain(a.temperature, a.raw, a.fault))
