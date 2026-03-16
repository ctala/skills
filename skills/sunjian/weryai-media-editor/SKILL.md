# WeryAI Media Editor Toolkit

<description>
Provides advanced AI media manipulation: Upscaling, Background Removal, Image-to-Video (I2V), and Face Swapping.
</description>

<usage>
```bash
# 1. Upscale / Enhance Quality
node /Users/king/weryai-media-editor-skill/weryai-media-editor.js upscale <image_url>

# 2. Remove Background
node /Users/king/weryai-media-editor-skill/weryai-media-editor.js remove-bg <image_url>

# 3. Image to Video (I2V)
node /Users/king/weryai-media-editor-skill/weryai-media-editor.js i2v <image_url> "<optional_english_prompt>"

# 4. Face Swap
node /Users/king/weryai-media-editor-skill/weryai-media-editor.js face-swap <target_image_url> <source_face_url>
```
</usage>

<rules>
1. For I2V prompts, translate to English first.
2. The script outputs "Success! Result: <URL>".
3. If the result is an image, render it as `![Result](<URL>)`.
4. If the result is a video, return the raw URL.
</rules>