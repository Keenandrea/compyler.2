
.PHONY: help scanner clean

.DEFAULT: help
help:
	@echo "Program Invocation (Python 2.7):"
	@echo "	python scanner.py"
	@echo "	python scanner.py [file]"
	@echo "	python scanner.py < [file].fs19"

clean:
	rm -rf *.pyc
