# setup
sudo add-apt-repository ppa:jonathonf/vim
sudo apt-get update

sudo apt-get install xclip
sudo apt-get install silversearcher-ag
sudo apt install exuberant-ctags
sudo apt install vim
sudo apt install gitk
mkdir $HOME/.undo
cd $HOME
ln -sf ./setup/.bashrc
ln -sf ./setup/.bash_aliases
ln -sf ./setup/.vim
ln -sf ./setup/.vimrc
ln -sf ./setup/.gitconfig
