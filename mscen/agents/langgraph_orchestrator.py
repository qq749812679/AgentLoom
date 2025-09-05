from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from langgraph.graph import StateGraph, START, END

from ..image_gen import generate_scene_image
from ..music_gen import generate_music_from_theme
from ..lighting import generate_lighting_from_theme, save_lighting_program
from ..wled import save_wled_preset
from ..video import compose_image_music_to_mp4
from .llm_planner import LLMPlanner
from ..core.logger import JsonlLogger


def build_graph(outputs_dir: Path, logger: JsonlLogger):
    llm_planner = LLMPlanner(logger)
    
    def plan_node(state: Dict[str, Any]) -> Dict[str, Any]:
        goal = state.get("goal", "")
        use_llm = state.get("use_llm", False)
        
        if use_llm:
            try:
                result = llm_planner.plan(goal, context=state)
                return {**state, "plan": result.get("plan", ["image", "music", "lighting"]), 
                       "theme": result.get("theme", goal), "reasoning": result.get("reasoning", "")}
            except Exception as e:
                logger.log({"event": "plan_fallback", "error": str(e)})
        
        # Fallback heuristic planner
        return {**state, "plan": ["image", "music", "lighting"], "theme": goal, "reasoning": "使用默认规划"}

    def image_node(state: Dict[str, Any]) -> Dict[str, Any]:
        theme = state.get("theme", "")
        img = generate_scene_image(theme, size=(896, 512))
        path = outputs_dir / "lg_image.png"
        img.save(path)
        return {**state, "image_path": path}

    def music_node(state: Dict[str, Any]) -> Dict[str, Any]:
        theme = state.get("theme", "")
        duration = float(state.get("duration", 20.0))
        wav = generate_music_from_theme(theme, duration_s=duration, out_dir=outputs_dir)
        return {**state, "music_path": wav}

    def lighting_node(state: Dict[str, Any]) -> Dict[str, Any]:
        theme = state.get("theme", "")
        frames = generate_lighting_from_theme(theme)
        path = save_lighting_program(frames, outputs_dir, filename="lg_lighting.json")
        wled_path = save_wled_preset(frames, outputs_dir, filename="lg_wled.json")
        return {**state, "lighting_path": path, "wled_path": wled_path}

    def video_node(state: Dict[str, Any]) -> Dict[str, Any]:
        img_path = state.get("image_path")
        music_path = state.get("music_path")
        if img_path and music_path:
            video_path = outputs_dir / "lg_video.mp4"
            try:
                compose_image_music_to_mp4(img_path, music_path, video_path, fps=30)
                return {**state, "video_path": video_path}
            except Exception as e:
                logger.log({"event": "video_node.error", "error": str(e)})
        return state

    def route_after_plan(state: Dict[str, Any]) -> str:
        plan = state.get("plan", [])
        if "image" in plan:
            return "image"
        elif "music" in plan:
            return "music"
        elif "lighting" in plan:
            return "lighting"
        else:
            return END

    g = StateGraph(dict)
    g.add_node("plan", plan_node)
    g.add_node("image", image_node)
    g.add_node("music", music_node)
    g.add_node("lighting", lighting_node)
    g.add_node("video", video_node)
    
    g.add_edge(START, "plan")
    g.add_conditional_edges("plan", route_after_plan, ["image", "music", "lighting", END])
    g.add_edge("image", "music")
    g.add_edge("music", "lighting")
    g.add_edge("lighting", "video")
    g.add_edge("video", END)
    return g.compile()


