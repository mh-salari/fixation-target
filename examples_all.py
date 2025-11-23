"""Generate example images for all target types."""

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
    center_diameter_in_degrees = 0.1
    outer_diameter_in_degrees = 0.6
    cross_width_in_degrees = 0.15

    # Output path for examples
    save_path = Path(__file__).parent / "examples"

    # Define colors
    black = (0, 0, 0, 255)
    white = (255, 255, 255, 255)

    # Color configurations for each target type (optimized for visibility)
    configs = {
        "A": {  # Center dot only - can be any color
            "center_color": black,
        },
        "B": {  # Outer circle only - can be any color
            "outer_color": black,
        },
        "C": {  # Cross only - can be any color
            "cross_color": black,
        },
        "AB": {  # Center + outer - must have different colors
            "center_color": white,
            "outer_color": black,
        },
        "AC": {  # Center + cross - must have different colors
            "center_color": white,
            "cross_color": black,
        },
        "BC": {  # Outer + cross - must have different colors
            "outer_color": black,
            "cross_color": white,
        },
        "ABC": {  # All components - cross must differ from both outer and center
            "center_color": black,  # A and B can be same
            "outer_color": black,  # A and B can be same
            "cross_color": white,  # C must differ from both A and B
        },
    }

    # Generate all target types
    for target_type, colors in configs.items():
        print(f"\nGenerating {target_type} target...")
        fixation_target(
            screen_width_mm,
            screen_height_mm,
            screen_width_px,
            screen_height_px,
            viewing_distance_mm,
            save_path,
            target_type=target_type,
            center_diameter_in_degrees=center_diameter_in_degrees,
            outer_diameter_in_degrees=outer_diameter_in_degrees,
            cross_width_in_degrees=cross_width_in_degrees,
            background_diameter_in_degrees=1.0,
            background_color=white,
            **colors,
            show=False,
        )

    print(f"\nAll examples saved in: {save_path}")
