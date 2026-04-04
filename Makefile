.PHONY: help download-video extract-frames detect-turns preview-region cache-clear
.PHONY: pipeline-youtube
.DEFAULT_GOAL := help

help: ## Show this help.
	@echo ""
	@echo "BD2 Helpers"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

cache-clear: ## Remove all cached data under .cache.
	rm -rf .cache

download-video: ## Download YouTube video into inputs/ (set YOUTUBE_URL or VIDEO_ID).
	@if [ -z "$(YOUTUBE_URL)" ] && [ -z "$(VIDEO_ID)" ]; then \
		echo "Set YOUTUBE_URL or VIDEO_ID to download a YouTube video."; \
		exit 1; \
	fi
	python3 scripts/bd2_download_youtube.py $(if $(YOUTUBE_URL),--youtube-url "$(YOUTUBE_URL)") $(if $(VIDEO_ID),--video-id "$(VIDEO_ID)")

extract-frames: ## Extract video frames (selects from inputs/ by default).
	python3 scripts/bd2_extract_frames.py

detect-turns: ## Run detection on existing frames (warn if missing).
	@if ! ls .cache/frames/**/frames.csv >/dev/null 2>&1; then \
		echo "Warning: no frames found in .cache/frames. Run 'make extract-frames' first."; \
	fi
	python3 scripts/bd2_detect_turns.py --use-cache

pipeline-youtube: ## Download YouTube video, extract frames, then detect turns.
	$(MAKE) download-video
	$(MAKE) extract-frames
	$(MAKE) detect-turns

preview-region: ## Save region crops only (no OCR).
	python3 scripts/bd2_detect_turns.py --use-cache --save-region --preview-only
