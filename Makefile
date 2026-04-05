.PHONY: help download-video extract-frames detect-turns preview-region cache-clear
.PHONY: pipeline-youtube
.DEFAULT_GOAL := help

VIDEO_ID ?=
VIDEO_PATH ?=
YOUTUBE_URL ?=

ifeq ($(VIDEO_ID),)
ifneq ($(YOUTUBE_URL),)
VIDEO_ID := $(shell python3 -c "import sys,urllib.parse;u=urllib.parse.urlparse('$(YOUTUBE_URL)');q=urllib.parse.parse_qs(u.query);print(q.get('v',[''])[0])")
endif
endif

ifeq ($(VIDEO_PATH),)
ifneq ($(VIDEO_ID),)
VIDEO_PATH := inputs/$(VIDEO_ID).mp4
endif
endif

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

extract-frames: ## Extract video frames (set VIDEO_PATH to avoid picker).
	python3 scripts/bd2_extract_frames.py $(if $(VIDEO_PATH),$(VIDEO_PATH),)

detect-turns: ## Run detection on existing frames (set VIDEO_ID or FRAMES_CSV).
	@if ! ls .cache/frames/**/frames.csv >/dev/null 2>&1; then \
		echo "Warning: no frames found in .cache/frames. Run 'make extract-frames' first."; \
	fi
	python3 scripts/bd2_detect_turns.py --use-cache $(if $(FRAMES_CSV),--frames-csv "$(FRAMES_CSV)",) $(if $(VIDEO_ID),--video-id "$(VIDEO_ID)",)

pipeline-youtube: ## Download YouTube video, extract frames, then detect turns.
	$(MAKE) download-video
	$(MAKE) extract-frames $(if $(VIDEO_PATH),VIDEO_PATH="$(VIDEO_PATH)",)
	$(MAKE) detect-turns $(if $(VIDEO_ID),VIDEO_ID="$(VIDEO_ID)",)

preview-region: ## Save region crops only (no OCR).
	python3 scripts/bd2_detect_turns.py --use-cache --save-region --preview-only
