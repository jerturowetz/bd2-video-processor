For your use case (detecting turn boundaries from a UI element), the most reliable signal is the **bottom-right button with the turn number**. We should ignore the mid‑screen turn text since it’s often missing in captured frames.

## Detection goal
- Track the **bottom-right turn button** and its number.
- Define the turn boundary as **the last frame where the button for that turn is still visible** (i.e., “last-seen” of the current turn’s button).
- When the button disappears or changes to the next turn, that last-seen frame becomes the timestamp for the completed turn.

## Stack choice
- Use **ffmpeg + Python** together:
  - ffmpeg to sample frames at fixed FPS and optionally trim start/end.
  - Python to:
    - Invoke ffmpeg (subprocess or `ffmpeg-python`).
    - Call a vision model with frame images.
    - Run the “last-seen” state machine and format timestamps.

Pure ffmpeg cannot call a vision model or maintain detection state; Python gives you that control while still letting ffmpeg do the heavy lifting.

## Next step
Start with `scripts/bd2_extract_frames.py` (ffmpeg sampling) and `scripts/bd2_detect_turns.py` (vision + last‑seen logic) to wire the model call into the existing frame pipeline.

## Main OCR pass (turn detection)
Use the **padded, region-cropped images** for OCR. These crops contain the “Turn ##” button text (or are blank/nonsense between turns), so they are the correct inputs to send for analysis.

## Status / current focus
- **Now:** Button detection and region discovery/tuning for the bottom-right turn button.
- **Next:** Validate region across multiple frames, lock the final region, then run full OCR.
- **Later:** Refine this brief with finalized detection assumptions, thresholds, and full-run workflow.

## Final region padding (percent, relative to detected “TURN” crop)
- **Right:** +2.0% (`--region-expand-right 0.02`)
- **Left:** +0.5% (`--region-expand-left 0.005`)
- **Vertical (top+bottom):** +0.5% (`--region-expand-vertical 0.005`)
