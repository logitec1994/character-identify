# Target window

TARGET_TITLE = "logitec@"


# ROI configuration
# Values are ratios relative to the captured frame.

ROI_X_RATIO = 0.0
ROI_Y_RATIO = 0.0
ROI_WIDTH_RATIO = 1.0
ROI_HEIGHT_RATIO = 0.5


# Detector input

ROI_SCALE = 1.0


# Diagnostics

SHOW_DIAGNOSTICS = True
SAVE_DIAGNOSTIC_IMAGES = False

DIAGNOSTICS_DIR = "diagnostics"

# Window geometry D-Bus interface

BUS_NAME = "org.gnome.Shell.Extensions.WindowGeometry"
OBJECT_PATH = "/org/gnome/Shell/Extensions/WindowGeometry"
INTERFACE = "org.gnome.Shell.Extensions.WindowGeometry"
