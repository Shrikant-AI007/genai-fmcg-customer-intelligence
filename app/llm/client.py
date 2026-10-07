import os
from .prompts import SYSTEM_PROMPT, USER_PROMPT

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "demo")
        self.model = os.getenv("LLM_MODEL", "")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

    def generate(self, question, analytics, documents):
        if self.provider == "demo" or not self.api_key or not self.model:
            return self._demo(question, analytics, documents)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": USER_PROMPT.format(question=question, analytics=analytics, documents=documents)},
                ], temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as exc:
            return self._demo(question, analytics, documents) + f"\n\n[LLM fallback activated: {type(exc).__name__}]"

    def _demo(self, question, analytics, documents):
        s = analytics.get("sales_summary", {})
        top = s.get("top_product") or "the leading product"
        revenue = s.get("revenue", 0)
        return (f"### Executive answer\nThe current dataset shows revenue of ₹{revenue:,.0f}, with **{top}** as the leading product. "
                f"The result is generated in demo mode using deterministic analytics; connect an LLM provider for full natural-language synthesis.\n\n"
                f"### Key evidence\n- Orders: {s.get('orders', 0):,}\n- Units: {s.get('units', 0):,}\n- Average order value: ₹{s.get('avg_order_value', 0):,.2f}\n\n"
                f"### Likely drivers / hypotheses\n- Investigate region, channel, product mix and promotion effects.\n- Validate inventory availability before concluding demand changed.\n\n"
                f"### Recommended next actions\n1. Compare the latest period with the prior period.\n2. Check high-risk inventory SKUs.\n3. Review promotion and channel performance.\n\n"
                f"### Data limitations\nSynthetic portfolio data is used. Retrieved documents provide contextual guidance, not external validation.")
