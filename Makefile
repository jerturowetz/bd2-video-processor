.PHONY: help download-video extract-frames detect-turns preview-region cache-clear cache-check
.PHONY: pipeline-youtube
.DEFAULT_GOAL := help

VIDEO_ID ?=
VIDEO_PATH ?=
YOUTUBE_URL ?=

ifeq ($(VIDEO_ID),)
ifneq ($(YOUTUBE_URL),)
VIDEO_ID := $(shell python3 -c "import sys,urllib.parse;u=urllib.parse.urlparse('$(YOUTUBE_URL)');q=urllib.parse.parse_qs(u.query);vid=q.get('v',[''])[0];print(vid or (u.path.lstrip('/') if u.netloc in ('youtu.be','www.youtu.be') else ''))")
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
 
cache-check: ## Prompt to clear cache if .cache exceeds 4GB.
	@size_kb=$$(du -sk .cache 2>/dev/null | awk '{print $$1}'); \
	if [ -z "$$size_kb" ]; then size_kb=0; fi; \
	if [ "$$size_kb" -ge 4194304 ]; then \
		echo ".cache is larger than 4GB ($$size_kb KB)."; \
		printf "Clear cache now? [y/N] "; \
		read ans; \
		case "$$ans" in y|Y) rm -rf .cache ;; *) echo "Keeping cache."; esac; \
	fi

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
	$(MAKE) cache-check
	$(MAKE) download-video
	$(MAKE) extract-frames $(if $(VIDEO_PATH),VIDEO_PATH="$(VIDEO_PATH)",)
	$(MAKE) detect-turns $(if $(VIDEO_ID),VIDEO_ID="$(VIDEO_ID)",)

preview-region: ## Save region crops only (no OCR).
	python3 scripts/bd2_detect_turns.py --use-cache --save-region --preview-only
