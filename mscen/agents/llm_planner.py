from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

import openai
from tenacity import retry, stop_after_attempt, wait_exponential

from ..core.logger import JsonlLogger


SYSTEM_PROMPT = """你是一个多模态内容创作规划师。根据用户目标，制定图片、音乐、灯光、视频的生成计划。

可用工具：
- image: 生成场景图片
- music: 生成背景音乐
- lighting: 生成灯光节目
- video: 合成视频(需要图片+音乐)
- wled: 导出WLED预设
- voice_tts: 语音播报

安全要求：
- 拒绝暴力、仇恨、成人内容
- 避免版权争议的角色/品牌

输出JSON格式：
{
  "safe": true/false,
  "plan": ["tool1", "tool2", ...],
  "theme": "refined_theme",
  "reasoning": "why this plan"
}"""


class LLMPlanner:
    def __init__(self, logger: JsonlLogger, api_key: Optional[str] = None) -> None:
        self.logger = logger
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
    def plan(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        context = context or {}
        user_msg = f"用户目标: {goal}\n上下文: {context}"
        
        self.logger.log({"event": "llm_plan.request", "goal": goal})
        
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            result = json.loads(resp.choices[0].message.content)
            self.logger.log({"event": "llm_plan.ok", "plan": result.get("plan"), "safe": result.get("safe")})
            
            if not result.get("safe", True):
                raise ValueError("LLM判断内容不安全")
                
            return result
            
        except Exception as e:
            self.logger.log({"event": "llm_plan.error", "error": str(e)})
            # Fallback to heuristic
            return {
                "safe": True,
                "plan": ["image", "music", "lighting"],
                "theme": goal,
                "reasoning": f"LLM失败，使用默认规划: {e}"
            }
