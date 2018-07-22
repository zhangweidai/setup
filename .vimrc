" Peter's Vim File "
set t_Co=256
execute pathogen#infect()

fixdel
syntax on
highlight comment ctermfg=white guifg=white

let MRU_Max_Entries = 600

set autochdir
set autoindent
set backspace=indent,eol,start
set cindent
set cul
set et
set hidden              " allow jumping without needing to save first
set hlsearch            " Highlight my search results "
set ic
set incsearch
set lazyredraw
set nofoldenable    " disable folding
set nu
set pastetoggle=<F11>
set ruler               " See important file information at the bottom of vim "
set scrolloff=10
set shiftwidth=4
set smartcase
set tabstop=4
set title
set ff=unix

let comment_str = "# "

" intelligent comments based on file type

" Syntax Highlighting on relevant files "
au WinEnter,BufRead,BufNewFile *.txt     set filetype=c
au WinEnter,BufRead,BufNewFile *.wiki    set filetype=c
au WinEnter,BufRead,BufNewFile *.dofile  set filetype=c
au WinEnter,BufRead,BufNewFile *.hotkeys set filetype=c
au WinEnter,BufRead,BufNewFile *.ampl*   set filetype=c
au WinEnter,BufRead,BufNewFile *.qual    set filetype=c
au WinEnter,BufRead,BufNewFile *.input   set filetype=c
au WinEnter,BufRead,BufNewFile *.diff    set filetype=c
au BufReadPost        *         if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif 

filetype plugin on

au FileType python setlocal smartindent shiftwidth=4 ts=4 et cinwords=if,elif,else,for,while,try,except,finally,def,class

