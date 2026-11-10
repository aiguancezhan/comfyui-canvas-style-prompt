# -*- coding: utf-8 -*-
"""Canvas Style Prompt - 画布风格提示词节点（极简版 / 社区发布版）
从画布项目的 74 种风格圣经(styles.json)里下拉选一个, 输入主体提示词,
节点把「风格段 + 主体」直接拼接输出, 不跑任何模型。
风格段 = visualStyle + colorGrading + lighting + cameraLanguage + postTexture。
输出可直接接 TextEncodeQwenImage21 等文本编码节点。
下拉按大类分组: 【电影写实】real / 【二次元插画】2d / 【3D渲染】3d。

2026-11-10 极简化:
- 移除 style_source 四来源(本地模型推理 / API 推理 / 直通)、LLM/GGUF/编码器加载、
  视觉 image 输入、模板分档、采样参数、自定义风格上传接口与前端显隐脚本。
- 只保留最初的核心玩法: 选风格 -> 拼接 -> 出提示词。
- 需要提示词扩写/走本地模型推理的, 用独立的文本生成节点(如 TextGenerateLTX2Prompt),
  在工作流里用开关自行切换「风格节点 / 扩写节点」两条链。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
STYLES_JSON = os.path.join(HERE, "styles.json")

_BIBLE_FIELDS = ("visualStyle", "colorGrading", "lighting", "cameraLanguage", "postTexture")
_CAT_ORDER = ("real", "2d", "3d")
_CAT_LABEL = {"real": "电影写实", "2d": "二次元插画", "3d": "3D渲染"}

_LOG_PREFIX = "[canvas-style-prompt]"


def _load_styles():
    with open(STYLES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("styles") or list(data.values())[0]
    out = {}
    for it in items:
        out[it["id"]] = {
            "name": it.get("name", it["id"]),
            "cat": it.get("category", ""),
            "bible": it.get("bible", {}),
        }
    return out


_STYLES = _load_styles()


def _build_choices():
    """按大类分组排序的全部风格下拉项。"""
    out = []
    for cat in _CAT_ORDER:
        label = _CAT_LABEL.get(cat, cat)
        for sid, v in _STYLES.items():
            if v["cat"] != cat:
                continue
            out.append("【%s】%s [%s]" % (label, v["name"], sid))
    # 兜底: 有风格不属于三个已知大类, 追加在尾部
    known = set(_CAT_ORDER)
    for sid, v in _STYLES.items():
        if v["cat"] not in known:
            out.append("%s [%s]" % (v["name"], sid))
    return out


_CHOICES = _build_choices()


def _style_para(sid: str) -> str:
    st = _STYLES.get(sid)
    if not st:
        return ""
    parts = []
    for field in _BIBLE_FIELDS:
        val = (st["bible"].get(field) or "").strip()
        if val:
            parts.append(val)
    return "\n".join(parts)


def _parse_style_id(style: str) -> str:
    return style.rsplit("[", 1)[-1].replace("]", "").strip() if "[" in style else style


class CanvasStylePrompt:
    """全部 74 风格，按【电影写实】【二次元插画】【3D渲染】分组。纯拼接，无模型推理。"""

    CHOICES = _CHOICES

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style": (cls.CHOICES,),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("prompt_full", "style_only")
    FUNCTION = "assemble"
    CATEGORY = "canvas"

    @staticmethod
    def VALIDATE_INPUTS(style):
        # 兼容新旧两种下拉值: 有没有【大类】前缀都认, 按 [id] 解析
        # 注意: ComfyUI 拿类直接调它(不传实例), 必须是 staticmethod
        if _parse_style_id(style) not in _STYLES:
            return "未知风格 id: %s (styles.json 里没有)" % style
        return True

    def assemble(self, style, prompt):
        prompt = (prompt or "").strip()
        sid = _parse_style_id(style)
        style_para = _style_para(sid)
        full = (style_para + "\n\n" + prompt) if (style_para and prompt) else (style_para or prompt)
        preview = " ".join(full.split())
        if len(preview) > 80:
            preview = preview[:80] + "…"
        print("%s 路径=内置拼接 | 风格=%s | 风格段 %d 字 | 主体 %d 字 | 输出 %d 字 | 预览=%s"
              % (_LOG_PREFIX, sid, len(style_para), len(prompt), len(full), preview), flush=True)
        return (full, style_para)


NODE_CLASS_MAPPINGS = {
    "CanvasStylePrompt": CanvasStylePrompt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CanvasStylePrompt": "画布风格提示词 (74风格)",
}
