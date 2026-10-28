# Makefile for Automatic Christmas Bell - Arduino CLI
# Usage: make [target]

# Configuration
BOARD ?= arduino:avr:uno
PORT ?= /dev/ttyACM0
FQBN ?= $(BOARD)
SKETCH = src/firmware/buttons.ino
BAUD ?= 115200

# Common targets
.PHONY: all compile upload monitor clean

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
	@echo "  boards      - List available boards"
	@echo "  ports       - List available ports"
	@echo ""
	@echo "Usage examples:"
	@echo "  make                       # Compile and upload to default board"
	@echo "  make BOARD=arduino:avr:nano upload  # Upload to Nano"
	@echo "  make PORT=/dev/ttyUSB0 upload        # Upload to specific port"
	@echo "  make clean upload                   # Clean and upload"
