# canvas-style-prompt ｜ 画布风格提示词

一个 ComfyUI 自定义节点插件：从内置的 **74 种画布风格库**里挑一个风格，再输入一句主体提示词，
节点把「风格段 + 主体」**直接拼接**输出，不加载、不运行任何模型。输出可直接接到
`TextEncodeQwenImage21` 等文本编码节点。

## 效果示例

同一条主体提示词，只换下拉里的风格，其余全部不动：

> A white porcelain teacup on a wooden table, steam rising gently from the cup, a small spoon beside it, clean plain background, centered composition.

| 暗夜电影感 | 二次元插画 |
| --- | --- |
| ![暗夜电影感](examples/example-1-noir-night.png) | ![二次元插画](examples/example-2-anime.png) |

| 水墨写意 | 科技感电影 |
| --- | --- |
| ![水墨写意](examples/example-3-ink-wash.png) | ![科技感电影](examples/example-4-sci-fi.png) |

| 灾难写实 |
| --- |
| ![灾难写实](examples/example-5-disaster.png) |

## 节点

| 节点 | 说明 |
| --- | --- |
| 画布风格提示词 (74风格) | 全部 74 风格，按【电影写实】【二次元插画】【3D渲染】分组 |

### 输入

| 输入 | 说明 |
| --- | --- |
| `style` 风格 | 下拉选择，风格段取自该风格的风格圣经（视觉风格 / 色彩分级 / 光影 / 镜头语言 / 后期质感五段） |
| `prompt` 提示词 | 主体内容，多行文本 |

### 输出

| 输出 | 说明 |
| --- | --- |
| `prompt_full` | 风格段 + 空行 + 主体提示词（最终提示词） |
| `style_only` | 风格段原文（调试用） |

## 用法

1. 下拉选一个风格；
2. 在提示词框里写主体（只写"画什么"，风格交给风格段）；
3. `prompt_full` 接到文本编码节点即可。

### 想不带风格？

提示词框留空只输出风格段；只想要主体原文时，把节点旁路掉、直接用你的 Text 节点即可。
需要 LLM 扩写 / 本地模型推理提示词的，请使用独立的文本生成节点（如 `TextGenerateLTX2Prompt`），
在工作流里用开关自行切换「风格拼接 / 模型扩写」两条链——本插件不再内置推理功能。

## 执行日志

跑一次队列，ComfyUI 控制台会打一行日志，方便确认拼接结果：

```
[canvas-style-prompt] 路径=内置拼接 | 风格=real-techy | 风格段 368 字 | 主体 62 字 | 输出 432 字 | 预览=...
```

## 安装

任选其一：

1. **ComfyUI Manager**：Custom Nodes Managers → Install via Git URL → 粘贴本仓库地址；
2. **手动**：把本目录整体放进 `ComfyUI/custom_nodes/`，重启 ComfyUI；
3. **命令行**：`git clone 本仓库地址 ComfyUI/custom_nodes/canvas-style-prompt`，重启 ComfyUI。

无任何第三方依赖（纯 Python 标准库），任何能跑 ComfyUI 的环境（含云端平台）都可直接安装。

## 自定义风格

编辑插件目录下的 `styles.json` 即可增删改风格（每个条目含 `id` / `name` / `category` / `bible`），
改完重启 ComfyUI 生效。

## English

A minimal ComfyUI custom node with 74 built-in visual styles. Pick a style from the dropdown,
type your subject prompt, and the node outputs the plain concatenation of the style paragraph
and your prompt — no model inference involved.

- Inputs: `style` (dropdown, grouped into Realistic / Anime / 3D), `prompt` (multiline string).
- Outputs: `prompt_full` (style paragraph + prompt), `style_only` (the style paragraph alone).
- Styles live in `styles.json` (`id` / `name` / `category` / `bible`); edit the file and restart
  ComfyUI to apply changes.
- No third-party dependencies.

## Requirements

- ComfyUI

## License

MIT
