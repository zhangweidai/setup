# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples
# find -name -type f -exec cp '{}' inner/ \;
# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
alias rg="ag"
export PATH=/usr/local/bin:/usr/bin:/home/pzhang/apps/gvim8/vim/src/bin:${PATH}
export PATH=/home/zoe/.local/bin:${PATH}

if [ -f ~/.bash_local ]; then
    . ~/.bash_local
fi

alias well='cd ~/setup2/python/zen; py bles.py'
alias welltf='python3 ~/setup/python/tf_check.py'
alias gopf='cd /mnt/c/Program\ Files'
alias gomc='cd /mnt/c/Users/pzhang'
alias gomc2='cd /mnt/c/Users/Zoe'
export DL='/mnt/c/Users/zoe/Documents'
export ANDROID_HOME='/mnt/c/Users/pzhang/AppData/Local/Android/Sdk'
alias go='source ~/setup/bin/go.bash'
alias py3='python3'
alias py='python3'
alias bpy='bpython'
alias p='ipython'
alias goz='cd /mnt/c/Users/Zoe/Desktop'

export CSCOPE_DB='/usr/local/lib/python2.7/dist-packages/cscope.out'
alias scopeme='find "$PWD/" -name "*.py" -o -iname "*.cfg" > cscope.files && cscope -bv -i cscope.files -f cscope.out'
alias pysite='python -m site'
alias vgitrc='vim ~/.gitconfig'

if [ `whoami` ==  "zoe" ]; then
    alias pl="cds; b; cd setup2; cd python/zen; py ~/setup2/python/zen/stock_plot.py"
    export PYTHONSTARTUP=~/setup2/python/zen/.pystart
    export SETUP="/home/zoe/setup2"
    alias cds="cd $SETUP"
else
    export PYTHONSTARTUP=~/setup/python/zen/.pystart
    alias pl="cds; cd python/zen; py ~/setup/python/zen/stock_plot.py"
fi
alias goa="cds; cd python/zen_dump/analysis"
alias go1="cds; cd python/zen"
alias go2="cd /mnt/c/Users/Zoe/Documents/setup/java/HelloWorld/app/src/main/java/com/example/pzhang222/helloworld"
alias gof="cds; cd python/zen_dump/final"
alias goh="cds; cd python/zen_dump/holdings"
alias god="cds; cd python/zen_dump"
export SPLIT="$SETUP/python/zen_dump/split"
alias goc="cd $SPLIT"
alias gop="cds; cd python/zen_dump/pkl"
alias goj="cds; cd java;"
alias gok="cds; cd kotlin;"
alias gokk="cd /home/zoe/git/kotlin-koans"
alias ipy="ipython3"
alias p="ipython3"
alias python="python3"
alias ka="killall python3"
alias checkout="git checkout --"
alias st2="git status -uno"
alias buy="py buy.py"
alias sell="py zen.py sell"
alias rsell="py zen.py rsell"
alias download="py z.py download"
alias wab="py zen.py wab"
alias wabp="py zen.py wabp --s"
alias buyl="py zen.py buy --date=l"
alias gbuy="go1; py gbuy.py"
alias owned="py buy.py --mode=owned"
alias orders="py buy.py --mode=order"
alias etfs="py buy.py --mode=etfs"
alias better="py buy.py --mode=better_etf"
alias mc="py buy.py --mode=mc"
alias all="py buy.py --mode=all"
alias one="all --live=True --drop=12"
alias two="better --live=True --drop=12"
alias accounts="py buy.py --mode=accounts"
alias bench="py buy.py --mode=benchmark"
alias live="py buy.py --live=True"
alias single="py buy.py --mode=single"
alias plot="py stock_plot.py"
alias multiple="py buy.py --mode=multiple"
alias special="py buy.py --mode=special"
alias notes="py buy.py --mode=notes"
alias worst="py buy.py --mode=worst"
alias rands="py buy.py --mode=rand"
alias sorted="py buy.py --mode=sorted"
alias daily="py buy.py --mode=daily"
alias gbuy2="py zen.py gbuy2"
alias gbuy2="py gbuy.py --skips=True"
alias well='cd ~/gits/manim; python -m manim example_scenes.py SquareToCircle -pl; '
alias well='cd ~/gits/manim; python -m manim example_scenes.py AAA -pl; '
alias well2='wsl-open /home/zoe/gits/manim/media/videos/example_scenes/2160p15/SquareToCircle.mp4'
alias well2='wsl-open /home/zoe/gits/manim/media/videos/example_scenes/480p15/AAA.mp4'
alias well='cd ~/setup/csharp; mcs hello.cs; mono hello.exe'
alias well='cd ~/setup/python/motivation; py main.py'
alias mko='cd ~/setup/csharp; mcs hello.cs'
alias gos='cd /mnt/c/Users/Zoe/SandBox'
alias delstock='py gained_discount.py --updatestocks=1 --delete'
alias gos2='cd /mnt/c/Users/Zoe/3D_SandBox'
#alias xdg-open='wsl-open'
#sudo -S true
set bell-style none

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="/home/zoe/.sdkman"
[[ -s "/home/zoe/.sdkman/bin/sdkman-init.sh" ]] && source "/home/zoe/.sdkman/bin/sdkman-init.sh"

LANG=en_US.utf8
export DISPLAY=:0.0
export PULSE_SERVER=tcp:localhost
alias  bd='python ~/setup2/python/bd.py'
# awk '{ print $1 }'
#go1
alias well='cd ~/setup2/python/; python watchfile.py'
