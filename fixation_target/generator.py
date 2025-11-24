"""Generate fixation targets for vision science experiments.

This module generates fixation target configurations as described by Thaler et al. (2013).
Supports different configurations: A (center dot), B (outer circle), C (cross), and
combinations: AB, AC, BC, ABC.

Reference:
    Thaler, L., Schütz, A.C., Goodale, M.A., & Gegenfurtner, K.R. (2013).
    What is the best fixation target? The effect of target shape on stability
    of fixational eye movements. Vision Research, 76, 31-42.
    https://doi.org/10.1016/j.visres.2012.10.012

Author:       Mohammadhossein Salari
Email:        mohammadhossein.salari@gmail.com
"""

from pathlib import Path

import svgwrite
from PIL import Image, ImageChops, ImageDraw

from fixation_target.converter import VisualAngleConverter


def _rgba_to_svg_attrs(color: tuple[int, int, int, int]) -> dict:
    """Convert RGBA color tuple to SVG attributes."""
    r, g, b, a = color
    return {"fill": f"rgb({r},{g},{b})", "fill-opacity": a / 255.0}


def _render_png(
    png_path: Path,
    img_size: tuple[int, int],
    cx: int,
    cy: int,
    draw_center: bool,
    draw_outer: bool,
    draw_cross: bool,
    center_diameter_px: int,
    outer_diameter_px: int,
    cross_width_px: int,
    center_color: tuple[int, int, int, int],
    outer_color: tuple[int, int, int, int],
    cross_color: tuple[int, int, int, int],
    background_diameter_px: int | None,
    background_color: tuple[int, int, int, int] | None,
    antialias: bool,
) -> Image.Image:
    """Render fixation target as PNG using PIL with optional supersampling."""
    # Apply 2x supersampling if antialiasing is enabled
    scale = 2 if antialias else 1
    scaled_size = (img_size[0] * scale, img_size[1] * scale)
    scaled_cx, scaled_cy = cx * scale, cy * scale

    img = Image.new("RGBA", scaled_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    if background_diameter_px is not None and background_color is not None:
        background_radius = (background_diameter_px * scale) // 2
        draw.ellipse(
            [
                scaled_cx - background_radius,
                scaled_cy - background_radius,
                scaled_cx + background_radius,
                scaled_cy + background_radius,
            ],
            fill=background_color,
        )

    # Outer circle (B component)
    if draw_outer:
        outer_radius = (outer_diameter_px * scale) // 2
        draw.ellipse(
            [scaled_cx - outer_radius, scaled_cy - outer_radius, scaled_cx + outer_radius, scaled_cy + outer_radius],
            fill=outer_color,
        )

    # Cross (C component)
    if draw_cross:
        outer_radius = (outer_diameter_px * scale) // 2

        # Create circular mask for outer circle boundary
        circle_mask = Image.new("L", scaled_size, 0)
        circle_draw = ImageDraw.Draw(circle_mask)
        circle_draw.ellipse(
            [scaled_cx - outer_radius, scaled_cy - outer_radius, scaled_cx + outer_radius, scaled_cy + outer_radius],
            fill=255,
        )

        # Create cross mask
        cross_mask = Image.new("L", scaled_size, 0)
        cross_draw = ImageDraw.Draw(cross_mask)
        cross_length = outer_radius
        cross_draw.line(
            [scaled_cx - cross_length, scaled_cy, scaled_cx + cross_length, scaled_cy],
            fill=255,
            width=cross_width_px * scale,
        )
        cross_draw.line(
            [scaled_cx, scaled_cy - cross_length, scaled_cx, scaled_cy + cross_length],
            fill=255,
            width=cross_width_px * scale,
        )

        # Clip cross to circle boundary
        cross_mask = ImageChops.multiply(cross_mask, circle_mask)

        # Composite cross onto image
        cross_layer = Image.new("RGBA", scaled_size, cross_color)
        img = Image.composite(cross_layer, img, cross_mask)

    # Center dot (A component)
    if draw_center:
        center_radius = (center_diameter_px * scale) // 2
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            [scaled_cx - center_radius, scaled_cy - center_radius, scaled_cx + center_radius, scaled_cy + center_radius],
            fill=center_color,
        )

    # Downsample to final size if antialiasing was applied
    if antialias:
        img = img.resize(img_size, Image.Resampling.LANCZOS)

    img.save(png_path)
    return img


