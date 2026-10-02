# langchain-kavel

A LangChain tool that generates and edits images with [Kavel AI](https://www.kavel.ai/?utm_source=langchain&utm_medium=package),
with **no API key needed** to start.

```bash
pip install langchain-kavel
```

```python
from langchain_kavel import KavelImageGenerator

tool = KavelImageGenerator()
url = tool.invoke({"prompt": "matte black ceramic mug on pale oak, soft window light",
                   "aspect_ratio": "16:9"})
# https://cdn.kavel.ai/uploads/kie/image/....webp
```

Give it to an agent like any other tool:

```python
from langchain.agents import create_agent

agent = create_agent("openai:gpt-5-mini", tools=[KavelImageGenerator()])
agent.invoke({"messages": [{"role": "user", "content": "Make a cover image for a post about sourdough"}]})
```

## Free tier, then your account

Without a key the tool runs on Kavel's free anonymous tier. On 2026-10-02 a fresh client id was
granted 5 credits and one generated image spent all five; free output is 1K and watermarked. When
the allowance is spent, the tool returns a short message the agent can act on instead of raising.

Pass `KavelImageGenerator(api_key=...)` or set `KAVEL_API_KEY` with a key from
[kavel.ai/settings/apikeys](https://www.kavel.ai/settings/apikeys?utm_source=langchain&utm_medium=package)
to run on your account. That also enables editing (`image_url`) and `model=` for any image model on
your plan.

## License

MIT.
