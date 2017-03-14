" nvim-palette - vim for noobs
" Author:       Matthieu Coudron
" License:      MIT


function! s:processResult(res)
	" echom 'result='.a:res. ' of type '.type(a:res)
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



function! PaletteFzf(entries)
	" echo "entries=".string(a:entries)
	let g:palette_fzf_opts = get(g:,'palette_fzf_opts', s:opts)
	let g:palette_fzf_opts.source = a:entries
	" let s:opts.source = a:entries
	" let s:opts.source = ["test 1", "test2"]
	" result processed in sink
	let l:ret = fzf#run(s:opts)
endfunction



nnoremap <silent> <Plug>(PaletteRun)	:<c-u>call PaletteGetBools()<cr>
