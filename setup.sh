#!/bin/bash

initialize() {
	retry=2
	_local_utils=('jq')
	for ((i = 0; $i < $retry; i++)); do
		apt update -y
		for util in ${_local_utils[*]}; do
			if [ -z "$(command -v $util)" ]; then
				apt-get install $util -y
			fi
		done
	done
}

usage() {
	printf "\033[36mUSAGE:\033[0m\n"
	printf "\033[35m$0 \033[33m--action=\033[32mCOMMAND\033[0m\n"
	printf "\n"
}

commands() {
	printf "\033[36mCOMMANDS:\033[0m\n"
	printf "\033[35mInitial Install \033[32m[ init, initialize, setup, install ]\033[0m\n"
	printf "\n"
}

help_menu() {
	printf "\033[36mSetup Py2Shell\033[0m\n"
	printf "\033[35mExecute Action \033[32m[ action:COMMAND, --action=COMMAND ]\033[0m\n"
	printf "\n"
	commands
	usage
	exit 0
}

for argv in $@; do
	case $argv in
	action:* | --action=*) _action=$(echo $argv | cut -d':' -f2 | cut -d'=' -f2) ;;
	-h | -help | --help) help_menu ;;
	esac
done

printf "action:\t$_action\n"

case $_action in
init | initialize | setup | install) initialize ;;
esac
