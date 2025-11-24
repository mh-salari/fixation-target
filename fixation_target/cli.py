"""Command-line interface for fixation target generator."""

import argparse
from pathlib import Path

from fixation_target import fixation_target, load_config


def main() -> None:
    """Run the fixation target generator from command line."""
    parser = argparse.ArgumentParser(
        description="Generate fixation targets for vision science experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from JSON config file
  fixation-target --json my_config.json --output output/

  # Generate specific target type with custom parameters
  fixation-target --output output/ --target-type AB --screen-width-mm 476.64 \\
    --screen-height-mm 268.11 --screen-width-px 1920 --screen-height-px 1080 \\
    --viewing-distance-mm 930

  # Generate with custom filename and no anti-aliasing
  fixation-target --json config.json --output output/ --filename my_target --no-antialias
        """,
    )

    # Config file input
    parser.add_argument(
        "--json",
        type=str,
        help="Path to JSON configuration file",
    )

    # Output path (required)
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory path for generated images",
    )

    # Display option
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Don't display the generated image",
    )

    # Output options
    parser.add_argument(
        "--filename",
        type=str,
        default="fixation",
        help="Base filename without extension (default: fixation). Target type suffix will be appended automatically",
    )
    parser.add_argument(
        "--no-antialias",
        action="store_true",
        help="Disable 2x supersampling anti-aliasing for PNG (enabled by default)",
    )

    # Screen parameters
    parser.add_argument("--screen-width-mm", type=float, help="Screen width in millimeters")
    parser.add_argument("--screen-height-mm", type=float, help="Screen height in millimeters")
    parser.add_argument("--screen-width-px", type=int, help="Screen width in pixels")
    parser.add_argument("--screen-height-px", type=int, help="Screen height in pixels")
    parser.add_argument("--viewing-distance-mm", type=float, help="Viewing distance in millimeters")

    # Target parameters
    parser.add_argument(
        "--target-type",
        type=str,
        choices=["A", "B", "C", "AB", "AC", "BC", "ABC"],
        help="Target type: A (center), B (outer), C (cross), or combinations",
    )
    parser.add_argument("--center-diameter", type=float, help="Center dot diameter in degrees")
    parser.add_argument("--outer-diameter", type=float, help="Outer circle diameter in degrees")
    parser.add_argument("--cross-width", type=float, help="Cross line width in degrees")
    parser.add_argument("--background-diameter", type=float, help="Background circle diameter in degrees")

    args = parser.parse_args()

    # Load config from JSON if provided
    if args.json:
        config = load_config(args.json)
        # Convert color lists to tuples (JSON doesn't have tuples)
        if "center_color" in config:
            config["center_color"] = tuple(config["center_color"])
        if "outer_color" in config:
            config["outer_color"] = tuple(config["outer_color"])
        if "cross_color" in config:
            config["cross_color"] = tuple(config["cross_color"])
        if "background_color" in config:
            config["background_color"] = tuple(config["background_color"])
    else:
        # Build config from command-line arguments
        required_params = [
            "screen_width_mm",
            "screen_height_mm",
            "screen_width_px",
            "screen_height_px",
            "viewing_distance_mm",
        ]
        missing = [p for p in required_params if getattr(args, p) is None]
        if missing:
            parser.error(
                f"The following arguments are required when not using --json: "
                f"{', '.join('--' + p.replace('_', '-') for p in missing)}"
            )

        config = {
            "screen_width_mm": args.screen_width_mm,
            "screen_height_mm": args.screen_height_mm,
            "screen_width_px": args.screen_width_px,
            "screen_height_px": args.screen_height_px,
            "viewing_distance_mm": args.viewing_distance_mm,
        }

        # Add optional parameters if provided
        if args.target_type:
            config["target_type"] = args.target_type
        if args.center_diameter:
            config["center_diameter_in_degrees"] = args.center_diameter
        if args.outer_diameter:
            config["outer_diameter_in_degrees"] = args.outer_diameter
        if args.cross_width:
            config["cross_width_in_degrees"] = args.cross_width
        if args.background_diameter:
            config["background_diameter_in_degrees"] = args.background_diameter

    # Set output path and show option
    config["save_path"] = Path(args.output)
    config["show"] = not args.no_show

    # Set filename and antialias options
    config["filename"] = args.filename
    config["antialias"] = not args.no_antialias

    # Generate the target
    fixation_target(**config)


if __name__ == "__main__":
    main()
