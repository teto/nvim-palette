" nvim-palette - vim for noobs
" Author:       Matthieu Coudron
" License:      MIT


function! s:processResult(res)
	let cmd = PalettePostprocessChoice(a:res)
	echom "Received cmd=".cmd
	execute cmd
	if get(g:,'palette_histadd', 0)
		call histadd(":", cmd)
	endif
endfunc


let s:opts = {
	\ 'source': ["choice 1", "choice 2"],
	\ 'sink': function('s:processResult'),
	\ 'options': ' --prompt "Palette>"',
	\ 'down': '50%',
	\ }



command! Palette call PaletteGetBools()
" does not work
if has("export_menu")
	" echom "has export_menu"
	command! PaletteMenu call PaletteGetMenu()
endif



function! PaletteFzf(entries)
	" echo "entries=".string(a:entries)
	let g:palette_fzf_opts = get(g:,'palette_fzf_opts', s:opts)
	let g:palette_fzf_opts.source = a:entries
	let l:ret = fzf#run(s:opts)
endfunction



nnoremap <silent> <Plug>(PaletteRun)	:<c-u>call PaletteGetBools()<cr>
