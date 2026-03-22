---
name: Audio-Segmenter
description: |-
  支持单个文件或整个文件夹，自动保留原始目录结构。
  未指定输出路径时：单文件输出到源目录，文件夹自动创建「原文件夹名_sliced_audio」。
  首次运行自动下载 ffmpeg（通过 ffmpeg-downloader），无需手动安装。
metadata:
  openclaw:
    requires:
      bins:
        - python
---

# Audio-Segmenter

**功能**：一键把长音频切成固定时长的片段，专为语音训练、素材整理、翻唱/Karaoke 准备、数据集制作设计。完美保持原文件夹结构 + 智能默认输出路径 + 自动处理 ffmpeg。

## 支持的音频格式
.mp3 / .wav / .m4a / .ogg / .flac / .aac / .wma 等（pydub 支持的所有常见格式）

## 参数说明（默认值）
1. **-i** → 输入路径（必填，支持单个文件或文件夹）
2. **-d** → 每段切片时长（秒），默认 60
3. **-o** → 输出目录（不传则智能选择）
4. **-r** → 文件夹模式下是否递归子文件夹（默认否）

## 执行步骤
1. **解析目录**：自动识别用户的源路径（单个音频文件 或 整个文件夹）。
2. **默认目标**：若未指定 -o，则：单文件 → 输出到源文件同一目录、文件夹 → 在输入同级创建 [输入文件夹名]_sliced_audio，并完全保留原始子目录结构。
3. **调用命令**：使用以下兼容性命令启动脚本（优先 python3，失败则 python）。脚本会自动创建虚拟环境、检测并下载 ffmpeg。

   ```bash
   (python3 ./skills/AudioSlicer/scripts/audio_slicer.py -i "<输入路径>" [-d <切片秒数>] [-o "<输出目录>"] [-r]) || (python ./skills/AudioSlicer/scripts/audio_slicer.py -i "<输入路径>" [-d <切片秒数>] [-o "<输出目录>"] [-r])