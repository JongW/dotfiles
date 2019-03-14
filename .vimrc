" Specify a directory for plugins
call plug#begin('/home/jongwoongto/.vim/plugged')

" Plug install list
Plug 'scrooloose/nerdtree'
Plug 'tpope/vim-fugitive'
Plug 'vim-syntastic/syntastic'
Plug 'majutsushi/tagbar'
Plug 'leafgarland/typescript-vim'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'vimwiki/vimwiki'
Plug 'j-tom/vim-old-hope'

" Initialize plugin system
call plug#end()

" My random attempts to fix powerline symbols showing up
" (not sure which one did it)
set guifont=DejaVu_Sans_Mono_for_Powerline_Book:h12
let g:airline_powerline_fonts=1
let g:Powerline_symbols='unicode'
set t_Co=256

"Enable mouse usage(all modes)
set mouse=a     

" Set compatibility to Vim only.
set nocompatible

" Turn on syntax highlighting.
syntax on

" Turn off modelines
set modelines=0

" Automatically wrap text that extends beyond the screen length.
set wrap
" Vim's auto indentation feature does not work properly with text copied from outisde of Vim. Press the <F2> key to toggle paste mode on/off.
nnoremap <F2> :set invpaste paste?<CR>
imap <F2> <C-O>:set invpaste paste?<CR>
set pastetoggle=<F2>

set formatoptions=tcqrn1
set tabstop=2
set shiftwidth=2
set softtabstop=2
set expandtab
set noshiftround

" Display 5 lines above/below the cursor when scrolling with a mouse.
set scrolloff=5
" Fixes common backspace problems
set backspace=indent,eol,start

" Speed up scrolling in Vim
set ttyfast
    
" Status bar
set laststatus=2

" Display options
set showmode
set showcmd

" Highlight matching pairs of brackets. Use the '%' character to jump between them.
set matchpairs+=<:>

" Show line numbers
set number

" Encoding
set encoding=utf-8

" Highlight matching search patterns
set hlsearch
" Enable incremental search
set incsearch
" Include matching uppercase words with lowercase search term
set ignorecase
" Include only uppercase words with uppercase search term
set smartcase

" Store info from no more than 100 files at a time, 9999 lines of text, 100kb of data. Useful for copying large amounts of data between files.
set viminfo='100,<9999,s100

" Fix for vim background color erase on KITTY
if &term =~ 'xterm-kitty'
  " disable Background Color Erase (BCE) so that color schemes
  " render properly when inside 256-color tmux and GNU screen.
  " see also http://snk.tuxfamily.org/log/vim-256color-bce.html
  set t_ut=
endif

" Vim Themes
"   Airline Theme
let g:airline_theme='minimalist'
"   Vim text colors
set background=dark
color old-hope

