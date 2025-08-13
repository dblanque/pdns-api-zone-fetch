-- Lua

-- Track SMN rule
AuthDomainsRuleName = "auth-domains-pool-rule-main"
AuthDomainsRuleAction = nil

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
	local AuthDomains = getSmnListFromFile("/etc/dnsdist/smn_domains.txt");
	AuthDomainsRule = SuffixMatchNodeRule(AuthDomains);
	AuthDomainsRuleAction = addAction(
		AuthDomainsRule,
		PoolAction('auth'),
		{name=AuthDomainsRuleName}
	);
	mvRuleToTop()
end

function reloadSMNRules()
	-- Remove Previous Rule
	local ok, result = pcall(function()
		return rmRule(AuthDomainsRuleName)
	end)

	setSMNRules()
end

-- Set SMN Rules at start
reloadSMNRules()