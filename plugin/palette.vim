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


let s:fzf_opts = {
	\ 'source': ["choice 1", "choice 2"],
	\ 'sink': function('s:processResult'),
	\ 'options': ' --prompt "Palette>"',
	\ 'down': '50%',
	\ }


" command! -nargs=* -complete=customlist,<sid>complete Palette call <sid>parse_flags(<q-args>)
command! Palette call PaletteSelect({ 'menus': v:true, 'options': v:true})

if exists("*menu_get")
	" echom "has export_menu"
	" PaletteAddSource("menu")

	command! PaletteMenu call PaletteSelect({ 'menus': 1})
endif

" if exists("*nvim_get_keymap")
" 	" echom "has nvim_get_keymap"
" 	command! PaletteKeymaps call PaletteSelect({ 'keymaps': 1})
" endif


function! PaletteSelect(filters)
   " TODO detect fuzzy finders (denite/fzf etc)
   " for now just supports fzf

   " retrieve entries from rplugin
	let l:entries = PaletteGetEntries(a:filters)
	" echo "entries0=".string(l:entries[0])
	call PaletteFzf(l:entries[0])

endfunc


" TODO make use of g:fzf_command_prefix
function! PaletteFzf(entries)
	" look at https://github.com/junegunn/fzf/wiki/Examples-(vim)
	" for the semantics
	" echo "entries=".string(a:entries)
	" todo we should merge them
	let g:palette_fzf_opts = get(g:,'palette_fzf_opts', s:fzf_opts)
	let g:palette_fzf_opts.source = a:entries
	let l:ret = fzf#run(g:palette_fzf_opts)
endfunction