" Debug macros - Bind F# Hot Keys to put text where the cursor is. "
nmap "w           bi"<Esc>ea"<Esc>
nmap (w           bi(<Esc>ea)<Esc>
nmap ,g           :MRU<cr>
nmap <F12>        o$writeln($strcat("Dbg f: ", "<C-R>% : <Esc>:r! date<Esc><Esc>k<S-J>o : "));<Esc>k<S-J>
nmap <F2>         oqDebug()<<"//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"  ";<Esc>
nmap <F3>         ostd::cout<<"\033[33m//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"  "<<"\033[0m"<<std::endl;<Esc>
nmap <F4>         ostd::cout<<"\033[31m//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"  "<<"\033[0m"<<std::endl;<Esc>
nmap <F5>         ostd::cout<< " VAR: " << VAR <<std::endl;<Esc>
nmap <F6>         ostd::cout<<"\033[36m//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"  "<<"\033[0m"<<std::endl;<Esc>
nmap <F7>         ostd::cout<<"\033[37m//Dbg-"<<__FILE__<<"\""<< __LINE__<<"\"  "<<"\033[0m"<<std::endl;<Esc>
nmap <F8>         o$writeln($strcat("--------------- ", " : " ));<Esc>
nmap <F9>         o$writeln($strcat("Dbg file: ", "<C-R>% : "));<Esc>
nmap <S-Left>     0dw<Esc>
nmap <S-Right>    0i<Tab><Esc>
nmap <c-l>        bywofor (i = 0; i < length(<Esc>pa); i = i + 1)<Esc>o{<Esc>o}<Esc>
nmap <c-n>        nzz
" map <c-p>         "*p
imap <S-Insert>   <Esc>"*p
nmap <c-space>    bywostd::cout<<"\033[32m//Dbg-"<<__FILE__<<"\""<< __LINE__<<" <Esc>pA "<<"\033[0m"<<<Esc>pA <<std::endl;<Esc>

nmap <leader>bb   :let @* = expand('%:p')<cr>:call ExecExtension()<cr>
nmap <leader>cf   :let @d = expand('%:p')<cr>o<esc>"dp<esc>:set clipboard=unnamed<cr>dd<esc>:set clipboard=<cr>
nmap <leader>d    :write!<cr>:!cd '%:p:h'; mkd<CR>
nmap <leader>f    :echo expand('%:p')<Esc>
nmap <leader>r    :NERDTreeFind<CR>
nmap <leader>w    :!
nmap <leader>a    :<Up><cr>
nmap <leader>s    :sp<CR>
nmap <leader>sp   :call Spellcheck()<CR>
nmap <s-tab>      <c-w><up>
nmap <space>      :call DebugExtension()<cr>
nmap <tab>        <c-w>w
nmap XX           :q!<cr>
nmap dc           yyp<m-up>kkw
nmap [{           ][=%''zz
nmap st           :FufTag<CR>
nmap <s-i>        o<Esc>
vmap i            I
nmap s            :write!<cr>
nmap <leader>]    [[=%''zz
map m $
map <m-up>        :call CommentStr()<cr>0i<C-r>=comment_str<Esc><Esc>j
map <m-down>      0xxj
map <m-h>         0xxx
map <m-l>         0i<tab><Esc>
imap <m-h>        <Esc>0xxx
imap <m-l>        <Esc>0i<tab><Esc>
nmap <leader>se   :!gnome-terminal --working-directory '%:p:h' -x tcsh -c "grf '<cword>'; /bin/tcsh -i"&<cr>
nmap <leader>sl   :!gnome-terminal --working-directory '%:p:h' -x tcsh -c "grf '<cword>'; /bin/tcsh -i"&<cr>
nmap <leader>tkd  :!tkdiff '%' & <cr>
nmap <silent> <leader><leader>t    :silent !gnome-terminal --working-directory '%:p:h'&<cr>
nmap <leader>go    :exe "!firefox -search '<cword>' &"<cr>

" work specific
nmap ,s           :find  %:t:r.c*<cr>
nmap ,h           :find  %:t:r.h<cr>
nmap ,H           :sfind %:t:r.h<cr>
" cnoreabbrev w :echo noop please use "s"
" cnoreabbrev w! :echo noop please use "s"
noremap! <C-Y> <Esc>klyWjpa

inoremap <m-h>    <Esc>0dw
inoremap <s-BS>   <C-O>x
inoremap <m-BS>   <C-O>h<C-O>daw
inoremap <c-BS>   <C-O>h<C-O>daw
" inoremap PP       <C-O>p

set undodir=~/.vim/undo
set undofile 

nmap <silent><S-Down> <C-T>
nmap <silent><S-Up> <C-]>
"
" File navigation macros - Jump to the declaration of the function with holding Shift and Up/Down while cursor is on a function name. "

"
"Allow faster screen movement with cursor movement when holding Control and Up/Down "
"
fu! s:Saving_scroll(cmd)
  let save_scroll = &scroll
  execute 'normal! ' . a:cmd
  let &scroll = save_scroll
endf
nnoremap <C-Down> :call <SID>Saving_scroll("5<C-V><C-D>")<CR>
vnoremap <C-Down> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-D>")<CR>
nnoremap <C-Up> :call <SID>Saving_scroll("5<C-V><C-U>")<CR>
vnoremap <C-Up> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-U>")<CR>
nnoremap <C-K> :call <SID>Saving_scroll("10<C-V><C-U>")<CR>
vnoremap <C-K> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-U>")<CR>
nnoremap <C-J> :call <SID>Saving_scroll("10<C-V><C-D>")<CR>
vnoremap <C-J> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-D>")<CR>

autocmd FileType make setlocal noexpandtab

fu! Spellcheck()
   set syntax=off
	setlocal spell spelllang=en_us
endf


fu! CommentStr()
   let filestr = expand('%:f')
   let exten = expand('%:e')
   if filestr =~ "vimrc"
      let g:comment_str = "\""
   elseif exten =~ "py"
      let g:comment_str = "#"
   elseif exten =~ "js"
      let g:comment_str = "//"
   elseif exten =~ "bat"
      let g:comment_str = "REM "
   elseif exten =~ "ahk"
      let g:comment_str = "; "
   endif
endf


fu! DebugExtension()
   if expand('%:p') =~ ".ahk"
      norm bywoMsgBox, %
      :norm pA%
   elseif expand('%:p') =~ ".py"
      norm bywoprint("
      :norm pA:" + 
      :norm pA)
   else
      norm bywo$writeln($strcat("Dbg f: ", "<C-R>% : <Esc>pA ", <Esc>pA));<Esc>
   endif 
endf


fu! ExecExtension()
   if expand('%:p') =~ ".ahk"
      :silent !"C:\Program Files\AutoHotkey\AutoHotkey.exe" %:p
   elseif expand('%:p') =~ ".py"
      :silent !python -i %:p
   else
   	:silent !wscript "C:\Users\Peter\Documents\send.vbs"
   endif 
endf


nmap j gj
nmap k gk
call arpeggio#map('i', '', 0, 'jk', '<Esc>')
call arpeggio#map('c', '', 0, 'jk', '<Esc>')
au WinEnter,BufRead,BufNewFile *   :cd %:p:h
"
" things to remember
"
   " :VCSBlame " blame
   " :set ul=0 | edit
   " :AnsiEsc
"



let g:airline_powerline_fonts = 1
set encoding=utf-8
set laststatus=2
let g:airline_theme='xtermlight'
:colo molokai

hi IndentGuidesOdd  ctermbg=black
hi IndentGuidesEven ctermbg=darkgrey
let g:indent_guides_start_level=2
let g:indent_guides_guie_size=1
