#!/usr/bin/env python3
"""
Generate appcast.xml for Sparkle/WinSparkle auto-updates.

This script generates an appcast XML file that can be used by both
Sparkle (macOS) and WinSparkle (Windows) for auto-update functionality.

Usage:
    python generate_appcast.py --version 2.1.0 \
        --win-url https://github.com/.../OrcaSlicer_Windows.exe \
        --win-signature "BASE64_SIGNATURE" \
        --win-length 150000000 \
        --mac-url https://github.com/.../OrcaSlicer_Mac.dmg \
        --mac-signature "BASE64_SIGNATURE" \
        --mac-length 200000000 \
        --release-notes-url https://github.com/.../releases/tag/v2.1.0 \
        --output appcast.xml
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from xml.dom import minidom


SPARKLE_NS = "http://www.andymatuschak.org/xml-namespaces/sparkle"
DC_NS = "http://purl.org/dc/elements/1.1/"


def create_appcast(
    version: str,
    release_notes_url: str,
    win_url: str = None,
    win_signature: str = None,
    win_length: int = None,
    mac_url: str = None,
    mac_signature: str = None,
    mac_length: int = None,
    title: str = "OrcaSlicer Updates",
    description: str = "Most recent updates to OrcaSlicer",
    link: str = "https://github.com/OrcaSlicer/OrcaSlicer",
) -> str:
    """
    Create an appcast XML string.

    Args:
        version: Version string (e.g., "2.1.0")
        release_notes_url: URL to release notes HTML page
        win_url: Download URL for Windows installer
        win_signature: EdDSA signature for Windows installer
        win_length: File size in bytes for Windows installer
        mac_url: Download URL for macOS DMG
        mac_signature: EdDSA signature for macOS DMG
        mac_length: File size in bytes for macOS DMG
        title: Feed title
        description: Feed description
        link: Link to project homepage

    Returns:
        XML string of the appcast
    """
    # Register namespaces
    ET.register_namespace("sparkle", SPARKLE_NS)
    ET.register_namespace("dc", DC_NS)

    # Create root RSS element
    rss = ET.Element("rss")
    rss.set("version", "2.0")
    rss.set(f"xmlns:sparkle", SPARKLE_NS)
    rss.set(f"xmlns:dc", DC_NS)

    # Create channel
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = link
    ET.SubElement(channel, "description").text = description
    ET.SubElement(channel, "language").text = "en"

    # Create item for this release
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"Version {version}"

    # Publication date in RFC 2822 format
    pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    ET.SubElement(item, "pubDate").text = pub_date

    # Release notes link
    release_notes = ET.SubElement(item, f"{{{SPARKLE_NS}}}releaseNotesLink")
    release_notes.text = release_notes_url

    # Windows enclosure
    if win_url and win_signature:
        win_enclosure = ET.SubElement(item, "enclosure")
        win_enclosure.set("url", win_url)
        win_enclosure.set(f"{{{SPARKLE_NS}}}version", version)
        win_enclosure.set(f"{{{SPARKLE_NS}}}os", "windows")
        win_enclosure.set(f"{{{SPARKLE_NS}}}edSignature", win_signature)
        if win_length:
            win_enclosure.set("length", str(win_length))
        win_enclosure.set("type", "application/octet-stream")

    # macOS enclosure
    if mac_url and mac_signature:
        mac_enclosure = ET.SubElement(item, "enclosure")
        mac_enclosure.set("url", mac_url)
        mac_enclosure.set(f"{{{SPARKLE_NS}}}version", version)
        mac_enclosure.set(f"{{{SPARKLE_NS}}}os", "macos")
        mac_enclosure.set(f"{{{SPARKLE_NS}}}edSignature", mac_signature)
        if mac_length:
            mac_enclosure.set("length", str(mac_length))
        mac_enclosure.set("type", "application/octet-stream")

    # Convert to pretty-printed string
    rough_string = ET.tostring(rss, encoding="unicode", method="xml")
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding=None)

    # Remove extra blank lines
    lines = [line for line in pretty_xml.split("\n") if line.strip()]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate appcast.xml for OrcaSlicer auto-updates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--version", "-v", required=True, help="Version string (e.g., 2.1.0)"
    )
    parser.add_argument(
        "--release-notes-url",
        "-r",
        required=True,
        help="URL to release notes page",
    )
    parser.add_argument(
        "--win-url", help="Download URL for Windows installer"
    )
    parser.add_argument(
        "--win-signature", help="EdDSA signature for Windows installer"
    )
    parser.add_argument(
        "--win-length", type=int, help="File size in bytes for Windows installer"
    )
    parser.add_argument(
        "--mac-url", help="Download URL for macOS DMG"
    )
    parser.add_argument(
        "--mac-signature", help="EdDSA signature for macOS DMG"
    )
    parser.add_argument(
        "--mac-length", type=int, help="File size in bytes for macOS DMG"
    )
    parser.add_argument(
        "--output", "-o", default="appcast.xml", help="Output file path"
    )
    parser.add_argument(
        "--title", default="OrcaSlicer Updates", help="Feed title"
    )
    parser.add_argument(
        "--link",
        default="https://github.com/OrcaSlicer/OrcaSlicer",
        help="Project homepage URL",
    )

    args = parser.parse_args()

    # Validate that at least one platform is specified
    has_windows = args.win_url and args.win_signature
    has_macos = args.mac_url and args.mac_signature

    if not has_windows and not has_macos:
        print(
            "Error: At least one platform (Windows or macOS) must have both URL and signature",
            file=sys.stderr,
        )
        sys.exit(1)

    # Generate appcast
    xml_content = create_appcast(
        version=args.version,
        release_notes_url=args.release_notes_url,
        win_url=args.win_url,
        win_signature=args.win_signature,
        win_length=args.win_length,
        mac_url=args.mac_url,
        mac_signature=args.mac_signature,
        mac_length=args.mac_length,
        title=args.title,
        link=args.link,
    )

    # Write output
    if args.output == "-":
        print(xml_content)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(xml_content)
        print(f"Appcast written to: {args.output}")


if __name__ == "__main__":
    main()
