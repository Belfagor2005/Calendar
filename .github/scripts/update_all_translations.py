#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UNIVERSAL translation update script for GitHub Actions.
Works for ANY Enigma2 plugin.
Just change PLUGIN_NAME and PLUGIN_DIR.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# ===== CONFIGURATION - MODIFY THESE 2 VALUES =====
PLUGIN_NAME = "Calendar"  # CHANGE HERE for other plugin
# Examples: "Vavoo", "PlutoTV", "IPAudio", etc.

# Relative path of the plugin from repository root
PLUGIN_DIR_RELATIVE = Path("usr/lib/enigma2/python/Plugins/Extensions/Calendar")
# CHANGE HERE if structure is different
# Example Vavoo: Path("usr/lib/enigma2/python/Plugins/Extensions/Vavoo")
# ===== END CONFIGURATION =====

# Script runs from repository root
REPO_ROOT = Path.cwd()
PLUGIN_DIR = REPO_ROOT / PLUGIN_DIR_RELATIVE
LOCALE_DIR = PLUGIN_DIR / "locale"
POT_FILE = LOCALE_DIR / f"{PLUGIN_NAME}.pot"

print("=" * 70)
print(f"PLUGIN: {PLUGIN_NAME}")
print(f"Plugin directory: {PLUGIN_DIR}")
print(f"Locale directory: {LOCALE_DIR}")
print("=" * 70)

# ===== 1. VERIFY STRUCTURE =====
def check_structure():
    """Verify that the plugin structure exists"""
    
    print("\n1. Verifying structure...")
    
    if not PLUGIN_DIR.exists():
        print(f"ERROR: Plugin directory not found: {PLUGIN_DIR}")
        print("\nAvailable directories in repository:")
        for item in REPO_ROOT.iterdir():
            if item.is_dir():
                print(f"  {item.name}/")
        sys.exit(1)
    
    print(f"✓ Plugin directory exists")
    
    # Check for setup.xml
    setup_xml = PLUGIN_DIR / "setup.xml"
    if not setup_xml.exists():
        print(f"WARNING: setup.xml not found in {PLUGIN_DIR}")
        print("Looking for setup files:")
        for xml_file in PLUGIN_DIR.glob("setup*.xml"):
            print(f"  Found: {xml_file.name}")
    else:
        print(f"✓ setup.xml found")
    
    # Check Python files
    py_files = list(PLUGIN_DIR.rglob("*.py"))
    print(f"✓ {len(py_files)} Python files found")
    
    # Check locale directory
    if not LOCALE_DIR.exists():
        print(f"WARNING: locale directory not found, will be created")
    else:
        print(f"✓ locale directory exists")
    
    return True

# ===== 2. EXTRACT FROM SETUP.XML =====
def extract_from_xml():
    """Extract strings from setup.xml file"""
    
    strings = set()
    setup_xml = PLUGIN_DIR / "setup.xml"
    
    if not setup_xml.exists():
        print("No setup.xml file found")
        return []
    
    print(f"\n2. Extracting from {setup_xml.name}...")
    
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(setup_xml)
        root = tree.getroot()
        
        extracted = 0
        for elem in root.iter():
            for attr in ['text', 'description', 'title']:
                if attr in elem.attrib:
                    text = elem.attrib[attr].strip()
                    if text and text not in ["None", ""]:
                        if not re.match(r'^#[0-9a-fA-F]{6,8}$', text):
                            strings.add(text)
                            extracted += 1
        
        print(f"✓ {extracted} strings extracted from setup.xml")
        
    except Exception as e:
        print(f"ERROR parsing setup.xml: {e}")
    
    return sorted(strings)

