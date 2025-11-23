# Visual Fixation Target

A Python package to generate customizable fixation targets for eye trcking experiments.

## Description

This package generates fixation target configurations as described by [Thaler et al. (2013)](https://www.sciencedirect.com/science/article/pii/S0042698912003380#f0005). It supports different target types:
- **A**: Center dot only
- **B**: Outer circle only
- **C**: Cross only
- **AB**, **AC**, **BC**: Combinations of two components
- **ABC**: All components (center dot + outer circle + cross)

All dimensions are specified in visual angles (degrees) and automatically converted to pixels based on your screen parameters.

### Target Type Examples

<table>
<tr>
<td align="center"><b>A</b><br/>(Center dot)</td>
<td align="center"><b>B</b><br/>(Outer circle)</td>
<td align="center"><b>C</b><br/>(Cross)</td>
<td align="center"><b>AB</b><br/>(Center + Outer)</td>
</tr>
<tr>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_a.png" width="100"/></td>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_b.png" width="100"/></td>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_c.png" width="100"/></td>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_ab.png" width="100"/></td>
</tr>
<tr>
<td align="center"><b>AC</b><br/>(Center + Cross)</td>
<td align="center"><b>BC</b><br/>(Outer + Cross)</td>
<td align="center"><b>ABC</b><br/>(All components)</td>
<td></td>
</tr>
<tr>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_ac.png" width="100"/></td>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_bc.png" width="100"/></td>
<td align="center"><img src="https://raw.githubusercontent.com/mh-salari/fixation-target/main/examples/fixation_abc.png" width="100"/></td>
<td></td>
</tr>
</table>

## Installation

### From PyPI
```bash
pip install fixation-target
```

### From source
```bash
git clone https://github.com/mh-salari/fixation-target.git
cd fixation-target
pip install -e .
```

## Usage

### Command-line Interface

#### Using a JSON configuration file

Create a JSON config file with your parameters:

```json
{
  "screen_width_mm": 476.64,
  "screen_height_mm": 268.11,
  "screen_width_px": 1920,
  "screen_height_px": 1080,
  "viewing_distance_mm": 930,
  "target_type": "ABC",
  "center_diameter_in_degrees": 0.1,
  "outer_diameter_in_degrees": 0.6,
  "cross_width_in_degrees": 0.15,
  "center_color": [0, 0, 0, 255],
  "outer_color": [0, 0, 0, 255],
  "cross_color": [255, 255, 255, 255],
  "background_diameter_in_degrees": 1.0,
  "background_color": [128, 128, 128, 255]
}
```
Load and use it:

```bash
fixation-target --json config.json --output output/
```

#### Using command-line arguments
```bash
fixation-target \
  --output output/ \
  --target-type ABC \
  --screen-width-mm 476.64 \
  --screen-height-mm 268.11 \
  --screen-width-px 1920 \
  --screen-height-px 1080 \
  --viewing-distance-mm 930 \
  --center-diameter 0.1 \
  --outer-diameter 0.6 \
  --cross-width 0.15 \
```

### Python API

```python
from pathlib import Path
from fixation_target import fixation_target

# Generate an ABC target
fixation_target(
    screen_width_mm=476.64,
    screen_height_mm=268.11,
    screen_width_px=1920,
    screen_height_px=1080,
    viewing_distance_mm=930,
    save_path=Path("output"),
    target_type="ABC",
    center_diameter_in_degrees=0.1,
    outer_diameter_in_degrees=0.6,
    cross_width_in_degrees=0.15,
    center_color=(0, 0, 0, 255),      # black
    outer_color=(0, 0, 0, 255),       # black
    cross_color=(255, 255, 255, 255), # white
    background_diameter_in_degrees=1.0,
    background_color=(128, 128, 128, 255),  # gray
    show=True
)
```

## Target Types

- **A**: Center dot only - useful for minimal fixation point
- **B**: Outer circle only - provides a reference boundary
- **C**: Cross only - traditional fixation cross
- **AB**: Center dot + outer circle
- **AC**: Center dot + cross
- **BC**: Outer circle + cross
- **ABC**: All components (recommended for stable fixation)

## Parameters

### Required Screen Parameters
- `screen_width_mm`: Physical width of your screen in millimeters
- `screen_height_mm`: Physical height of your screen in millimeters
- `screen_width_px`: Screen resolution width in pixels
- `screen_height_px`: Screen resolution height in pixels
- `viewing_distance_mm`: Distance from viewer to screen in millimeters

### Target Parameters
- `target_type`: One of "A", "B", "C", "AB", "AC", "BC", "ABC" (default: "ABC")
- `center_diameter_in_degrees`: Diameter of center dot in visual degrees (default: 0.1)
- `outer_diameter_in_degrees`: Diameter of outer circle in visual degrees (default: 0.6)
- `cross_width_in_degrees`: Width of cross lines in visual degrees (default: 0.15)
- `center_color`: RGBA color tuple for center dot (default: black)
- `outer_color`: RGBA color tuple for outer circle (default: black)
- `cross_color`: RGBA color tuple for cross (default: white)
- `background_diameter_in_degrees`: Optional background circle diameter
- `background_color`: Optional background circle color (RGBA tuple)
- `show`: Whether to display the generated image (default: True)

## Reference

Thaler, L., Schütz, A.C., Goodale, M.A., & Gegenfurtner, K.R. (2013).
What is the best fixation target? The effect of target shape on stability of fixational eye movements.
*Vision Research*, 76, 31-42.
https://doi.org/10.1016/j.visres.2012.10.012

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project has received funding from the European Union's Horizon Europe research and innovation funding program under grant agreement No 101072410, Eyes4ICU project.

<p align="center">
<img src="https://github.com/mh-salari/fixation-target/raw/main/resources/Funded_by_EU_Eyes4ICU.png" alt="Funded by EU Eyes4ICU" width="500">
</p>

## Author

Mohammadhossein Salari
Email: mohammadhossein.salari@gmail.com
