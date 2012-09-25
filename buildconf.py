# File whose presence means the submodule was already built
COOKIENAME = ".hawaii-ci-cookie"

# Modules
MODULES = [
	"kde-extra-cmake-modules",
	"kde-solid",
	"vibe",
	"widget-styles",
	"icon-themes",
	"wallpapers",
	"fluid",
	"fluid-themes",
	"loginmanager",
	"greenisland",
	"swordfish",
	"system-preferences",
	"archiver",
	"eyesight",
	"terminal",
	"widget-factory",
]

# Ignore modules
IGNORED_MODULES = [
	"widget-styles",
]

# Dependencies
DEPENDENCIES = {
	"kde-extra-cmake-modules": "",
	"kde-solid": "kde-extra-cmake-modules",
	"vibe": "kde-solid",
	"fluid": "vibe,fluid-themes",
	"fluid-themes": "",
	"widget-styles": "vibe",
	"icon-themes": "",
	"wallpapers": "",
	"loginmanager": "fluid",
	"greenisland": "vibe,fluid,wallpapers",
	"swordfish": "vibe",
	"system-preferences": "vibe",
	"archiver": "vibe",
	"eyesight": "vibe",
	"terminal": "vibe",
	"widget-factory": "widget-styles",
}
