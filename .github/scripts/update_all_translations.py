#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT per aggiornamento traduzioni - DA ESEGUIRE NELLA CARTELLA DEL PLUGIN
Assumi di essere in: usr/lib/enigma2/python/Plugins/Extensions/Calendar/
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# ===== CONFIGURAZIONE =====
PLUGIN_NAME = "Calendar"
SCRIPT_DIR = Path(__file__).parent.absolute()

# IMPORTANTE: Questo script viene eseguito DALLA CARTELLA DEL PLUGIN
# cd usr/lib/enigma2/python/Plugins/Extensions/Calendar/
# python ../../../../../../.github/scripts/update_all_translations.py

# Percorsi RELATIVI alla cartella del plugin (dove siamo ora)
PLUGIN_DIR = Path.cwd()  # usr/lib/enigma2/python/Plugins/Extensions/Calendar/
LOCALE_DIR = PLUGIN_DIR / "locale"
POT_FILE = LOCALE_DIR / f"{PLUGIN_NAME}.pot"

print(f"Working directory: {PLUGIN_DIR}")
print(f"Locale directory: {LOCALE_DIR}")
print(f"POT file: {POT_FILE}")

# ===== 1. ESTRAI DA SETUP.XML =====
def extract_from_xml():
    """Estrae stringhe da setup.xml"""
    strings = set()
    
    # Cerca setup.xml nella cartella corrente
    xml_files = list(PLUGIN_DIR.glob("setup*.xml"))
    
    if not xml_files:
        print(" Nessun file setup*.xml trovato")
        return []
    
    for xml_file in xml_files:
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Cerca tutti gli elementi con attributi text/description/title
            for elem in root.iter():
                for attr in ['text', 'description', 'title']:
                    if attr in elem.attrib:
                        text = elem.attrib[attr].strip()
                        if text and text != "None":
                            # Escludi codici colore
                            if not re.match(r'^#[0-9a-fA-F]{6,8}$', text):
                                strings.add(text)
            
            print(f"📄 {xml_file.name}: {len(strings)} stringhe")
            
        except Exception as e:
            print(f"Errore parsing {xml_file}: {e}")
    
    return sorted(strings)

# ===== 2. ESTRAI DA PYTHON =====
def extract_from_python():
    """Estrae stringhe da tutti i .py"""
    py_files = list(PLUGIN_DIR.rglob("*.py"))
    
    if not py_files:
        print("  Nessun file .py trovato")
        return []
    
    # Crea comando xgettext
    temp_pot = PLUGIN_DIR / "temp_py.pot"
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
    ] + [str(f) for f in py_files]
    
    try:
        # Esegui xgettext
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f" xgettext warning: {result.stderr[:200]}")
        
        # Leggi le stringhe
        strings = set()
        if temp_pot.exists():
            with open(temp_pot, 'r', encoding='utf-8') as f:
                content = f.read()
                for match in re.finditer(r'msgid "([^"]+)"', content):
                    text = match.group(1)
                    if text and text.strip() and text != '""':
                        strings.add(text.strip())
            
            # Elimina temp file
            temp_pot.unlink()
        
        print(f"Python: {len(strings)} stringhe")
        return sorted(strings)
        
    except Exception as e:
        print(f"Errore xgettext: {e}")
        return []

# ===== 3. AGGIORNA .POT =====
def update_pot_file(xml_strings, py_strings):
    """Aggiungi nuove stringhe al .pot"""
    
    # Unisci stringhe
    all_strings = sorted(set(xml_strings + py_strings))
    
    if not all_strings:
        print(" Nessuna stringa da processare")
        return 0
    
    # Assicura che la cartella locale esista
    LOCALE_DIR.mkdir(exist_ok=True)
    
    # Leggi stringhe esistenti
    existing_strings = set()
    if POT_FILE.exists():
        with open(POT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in re.finditer(r'msgid "([^"]+)"', content):
                existing_strings.add(match.group(1))
    
    # Trova nuove stringhe
    new_strings = [s for s in all_strings if s not in existing_strings]
    
    if not new_strings:
        print("Nessuna nuova stringa per .pot")
        return 0
    
    print(f"{len(new_strings)} nuove stringhe per .pot")
    
    # Aggiungi al file .pot
    with open(POT_FILE, 'a', encoding='utf-8') as f:
        f.write('\n# New strings - GitHub Action\n')
        for text in new_strings:
            escaped = text.replace('"', '\\"')
            f.write(f'\nmsgid "{escaped}"\n')
            f.write('msgstr ""\n')
    
    return len(new_strings)

# ===== 4. AGGIORNA TUTTI I .PO =====
def update_po_files():
    """Aggiorna tutti i file .po con msgmerge"""
    
    if not POT_FILE.exists():
        print("File .pot non trovato")
        return 0
    
    updated = 0
    
    # Cerca tutti i .po nelle sottocartelle di locale/
    for po_file in LOCALE_DIR.rglob("*.po"):
        if po_file.name == f"{PLUGIN_NAME}.po":
            # Ottieni la lingua dal percorso
            parts = po_file.parts
            try:
                # Trova l'indice di 'locale' e prendi il prossimo elemento
                locale_idx = parts.index('locale')
                if locale_idx + 1 < len(parts):
                    lang = parts[locale_idx + 1]
                else:
                    lang = "unknown"
            except:
                lang = "unknown"
            
            print(f"Aggiornando {lang}...")
            
            try:
                # Usa msgmerge
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
                    print(f"  {lang} aggiornato")
                    updated += 1
                else:
                    print(f"   {lang}: {result.stderr[:100]}")
                    
            except Exception as e:
                print(f"  {lang}: {e}")
    
    return updated

# ===== 5. MAIN =====
def main():
    print("=" * 60)
    print("GITHUB ACTION - AGGIORNAMENTO TRADUZIONI")
    print("=" * 60)
    
    # 1. Estrai stringhe
    print("\n1. Estrazione stringhe...")
    xml_strings = extract_from_xml()
    py_strings = extract_from_python()
    
    if not xml_strings and not py_strings:
        print("Nessuna stringa trovata")
        return
    
    # 2. Aggiorna .pot
    print(f"\n2. Aggiornamento {POT_FILE.name}...")
    new_strings = update_pot_file(xml_strings, py_strings)
    
    if new_strings == 0:
        print("Nessun aggiornamento necessario")
        return
    
    # 3. Aggiorna .po
    print(f"\n3. Aggiornamento file .po...")
    updated_langs = update_po_files()
    
    print("\n" + "=" * 60)
    print(f"COMPLETATO!")
    print(f"   • Nuove stringhe: {new_strings}")
    print(f"   • Lingue aggiornate: {updated_langs}")
    print("=" * 60)
    print("\nI file .mo NON sono stati compilati.")
    print("   Compilali manualmente dopo il merge della PR.")

if __name__ == "__main__":
    main()