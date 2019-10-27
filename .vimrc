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
set pastetoggle=<F12>
set ruler               " See important file information at the botom of vim "
set scrolloff=10
set expandtab
set shiftwidth=4
set smartcase
set tabstop=4
set softtabstop=4
set title
set fileformat=unix 
set smartindent

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

au FileType python setlocal cinwords=if,elif,else,for,while,try,except,finally,def,class

" Debug macros - Bind F# Hot Keys to put text where the cursor is. "
nmap "w           bi"<Esc>ea"<Esc>
nmap 'w           bi'<Esc>ea'<Esc>
nmap (w           bi(<Esc>ea)<Esc>
nmap %w           bi%<Esc>ea%<Esc>
nmap ,g           :MRU<cr>

" tab indentation
nmap <S-Left>     0dw<Esc>
nmap <S-Right>    0i<Tab><Esc>

" paste clipboard
inoremap <C-v> <C-r><C-o>+
imap <S-Insert>   <Esc>"*p
imap <c-j>   (<Esc>ea)<Esc>
imap <c-k>   ()<esc>
"imap <c-i>   []<esc>


" exec extension / reload vimrc
nmap <leader>b   :let @* = expand('%:p')<cr>:call ExecExtension()<cr>
nmap <silent> <leader><leader><leader> :source %:p<cr>

" copy file
nmap <leader>cf   :let @*=expand('%:p')<cr>
nmap <leader>cd   :let @*=expand('%:p:h')<cr>

" show file
nmap <leader>f    :echo expand('%:p')<Esc>

" debug extension
nmap <space>      :call DebugExtension()<cr>
nmap <leader><Space>  :call DebugExtension2()<cr>
nmap <leader>t     :call DebugExtension3()<cr>
nmap <s-l>          0i<tab><esc>
nmap <s-h>          0xxxx<esc>
nmap <leader>ex     0iraise SystemExit<esc>
nmap ;;             A:<esc>



" split tabbing
nmap <tab>        <c-w>w

" quit no save
nmap XX           :q!<cr>

" quit no save
nmap tt           :call Toggler()<cr>

" fast saving
nmap s            :write!<cr>

" fast end of the line
map m $

" fast scrolling
nnoremap <C-K> :call <SID>Saving_scroll("10<C-V><C-U>")<CR>
vnoremap <C-K> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-U>")<CR>
nnoremap <C-J> :call <SID>Saving_scroll("10<C-V><C-D>")<CR>
vnoremap <C-J> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-D>")<CR>
vnoremap c "*y


" other
nmap <c-space>    bywostd::cout<<"\033[32m//Dbg-"<<__FILE__<<"\""<< __LINE__<<" <Esc>pA "<<"\033[0m"<<<Esc>pA <<std::endl;<Esc>
nmap <leader>sp   :call Spellcheck()<CR>
nmap dc           yyp<m-up>kkw
nmap [{           ][=%''zz
vmap i            I
nmap <leader>]    [[=%''zz
map <m-up>        :call CommentStr()<cr>0i<C-r>=comment_str<Esc><Esc>j
map <m-down>      0xxj
map <m-h>         0xxx
map <m-l>         0i<tab><Esc>
imap <m-h>        <Esc>0xxx
imap <m-l>        <Esc>0i<tab><Esc>
nmap <leader>se   :!gnome-terminal --working-directory '%:p:h' -x tcsh -c "grf '<cword>'; /bin/tcsh -i"&<cr>
nmap <leader>sl   :!gnome-terminal --working-directory '%:p:h' -x tcsh -c "grf '<cword>'; /bin/tcsh -i"&<cr>
nmap <leader>go   :exe "!firefox -search '<cword>' &"<cr>
"nmap <leader>t    :let @d = expand('%:p:h')<cr>o<esc>"dp<esc>:set clipboard=unnamed<cr>dd<esc>:set clipboard=<cr>

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

if has("win32")
    set undodir=~\Documents\undo
    let MRU_File="C:\\Users\\Peter\\.vim_mru_files"
else
    let MRU_File="/home/zoe/.vim_mru_files"
"    let MRU_File=expand("~/.vim_mru_files")
    set undodir=~/.undo
endif
set undofile 

"nmap <silent><S-Down> <C-T>
"nmap <silent><S-Up> <C-]>
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

"nnoremap <C-Down> :call <SID>Saving_scroll("5<C-V><C-D>")<CR>
"vnoremap <C-Down> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-D>")<CR>
"nnoremap <C-Up> :call <SID>Saving_scroll("5<C-V><C-U>")<CR>
"vnoremap <C-Up> <Esc>:call <SID>Saving_scroll("gv1<C-V><C-U>")<CR>


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
   elseif exten =~ "java"
      let g:comment_str = "//"
   elseif exten =~ "vim"
      let g:comment_str = "\""
   elseif exten =~ "cs"
      let g:comment_str = "//"
   elseif exten =~ "js"
      let g:comment_str = "//"
   elseif exten =~ "bat"
      let g:comment_str = "REM "
   elseif exten =~ "ahk"
      let g:comment_str = "; "
   endif
endf

fu! DebugExtension3()
   if expand('%:p') =~ ".py"
      norm bywoprint(type(
      :norm pA))
   endif 
endf

fu! DebugExtension2()
   if expand('%:p') =~ ".py"
      norm bywoprint(
      :norm pA)
   endif 
endf


fu! DebugExtension()
   if expand('%:p') =~ ".ahk"
      norm bywoMsgBox, %
      :norm pA%
   elseif expand('%:p') =~ ".py"
      norm bywoprint("
      :norm pA: {}".format( 
      :norm pA))
   elseif expand('%:p') =~ ".java"
      norm bywoLog.d("
      :norm pA= ",
      :norm pA);
   else
      norm bywo$writeln($strcat("Dbg f: ", "<C-R>% : <Esc>pA ", <Esc>pA));<Esc>
   endif 
endf



fu! Toggler()
    let cchar = matchstr(getline('.'), '\%' . col('.') . 'c.')
    while (col('.') > 1)
        norm h
        let cchar = matchstr(getline('.'), '\%' . col('.') . 'c.')
        if (l:cchar == ' ') || (l:cchar == "\"") || (l:cchar == "\'") || (l:cchar == "%") 
            break
        endif
    endwhile

    if l:cchar == " "
        norm li"
        norm f 
        let cchar = matchstr(getline('.'), '\%' . col('.') . 'c.')
        if l:cchar == "\""
            norm A"
        endif
    elseif l:cchar =~ "\""
        norm xi'
        norm f"a'
        norm hxh
    elseif l:cchar =~ "\'"
        norm xi%
        norm f'a%
        norm hxh
    elseif l:cchar =~ "%"
        norm xi"
        norm f%a"
        norm hxh
    endif
endf

fu! MoreScope()
    cs add $CSCOPE_DB
endf

fu! ExecExtension()
   let path = expand('%:p')

    if l:path =~ ".ahk"
      :silent !"C:\Program Files\AutoHotkey\AutoHotkey.exe" %:p
    elseif l:path =~ ".py"
      :silent !python -i %:p
    elseif l:path =~ ".reg"
      :silent !%:p
    elseif l:path =~ ".bat"
   	    :silent !wscript "C:\Users\Peter\Documents\send.vbs"
    else
   	    :silent !wscript "C:\Users\Peter\Documents\send.vbs"
   endif 
endf


nmap j gj
nmap k gk

"call arpeggio#map('i', '', 0, 'fd', '<Esc>a(<Esc>ea)<Esc>')
"call arpeggio#map('c', '', 0, 'fd', '<Esc>a(<Esc>ea)<Esc>')
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

set noerrorbells visualbell t_vb=
autocmd GUIEnter * set visualbell t_vb=

if has("windows")
    set shell=C:\Windows\System32\bash.exe
    set shellpipe=|
    set shellredir=>
    set shellcmdflag=
endif

if executable('ag')
  let g:ackprg = 'ag --vimgrep'
endif

