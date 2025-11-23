"""Visual Fixation Target - Generate customizable fixation targets for vision science experiments."""

from importlib.metadata import version

from fixation_target.config import load_config, save_config
from fixation_target.converter import VisualAngleConverter
from fixation_target.generator import fixation_target

__version__ = version("fixation-target")
__all__ = ["VisualAngleConverter", "fixation_target", "load_config", "save_config"]
