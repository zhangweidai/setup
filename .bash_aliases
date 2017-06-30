
# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

alias uplinux='sudo apt-get update; sudo apt-get upgrade; sudo apt-get dist-upgrade'
alias dmouse='xinput disable "ETPS/2 Elantech Touchpad"'
alias emouse='xinput enable "ETPS/2 Elantech Touchpad"'
alias cds='cd $HOME/setup'
alias cdss='cd $HOME/setup'
alias mk='make'

alias hi="history"
alias gvim="vim"
alias b="cd .."
alias bb="cd ../.."
alias bbb="cd ../../.."
alias bbbb="cd ../../../.."
alias vcs="vim ~/.bashrc"
alias vcsa="vim ~/.bash_aliases"
alias vrc="vim ~/.vimrc"
alias sl="ssh pzhang@skyline.wv.mentorg.com"
alias psx="ps -aux"
alias grf='vimack.sh'
alias ll='/bin/ls --color=always -all -h'
alias ls='/bin/ls --color=always '
alias vi='bash $HOME/setup/bin/gvimscript.sh '
alias kill='kill -9'
alias vcin='vim ~/setup/notes'
alias py='python'
export TS="/tmp"

# get current branch in git repo
function parse_git_branch() {
	BRANCH=`git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`
	if [ ! "${BRANCH}" == "" ]
	then
		echo "[${BRANCH}]"
	else
		echo ""
	fi
}

# get current status of git repo
function parse_git_dirty {
	status=`git status 2>&1 | tee`
	dirty=`echo -n "${status}" 2> /dev/null | grep "modified:" &> /dev/null; echo "$?"`
	untracked=`echo -n "${status}" 2> /dev/null | grep "Untracked files" &> /dev/null; echo "$?"`
	ahead=`echo -n "${status}" 2> /dev/null | grep "Your branch is ahead of" &> /dev/null; echo "$?"`
	newfile=`echo -n "${status}" 2> /dev/null | grep "new file:" &> /dev/null; echo "$?"`
	renamed=`echo -n "${status}" 2> /dev/null | grep "renamed:" &> /dev/null; echo "$?"`
	deleted=`echo -n "${status}" 2> /dev/null | grep "deleted:" &> /dev/null; echo "$?"`
	bits=''
	if [ "${renamed}" == "0" ]; then
		bits=">${bits}"
	fi
	if [ "${ahead}" == "0" ]; then
		bits="*${bits}"
	fi
	if [ "${newfile}" == "0" ]; then
		bits="+${bits}"
	fi
	if [ "${untracked}" == "0" ]; then
		bits="?${bits}"
	fi
	if [ "${deleted}" == "0" ]; then
		bits="x${bits}"
	fi
	if [ "${dirty}" == "0" ]; then
		bits="!${bits}"
	fi
	if [ ! "${bits}" == "" ]; then
		echo " ${bits}"
	else
		echo ""
	fi
}

alias filesThatContain="grep -Rl" 
bind '"\C-u": kill-whole-line'
alias clipdir='echo -n `pwd` | xclip -i -sel p -f | xclip -i -f -sel c'
bind '"\C-k":"clipdir\n"'
export PATH="$HOME/setup/bin:$PATH"
export PS1="\n\[\e[33m\][ \h \[\e[33m\]]\[\e[m\]\`parse_git_branch\` \w \n\W$ "

alias py='python'
alias well='sudo uwsgi --http :80 --wsgi-file /home/peter/setup/python/hang.py'
alias well2='sudo uwsgi --http :80 --wsgi-file /home/peter/setup/python/hang2.py'

