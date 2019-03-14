# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
PATH="$HOME/.local/bin:$HOME/bin:$HOME/Scripts:$PATH"
export PATH
# Displya directory in the terminal prompt
# export PS1="\u@\h \e[0;36m \w \e[m>"
export PS1="\[\u\] \e[0;36m\w\e[m > "
#export PATH="~/.config/polybar/polybar-themes/polybar-2/scripts:$PATH"

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

############################################################
                       # Aliases #
############################################################
# Replacement for existing temrinal commands
alias vi='vimx'
alias vim='vimx'
alias ls='ls --color=auto'
alias ll='ls -l'
alias rxrdb='xrdb $HOME/.config/Xresources/.Xresources'
alias testpoly='polybar main -c $HOME/.config/polybar/test '
# Shortcut commands
#   Direct vim commands
alias gXresources='vimx $HOME/.config/Xresources/.Xresources'
alias gi3='vimx /home/jongwoongto/.config/i3/config'
alias gurxvt='vimx $HOME/.config/Xresources/urxvt/custom'
alias grofi='vimx ~/.config/Xresources/rofi/cusom'
alias gcompton='vimx ~/.config/compton.conf'
alias wiki='vimx ~/vimwiki/index.wiki'
#   Open dir commands
alias gkitty='cd ~/.config/kitty && ls'
alias gpoly='cd ~/.config/polybar && ls'
alias gscript='cd ~/Documents/Script_Prac && ls'
#Not sure why this is here for...
alias sudo='sudo '
alias dotsync='dotfiles_sync.sh'