def _render_svg(
    svg_path: Path,
    img_size: tuple[int, int],
    cx: int,
    cy: int,
    draw_center: bool,
    draw_outer: bool,
    draw_cross: bool,
    center_diameter_px: int,
    outer_diameter_px: int,
    cross_width_px: int,
    center_color: tuple[int, int, int, int],
    outer_color: tuple[int, int, int, int],
    cross_color: tuple[int, int, int, int],
    background_diameter_px: int | None,
    background_color: tuple[int, int, int, int] | None,
) -> None:
    """Render fixation target as SVG."""
    dwg = svgwrite.Drawing(str(svg_path), size=img_size, profile="full")

    # Background circle
    if background_diameter_px is not None and background_color is not None:
        background_radius = background_diameter_px / 2
        dwg.add(dwg.circle(center=(cx, cy), r=background_radius, **_rgba_to_svg_attrs(background_color)))

    # Outer circle (B component)
    if draw_outer:
        outer_radius = outer_diameter_px / 2
        dwg.add(dwg.circle(center=(cx, cy), r=outer_radius, **_rgba_to_svg_attrs(outer_color)))

    # Cross (C component)
    if draw_cross:
        outer_radius = outer_diameter_px / 2
        cross_length = outer_radius

        # Clip path for circular boundary
        clip_id = "circle-clip"
        clip = dwg.defs.add(dwg.clipPath(id=clip_id))
        clip.add(dwg.circle(center=(cx, cy), r=outer_radius))

        # Cross lines with clipping
        cross_group = dwg.g(clip_path=f"url(#{clip_id})")
        r, g, b, a = cross_color
        stroke_attrs = {
            "stroke": f"rgb({r},{g},{b})",
            "stroke-opacity": a / 255.0,
            "stroke-width": cross_width_px,
            "stroke-linecap": "butt",
        }
        cross_group.add(
            dwg.line(start=(cx - cross_length, cy), end=(cx + cross_length, cy), fill="none", **stroke_attrs)
        )
        cross_group.add(
            dwg.line(start=(cx, cy - cross_length), end=(cx, cy + cross_length), fill="none", **stroke_attrs)
        )
        dwg.add(cross_group)

    # Center dot (A component)
    if draw_center:
        center_radius = center_diameter_px / 2
        dwg.add(dwg.circle(center=(cx, cy), r=center_radius, **_rgba_to_svg_attrs(center_color)))

    dwg.save()


