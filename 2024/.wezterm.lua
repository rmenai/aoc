local wezterm = require("wezterm")
local mux = wezterm.mux
local workspace = mux.get_active_workspace()

local function sh(cmd)
    return { "nu", "-c", cmd .. "; exec nu" }
end

local function main(win, gui)
    win:spawn_tab({ args = sh("yazi src/bin") })
end

for _, win in ipairs(mux.all_windows()) do
    if win:get_workspace() == workspace then
        local gui = win:gui_window()
        main(win, gui)
        break
    end
end
