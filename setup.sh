#!/bin/bash

template_dir="templates"
main_app='py2shell.py'

error(){
	printf "\033[35mError:\t\033[31m${1}!\033[0m\n"
	exit 1
}

init_templates(){
	userpath="${HOME}/.py2shell"
	if [ ! -d "${userpath}" ];
	then
		mkdir -vp "${userpath}"
	fi
	if [ -d "${template_dir}" ];
	then
		printf "\033[1;36mGenerating, $(ls ${template_dir} | wc -l) templates\033[0m\n"
		cp -a -v "${template_dir}" "${userpath}"
	else
		error "Missing or unable to locate templates directory"
	fi
}

initialize() {
	retry=2
	_local_utils=('jq')
	for ((i = 0; $i < $retry; i++)); do
		sudo apt update -y
		for util in ${_local_utils[*]}; do
			if [ -z "$(command -v $util)" ]; then
				sudo apt-get install $util -y
			fi
		done
	done
	if [ -f "${main_app}" ]; then
		printf "\033[33mMaking \033[35m${main_app} \033[33mexecutable...\033[0m\n"
		sudo chmod a+x "${main_app}"
	fi
	init_templates
	printf "\033[32mInitialization process is complete!!!\033[0m\n"
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
	action:*|--action=*) _action=$(echo $argv | cut -d':' -f2 | cut -d'=' -f2);;
	-h|-help|--help) help_menu;;
	esac
done

case $_action in
	init|initialize|setup|install) initialize;;
esac