def fixation_target(
    screen_width_mm: float,
    screen_height_mm: float,
    screen_width_px: int,
    screen_height_px: int,
    viewing_distance_mm: float,
    save_path: Path | str,
    target_type: str = "ABC",
    center_diameter_in_degrees: float = 0.1,
    outer_diameter_in_degrees: float = 0.6,
    cross_width_in_degrees: float = 0.15,
    center_color: tuple[int, int, int, int] = (0, 0, 0, 255),
    outer_color: tuple[int, int, int, int] = (0, 0, 0, 255),
    cross_color: tuple[int, int, int, int] = (255, 255, 255, 255),
    background_diameter_in_degrees: float | None = None,
    background_color: tuple[int, int, int, int] | None = None,
    antialias: bool = True,
    show: bool = True,
) -> None:
    """Generate a fixation target for vision science experiments.

    Supports configurations: A (center), B (outer circle), C (cross), AB, AC, BC, ABC.

    Args:
        screen_width_mm: Width of the screen in millimeters.
        screen_height_mm: Height of the screen in millimeters.
        screen_width_px: Width of the screen in pixels.
        screen_height_px: Height of the screen in pixels.
        viewing_distance_mm: Distance between the viewer and the screen in millimeters.
        save_path: Path where the generated image will be saved.
        target_type: Type of target ("A", "B", "C", "AB", "AC", "BC", "ABC"). Default: "ABC".
        center_diameter_in_degrees: Diameter of the center dot in degrees. Default: 0.1.
        outer_diameter_in_degrees: Diameter of the outer circle in degrees. Default: 0.6.
        cross_width_in_degrees: Width of the cross lines in degrees. Default: 0.15.
        center_color: Color of the center dot in (R, G, B, A) format. Default: black.
        outer_color: Color of the outer circle in (R, G, B, A) format. Default: black.
        cross_color: Color of the cross in (R, G, B, A) format. Default: white.
        background_diameter_in_degrees: Diameter of background circle in degrees (optional).
        background_color: Color of background circle in (R, G, B, A) format (optional).
        antialias: Apply 2x supersampling for smoother edges in PNG. Default: True.
        show: Whether to display the image after generation. Default: True.

    """
    # Validate and normalize target type
    target_type = target_type.upper()
    valid_types = {"A", "B", "C", "AB", "AC", "BC", "ABC"}
    if target_type not in valid_types:
        msg = f"Invalid target_type: {target_type}. Must be one of: {', '.join(sorted(valid_types))}"
        raise ValueError(msg)

    # Determine which components to draw
    draw_center = "A" in target_type
    draw_outer = "B" in target_type
    draw_cross = "C" in target_type

    # Validate color combinations for visibility in combined targets
    if draw_center and draw_outer and not draw_cross and center_color == outer_color:  # AB only
        msg = (
            f"For AB target, center and outer must have different colors. "
            f"Both are currently {center_color}. The center will not be visible."
        )
        raise ValueError(msg)

    if draw_center and draw_cross and not draw_outer and center_color == cross_color:  # AC only
        msg = (
            f"For AC target, center and cross must have different colors. "
            f"Both are currently {center_color}. Components will not be distinguishable."
        )
        raise ValueError(msg)

    if draw_outer and draw_cross and not draw_center and outer_color == cross_color:  # BC only
        msg = (
            f"For BC target, outer circle and cross must have different colors. "
            f"Both are currently {outer_color}. The cross will not be visible."
        )
        raise ValueError(msg)

    if draw_center and draw_outer and draw_cross:  # ABC
        if cross_color == outer_color:
            msg = (
                f"For ABC target, cross and outer circle must have different colors. "
                f"Both are currently {cross_color}. The cross will not be visible."
            )
            raise ValueError(msg)
        if cross_color == center_color:
            msg = (
                f"For ABC target, cross and center must have different colors. "
                f"Both are currently {cross_color}. Components will not be distinguishable."
            )
            raise ValueError(msg)

    # Initialize the visual angle converter
    converter = VisualAngleConverter(
        screen_width_pixels=screen_width_px,
        screen_height_pixels=screen_height_px,
        screen_width_mm=screen_width_mm,
        screen_height_mm=screen_height_mm,
        distance=viewing_distance_mm,
    )

    # Calculate sizes
    center_diameter_px = int(converter.visual_angle_to_pixels(center_diameter_in_degrees, orientation="vertical"))
    outer_diameter_px = int(converter.visual_angle_to_pixels(outer_diameter_in_degrees, orientation="vertical"))
    cross_width_px = int(converter.visual_angle_to_pixels(cross_width_in_degrees, orientation="vertical"))

    # Print configuration
    print(f"Target type: {target_type}")
    if draw_center:
        print(f"Center dot: {center_diameter_px} px ({center_diameter_in_degrees:.2f}°)")
    if draw_outer:
        print(f"Outer circle: {outer_diameter_px} px ({outer_diameter_in_degrees:.2f}°)")
    if draw_cross:
        print(f"Cross width: {cross_width_px} px ({cross_width_in_degrees:.2f}°)")

    # Calculate background circle size if provided
    if background_diameter_in_degrees is not None:
        background_diameter_px = int(
            converter.visual_angle_to_pixels(background_diameter_in_degrees, orientation="vertical")
        )
        print(f"Background: {background_diameter_px} px ({background_diameter_in_degrees:.2f}°)")
        largest_diameter = background_diameter_px
    else:
        background_diameter_px = None
        # Determine largest diameter from active components
        diameters = []
        if draw_center:
            diameters.append(center_diameter_px)
        if draw_outer:
            diameters.append(outer_diameter_px)
        if draw_cross:
            diameters.append(outer_diameter_px)  # Cross extends to outer radius
        largest_diameter = max(diameters) if diameters else outer_diameter_px

    # Create image size and center coordinates
    img_size = (largest_diameter + 2, largest_diameter + 2)
    cx, cy = img_size[0] // 2, img_size[1] // 2
    print(f"Image size: {img_size[0]}x{img_size[1]} px")

    # Save paths
    save_path = Path(save_path)
    save_path.mkdir(exist_ok=True)
    png_path = save_path / f"fixation_{target_type.lower()}.png"
    svg_path = save_path / f"fixation_{target_type.lower()}.svg"

    # Render PNG
    img = _render_png(
        png_path,
        img_size,
        cx,
        cy,
        draw_center,
        draw_outer,
        draw_cross,
        center_diameter_px,
        outer_diameter_px,
        cross_width_px,
        center_color,
        outer_color,
        cross_color,
        background_diameter_px,
        background_color,
        antialias,
    )
    print(f"Saved PNG: {png_path}")

    # Render SVG
    _render_svg(
        svg_path,
        img_size,
        cx,
        cy,
        draw_center,
        draw_outer,
        draw_cross,
        center_diameter_px,
        outer_diameter_px,
        cross_width_px,
        center_color,
        outer_color,
        cross_color,
        background_diameter_px,
        background_color,
    )
    print(f"Saved SVG: {svg_path}")

    # Display if requested
    if show:
        img.show()