# ===== 3. EXTRACT FROM PYTHON FILES =====
def extract_from_python():
    """Extract strings from all .py files"""
    
    py_files = list(PLUGIN_DIR.rglob("*.py"))
    
    if not py_files:
        print("No Python files found")
        return []
    
    print(f"\n3. Extracting from {len(py_files)} Python files...")
    
    original_cwd = os.getcwd()
    os.chdir(PLUGIN_DIR)
    
    try:
        temp_pot = Path("temp_py.pot")
        cmd = [
            'xgettext',
            '--no-wrap',
            '-L', 'Python',
            '--from-code=UTF-8',
            '-kpgettext:1c,2',
            '-k_:1,2',
            '-k_:1',
            '--add-comments=TRANSLATORS:',
            '-d', PLUGIN_NAME,
            '-o', str(temp_pot),
        ] + [str(f.relative_to(PLUGIN_DIR)) for f in py_files]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"xgettext warning: {result.stderr[:200]}")
        
        strings = set()
        if temp_pot.exists():
            with open(temp_pot, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in re.finditer(r'msgid "([^"]+)"', content):
                    text = match.group(1)
                    if text and text.strip() and text != '""':
                        strings.add(text.strip())
            
            temp_pot.unlink()
        
        print(f"✓ {len(strings)} strings extracted from Python files")
        return sorted(strings)
        
    except Exception as e:
        print(f"ERROR with xgettext: {e}")
        return []
    finally:
        os.chdir(original_cwd)

# ===== 4. UPDATE .POT FILE =====
def update_pot_file(xml_strings, py_strings):
    """Add new strings to .pot file"""
    
    all_strings = sorted(set(xml_strings + py_strings))
    
    if not all_strings:
        print("No strings to process")
        return 0
    
    LOCALE_DIR.mkdir(exist_ok=True)
    
    existing_strings = set()
    if POT_FILE.exists():
        with open(POT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in re.finditer(r'msgid "([^"]+)"', content):
                existing_strings.add(match.group(1))
    
    new_strings = [s for s in all_strings if s not in existing_strings]
    
    if not new_strings:
        print("No new strings for .pot file")
        return 0
    
    print(f"\n4. Adding {len(new_strings)} new strings to {POT_FILE.name}...")
    
    with open(POT_FILE, 'a', encoding='utf-8') as f:
        f.write('\n# New strings - GitHub Action\n')
        for text in new_strings:
            escaped = text.replace('"', '\\"')
            f.write(f'\nmsgid "{escaped}"\n')
            f.write('msgstr ""\n')
    
    return len(new_strings)

# ===== 5. UPDATE ALL .PO FILES =====
def update_po_files():
    """Update all .po files with msgmerge"""
    
    if not POT_FILE.exists():
        print("ERROR: .pot file not found")
        return 0
    
    if not LOCALE_DIR.exists():
        print("No locale directory found")
        return 0
    
    print(f"\n5. Updating .po files in {LOCALE_DIR}...")
    
    updated = 0
    po_files = list(LOCALE_DIR.rglob("*.po"))
    
    if not po_files:
        print("No .po files found")
        return 0
    
    print(f"Found {len(po_files)} .po files")
    
    for po_file in po_files:
        if po_file.name == f"{PLUGIN_NAME}.po":
            # Get language from directory structure
            try:
                # Find the language directory (any directory inside locale/)
                rel_path = po_file.relative_to(LOCALE_DIR)
                # First directory after locale/ is usually language code
                lang = rel_path.parts[0] if len(rel_path.parts) > 1 else "unknown"
            except:
                lang = "unknown"
            
            print(f"  Updating {lang}...", end=" ")
            
            try:
                cmd = [
                    'msgmerge',
                    '--update',
                    '--backup=none',
                    '--no-wrap',
                    '--sort-output',
                    '--previous',
                    str(po_file),
                    str(POT_FILE)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("OK")
                    updated += 1
                else:
                    print(f"ERROR: {result.stderr[:100]}")
                    
            except Exception as e:
                print(f"EXCEPTION: {e}")
    
    return updated

# ===== 6. MAIN =====
def main():
    print("\n" + "=" * 70)
    print(f"GITHUB ACTION - TRANSLATION UPDATE FOR {PLUGIN_NAME}")
    print("=" * 70)
    
    # 1. Check structure
    if not check_structure():
        return
    
    # 2. Extract strings
    xml_strings = extract_from_xml()
    py_strings = extract_from_python()
    
    if not xml_strings and not py_strings:
        print("\nNo strings found to update")
        return
    
    # 3. Update .pot file
    new_strings = update_pot_file(xml_strings, py_strings)
    
    if new_strings == 0:
        print("\nNo updates needed")
        return
    
    # 4. Update .po files
    updated_langs = update_po_files()
    
    print("\n" + "=" * 70)
    print(f"COMPLETED SUCCESSFULLY!")
    print(f"  Plugin: {PLUGIN_NAME}")
    print(f"  New strings added: {new_strings}")
    print(f"  Languages updated: {updated_langs}")
    print("=" * 70)
    print("\nNOTE: .mo files were NOT compiled.")
    print("      Compile them manually after PR merge.")

if __name__ == "__main__":
    main()