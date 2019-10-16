--[[
palette.nvim: Access neovim/plugin options by their description
This is the lua reimplementation of python
--]]
-- luacheck: globals unpack
-- Inspired by https://github.com/Vigemus/palette/blob/master/lua/palette/init.lua
-- [ Private variables and tables
local state = {}
local palette = {}
local bindings = require('palette.bindings')
local vars = require('palette.vars')
local fns = require('palette.fns')
palette.debug = {}
palette.bindings = bindings
palette.config = {}
palette.term = {}
palette.term.prompt = {}

local nvim = vim.api -- luacheck: ignore
