-- Lua
local function empty_str(s)
	return s == nil or s == ''
end

local function is_comment(v)
	if not v then return false end
	local p_list = {
		"^%s*#",      -- Matches "#" with optional leading spaces
		"^%s*%-%-",   -- Matches "--" with optional leading spaces
		"^%s*//",     -- Matches "//" with optional leading spaces
		"^%s*!"       -- Matches "!" with optional leading spaces
	}
	for _, pattern in ipairs(p_list) do
		if v:match(pattern) then return true end
	end
	return false
end

-- returns true if the given file exists
local function fileExists(file)
	local f = io.open(file, "rb")
	if f then
		f:close()
	end
	return f ~= nil
end

local function getAbsolutePathViaCommand()
	local info = debug.getinfo(1, 'S')
	local scriptPath = info.source:sub(2)
	
	local handle, err
	local absPath
	
	if package.config:sub(1,1) == "\\" then
		-- Windows
		handle = io.popen('cd')
		if handle then
			local currentDir = handle:read('*l')
			handle:close()
			absPath = currentDir .. "\\" .. scriptPath
		end
	else
		-- Unix-like systems
		handle = io.popen('pwd')
		if handle then
			local currentDir = handle:read('*l')
			handle:close()
			absPath = currentDir .. "/" .. scriptPath
		end
	end
	
	return absPath
end

local function splitPath(path)
	if not path or path == "" then
		return "", ""
	end
	
	-- Handle the case where path is just a filename (no directory)
	if not path:find("[/\\]") then
		return "", path
	end
	
	-- Find the last occurrence of either / or \ separator
	local last_slash_pos = 0
	for i = #path, 1, -1 do
		local char = path:sub(i, i)
		if char == "/" or char == "\\" then
			last_slash_pos = i
			break
		end
	end
	
	if last_slash_pos == 0 then
		-- No separator found (shouldn't happen given the check above, but just in case)
		return "", path
	else
		local dirname = path:sub(1, last_slash_pos)
		local filename = path:sub(last_slash_pos + 1)
		return dirname, filename
	end
end

-- Track SMN rule indices
AuthDomainsRule = nil
local scriptPath = getAbsolutePathViaCommand()
local scriptDir, scriptName = splitPath(scriptPath)

-- loads contents of a file line by line into the whitelist table
local function getSmnListFromFile(filename)
	local AuthDomains = newSuffixMatchNode();

	-- Validate input parameters
	if type(filename) ~= "string" then
		mainlog("getSmnListFromFile(): invalid parameters", pdns.loglevels.Error)
		return false
	end
	
	if not fileExists(filename) then
		mainlog(
			fn_name .. "(): could not open file " .. filename,
			pdns.loglevels.Warning
		)
		return
	end

	for line in io.lines(filename) do
		-- Trim whitespace from line
		line = line:match("^%s*(.-)%s*$")
		AuthDomains:add(newDNSName(line));
	end
	return AuthDomains
end

local function setSMNRules()
	AuthDomains = getSmnListFromFile(scriptDir .. "01_smn_domains.lua");
	AuthDomainsRule = SuffixMatchNodeRule(AuthDomains);
	addAction(AuthDomainsRule, PoolAction('auth'));
end

function reloadSMNRules()
	-- Remove Previous Rule
	if AuthDomainsRule then
		rmRule(AuthDomainsRule)
	end

	setSMNRules()
end
