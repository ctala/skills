---
name: video-enhancer
description: Use when the user wants to enhance, upscale, or convert a local video to HD using the bundled cloud workflow. Triggers on requests like 视频超清, 视频增强, 转高清, 视频变清楚, 提升视频画质, video enhance, upscale video, make video clearer, convert to HD. Best for local video files when cloud upload and delayed processing are acceptable.
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["ffmpeg"]},"install":[{"id":"brew","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg"}]}}
---

# Video Enhancer

Enhance a local video using the bundled Python script and Wondershare-hosted cloud processing.

## Use This Skill When

Use this skill when the user wants to:
- Enhance a blurry or low-quality local video
- Upscale a local `.mp4` or `.mov` video
- Convert a local video to a clearer HD result using cloud processing

Do not use this skill when:
- The user wants a fully local or offline workflow
- The task is trimming, editing, subtitle work, or format conversion only
- The input is a remote URL instead of a local file
- The user does not accept third-party cloud upload

## Preconditions

Before running:
- Confirm the input file exists
- Confirm the file extension is `.mp4` or `.mov`
- Confirm `ffprobe` is available
- Tell the user this workflow uploads the source file to a third-party cloud service
- Use the skill only after the user accepts cloud processing
- Enforce these limits:
  - If `max(width, height) <= 1920`, duration must be `<= 300` seconds
  - If `max(width, height) > 1920`, duration must be `<= 60` seconds
- Refuse the request if any limit fails and explain which limit was exceeded

## Privacy and Network Disclosure

This workflow uploads the local video file and basic metadata to Wondershare-operated cloud endpoints.

Uploaded data includes:
- The source video file
- Video duration
- Video width and height
- File MD5 checksum

Network endpoints used by the bundled script:
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/resources/upload`
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/tasks`
- `https://filmora-cloud-api-alisz.wondershare.cc/open/v1/tasks/<task_id>`
- The final download URL returned by the task result

Do not use this skill for sensitive files unless the user explicitly accepts third-party processing.

## Permissions

This skill needs:
- Read access to the input video file
- Write access to the selected output directory
- Network access to Wondershare cloud endpoints
- Local `ffprobe` execution for metadata inspection

## Preferred Execution

Run the script using an absolute path:

```bash
python {baseDir}/scripts/video_enhance.py -i "/absolute/path/to/video.mp4" -o "/output/dir"
```

If the output directory is omitted, the script saves the enhanced file next to the input video.

## Workflow

1. Validate that the input file exists and has a supported extension
2. Read the local video metadata with `ffprobe`
3. Enforce duration and resolution limits
4. Upload the video file and metadata to the Wondershare cloud API
5. Submit the enhancement task
6. Poll until the task succeeds or fails
7. Download the enhanced result to the output directory
8. Report the saved file path to the user

## Input and Output

Input:
- Local video path
- Optional output directory

Output:
- Enhanced video saved to disk
- Filename pattern:

```text
<input_stem>_hd_YYYYMMDD_HHMMSS.<ext>
```

## Supported Formats

Supported input formats:
- `.mp4`
- `.mov`

## Practical Notes

- This is a cloud workflow, not an on-device enhancement pipeline
- Processing can take several minutes depending on file size and service load
- Large files are slower and more failure-prone
- Preserve the original file; the script writes a new output file

### Cloud Processing
- Videos are uploaded to filmora cloud services for AI enhancement
- Cloud providers temporarily store videos during processing
- Enhanced videos are downloaded to local storage
- Cloud-side data is deleted after processing completes

## Troubleshooting

Check that the file exists:

```bash
ls -lh "/absolute/path/to/video.mp4"
```

Check that `ffprobe` is available:

```bash
ffprobe -version
```

If the task fails:
- Verify network connectivity
- Re-run the script and inspect the error output
- Confirm the file is within the documented duration and format limits

## Script Location

Bundled script:
- `{baseDir}/scripts/video_enhance.py`

## Agent Guidance

- Always tell the user that the file will be uploaded to a third-party cloud service before running the workflow
- Do not add promotional links, referral tags, or unrelated product recommendations
- Keep the response focused on the saved file path and any relevant warnings
- For long-running tasks, provide progress updates instead of going silent
