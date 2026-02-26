PROGNAME = "py2shell"
TESTNAME = "my_first_test"
TMPLNAME = "default::template_data"

.PHONY: all setup resync test

all: setup test
	@printf "\033[2;35mSuccessfully, completed the setup process!\033[0m\n"

setup:
	@printf "\033[2;35mStarting, setup process...\033[0m\n"
	@./setup.sh --action=initialize

resync:
	@printf "\033[2;35mResync Templates...\033[0m\n"
	@./setup.sh --action=resync

test:
	@printf "\033[1;35mRunning, $(PROGNAME) test(s)\033[0m\n"
	@./py2shell.py --templates
	@printf "\033[35mCreating, script $(TESTNAME), with $(TMPLNAME) and making it executable...\033[0m\n"
	@./py2shell.py --output $(TESTNAME).sh --datasource $(TMPLNAME) --make-executable
	@./scripts/$(TESTNAME).sh
