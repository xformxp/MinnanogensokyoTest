# Options
PY			:= python
PYFLAGS		:= -m compileall
FILES		:= $(shell find *.py)
RUNFILES	:= $(patsubst %.py, %.pyc, $(FILES))

# Compile
compile				: $(RUNFILES)

%.pyc		: %.py
	@mkdir -p runfile
	@$(PY) $(PYFLAGS) $<

run					: compile
	@python main.pyc

list				:
	@echo $(FILES)

clean				:
	@rm -rf $(RUNFILES)

cleanlog			:
	@rm -rf log/*.log

logout				: clean
	@rm -rf user.inf
