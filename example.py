"""Example script to generate fixation targets.

Author:       Mohammadhossein Salari
Email:        mohammadhossein.salari@gmail.com
"""

from pathlib import Path

from fixation_target import fixation_target

if __name__ == "__main__":
    # Screen parameters
    screen_width_mm = 476.64
    screen_height_mm = 268.11
    screen_width_px = 1920
    screen_height_px = 1080
    viewing_distance_mm = 930

    # Target parameters (in degrees)
    center_diameter_in_degrees = 0.1  # A component: center dot
    outer_diameter_in_degrees = 0.6  # B component: outer circle
    cross_width_in_degrees = 0.15  # C component: cross lines

    # Optional background circle
    background_diameter_in_degrees = 1.0
    background_color = (128, 128, 128, 255)  # gray

    # Colors (R, G, B, A)
    center_color = (0, 0, 0, 255)  # black center dot
    outer_color = (0, 0, 0, 255)  # black outer circle
    cross_color = (255, 255, 255, 255)  # white cross

    # Output path
    save_path = Path(__file__).parent / "output"

    # Generate ABC target (all components)
    fixation_target(
        screen_width_mm,
        screen_height_mm,
        screen_width_px,
        screen_height_px,
        viewing_distance_mm,
        save_path,
        target_type="ABC",
        center_diameter_in_degrees=center_diameter_in_degrees,
        outer_diameter_in_degrees=outer_diameter_in_degrees,
        cross_width_in_degrees=cross_width_in_degrees,
        center_color=center_color,
        outer_color=outer_color,
        cross_color=cross_color,
        background_diameter_in_degrees=background_diameter_in_degrees,
        background_color=background_color,
        filename="fixation",
        antialias=True,
    )
