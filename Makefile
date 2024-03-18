PROGNAME = "py2shell"
TESTNAME = "my_first_test"
TMPLNAME = "default::template_data"

all: setup test
	@printf "\033[2;35mSuccessfully, completed the setup process!\033[0m\n"

setup:
	@printf "\033[2;35mStarting, setup process...\033[0m\n"
	@./setup.sh --action=initialize

test:
	@printf "\033[1;35mRunning, $(PROGNAME) test(s)\033[0m\n"
	@./py2shell.py --templates
	@printf "\033[35mCreating, script $(TESTNAME), with $(TMPLNAME) and making it executable...\033[0m\n"
	@./py2shell.py --output $(TESTNAME).sh --datasource $(TMPLNAME) --make-executable
	@./scripts/$(TESTNAME).sh
