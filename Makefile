# Makefile for Automatic Christmas Bell - Arduino CLI
# Usage: make [target]

# Configuration
BOARD ?= arduino:avr:uno
PORT ?= /dev/ttyACM0
FQBN ?= $(BOARD)
SKETCH = src/firmware/buttons.ino
BAUD ?= 115200

# Common targets
.PHONY: all compile upload monitor clean publish publish-draft publish-built

all: compile upload

# Compile the sketch
compile:
	arduino-cli compile --fqbn $(FQBN) $(SKETCH)

# Upload to Arduino
upload: compile
	arduino-cli upload -p $(PORT) --fqbn $(FQBN) $(SKETCH)

# Open serial monitor
monitor:
	arduino-cli monitor -p $(PORT) -b $(BAUD)

# Clean build files
clean:
	rm -rf .pio

# Publish the manufacturing files of every board's current release as a GitHub pre-release (docs/decisions.md D-22):
# edakit release verify on the order files, build/publish/<tag>/, tag = the date
publish:
	python3 tools/publish_release.py

# The same as a draft release only the account sees – a test; delete it afterwards (the script says how)
publish-draft:
	python3 tools/publish_release.py --draft

# A board of release TAG has been built and works: drop the pre-release mark
publish-built:
	@test -n "$(TAG)" || { echo "usage: make publish-built TAG=<tag>"; exit 1; }
	gh release edit $(TAG) --prerelease=false

# Show available boards
boards:
	arduino-cli board list

# Show available ports
ports:
	arduino-cli board listall

# Show help
help:
	@echo "Available targets:"
	@echo "  all         - Compile and upload"
	@echo "  compile     - Compile only"
	@echo "  upload      - Upload only"
	@echo "  monitor     - Open serial monitor"
	@echo "  clean       - Clean build files"
	@echo "  publish     - Publish the boards' manufacturing files as a GitHub pre-release"
	@echo "  publish-draft - The same as a draft, for a test"
	@echo "  publish-built TAG=<tag> - Drop the pre-release mark after a board was built"
	@echo "  boards      - List available boards"
	@echo "  ports       - List available ports"
	@echo ""
	@echo "Usage examples:"
	@echo "  make                       # Compile and upload to default board"
	@echo "  make BOARD=arduino:avr:nano upload  # Upload to Nano"
	@echo "  make PORT=/dev/ttyUSB0 upload        # Upload to specific port"
	@echo "  make clean upload                   # Clean and upload"
