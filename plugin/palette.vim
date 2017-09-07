" nvim-palette - nvim for noobs
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


" command! -nargs=* -complete=customlist,<sid>complete Palette call <sid>parse_flags(<q-args>)
command! Palette call PaletteSelect({ 'menus': v:true, 'options': v:true})


if exists("*menu_get")
	" echom "has export_menu"
	PaletteAddSource("menu")

	command! PaletteMenu call PaletteSelect({ 'menus': 1})
endif

if exists("*nvim_get_keymap")
	" echom "has nvim_get_keymap"
	command! PaletteKeymaps call PaletteSelect({ 'menus': 1})
endif

"TODO detect fzf via fzf.vim for instance ?

function! PaletteFzf(entries)
	" echo "entries=".string(a:entries)
	let g:palette_fzf_opts = get(g:,'palette_fzf_opts', s:opts)
	let g:palette_fzf_opts.source = a:entries
	let l:ret = fzf#run(s:opts)
endfunction

