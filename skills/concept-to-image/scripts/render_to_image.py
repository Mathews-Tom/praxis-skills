#!/usr/bin/env python3
"""
render_to_image.py — Convert self-contained HTML to PNG or SVG.

Uses Playwright (headless Chromium) for pixel-perfect rendering.

Usage:
    python3 render_to_image.py input.html output.png [--scale 2] [--selector ".canvas"]
    python3 render_to_image.py input.html output.svg [--selector ".canvas"]

PNG: Screenshots the target element at the given device scale factor.
SVG: Extracts inline SVG content if present; otherwise falls back to PNG with a warning.
"""

import argparse
import sys
from pathlib import Path


def _launch_browser(playwright):
    """Launch Chromium with container-safe flags."""
    return playwright.chromium.launch(
        args=[
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-software-rasterizer',
            '--single-process',
        ]
    )


def extract_svg_content(page, selector: str) -> str | None:
    """
    Attempt to extract a root <svg> element from inside the target container.
    Returns the SVG markup string if found, None otherwise.
    """
    return page.evaluate(f"""
        (() => {{
            const container = document.querySelector('{selector}');
            if (!container) return null;

            // Check if the container itself is an SVG
            if (container.tagName.toLowerCase() === 'svg') {{
                return container.outerHTML;
            }}

            // Check for a single direct SVG child (ignoring whitespace text nodes)
            const children = Array.from(container.children);
            const svgChildren = children.filter(c => c.tagName.toLowerCase() === 'svg');

            if (svgChildren.length === 1 && children.length === 1) {{
                return svgChildren[0].outerHTML;
            }}

            // Multiple children or no SVG — can't cleanly extract
            return null;
        }})()
    """)


def render_png(page, output_path: str, selector: str):
    """Screenshot the target element as PNG."""
    element = page.query_selector(selector)
    if not element:
        print(f"WARNING: Selector '{selector}' not found. Capturing full page.", file=sys.stderr)
        page.screenshot(path=output_path, full_page=True)
    else:
        element.screenshot(path=output_path)

    size = Path(output_path).stat().st_size
    print(f"PNG saved: {output_path}")
    print(f"  Size: {size:,} bytes ({size / 1024:.1f} KB)")
    return output_path


def render_svg(page, output_path: str, selector: str):
    """Extract SVG content or warn and fall back to PNG."""
    svg_content = extract_svg_content(page, selector)

    if svg_content:
        # Add XML declaration if missing
        if not svg_content.startswith('<?xml'):
            svg_content = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_content

        # Ensure xmlns is present
        if 'xmlns=' not in svg_content:
            svg_content = svg_content.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)

        Path(output_path).write_text(svg_content, encoding='utf-8')
        size = Path(output_path).stat().st_size
        print(f"SVG saved: {output_path}")
        print(f"  Size: {size:,} bytes ({size / 1024:.1f} KB)")
        return output_path
    else:
        # Fall back to PNG
        fallback_path = output_path.replace('.svg', '.png')
        print(
            f"WARNING: No extractable SVG found in '{selector}'.\n"
            f"  The content uses HTML/CSS which cannot produce true vector SVG.\n"
            f"  Falling back to PNG: {fallback_path}\n"
            f"  TIP: For vector SVG output, redesign using a root <svg> element inside '{selector}'.",
            file=sys.stderr
        )
        return render_png(page, fallback_path, selector)


def main():
    parser = argparse.ArgumentParser(description='Render HTML to PNG or SVG')
    parser.add_argument('input', help='Path to input HTML file')
    parser.add_argument('output', help='Output path (.png or .svg)')
    parser.add_argument('--width', type=int, default=1920, help='Viewport width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Viewport height (default: 1080)')
    parser.add_argument('--scale', type=float, default=2, help='Device scale factor for PNG (default: 2)')
    parser.add_argument('--selector', default='.canvas', help='CSS selector for target element (default: .canvas)')
    parser.add_argument('--full-page', action='store_true', help='Capture full page instead of element')

    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_ext = output_path.suffix.lower()
    if output_ext not in ('.png', '.svg'):
        print(f"ERROR: Output must be .png or .svg, got: {output_ext}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = _launch_browser(p)

        scale = args.scale if output_ext == '.png' else 1
        context = browser.new_context(
            viewport={'width': args.width, 'height': args.height},
            device_scale_factor=scale,
        )
        page = context.new_page()

        # Load HTML — use set_content for reliability in container environments
        html_content = input_path.read_text(encoding='utf-8')
        page.set_content(html_content, wait_until='domcontentloaded')
        page.wait_for_timeout(500)  # let CSS transitions settle

        if args.full_page:
            if output_ext == '.png':
                page.screenshot(path=str(output_path), full_page=True)
                size = output_path.stat().st_size
                print(f"PNG (full page) saved: {output_path}")
                print(f"  Size: {size:,} bytes ({size / 1024:.1f} KB)")
                actual = str(output_path)
            else:
                print("ERROR: --full-page with SVG not supported.", file=sys.stderr)
                sys.exit(1)
        else:
            if output_ext == '.png':
                actual = render_png(page, str(output_path), args.selector)
            else:
                actual = render_svg(page, str(output_path), args.selector)

        browser.close()

    print(f"\nDone. Output: {actual}")
    return actual


if __name__ == '__main__':
    main()
