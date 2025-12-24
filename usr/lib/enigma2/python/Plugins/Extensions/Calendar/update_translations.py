#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
###########################################################
#                                                         #
#  Created by: Lululla                                    #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Lululla                    #
#  • Event system & modifications: Lululla                #
#  Last Updated: 2025-12-25                               #
#  Status: Stable with all systems integrated             #
###########################################################
"""

import os
import re
import subprocess
from xml.etree import ElementTree as ET

# ===== CONFIGURAZIONE =====
PLUGIN_NAME = "Calendar"
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(PLUGIN_DIR, "locale")
POT_FILE = os.path.join(LOCALE_DIR, f"{PLUGIN_NAME}.pot")


# ===== 1. ESTRAI STRINGHE DA setup.xml =====
def extract_xml_strings():
    """Estrae tutte le stringhe da setup.xml"""
    xml_file = os.path.join(PLUGIN_DIR, "setup.xml")

    if not os.path.exists(xml_file):
        print(f"ERRORE: {xml_file} non trovato!")
        return []

    strings = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Cerca in tutti i tag rilevanti
        for elem in root.findall('.//*[@text]'):
            text = elem.get('text', '').strip()
            if text and not re.match(r'^#[0-9a-fA-F]{6,8}$', text):
                strings.append(('text', text))

        for elem in root.findall('.//*[@description]'):
            desc = elem.get('description', '').strip()
            if desc and not re.match(r'^#[0-9a-fA-F]{6,8}$', desc):
                strings.append(('description', desc))

        for elem in root.findall('.//*[@title]'):
            title = elem.get('title', '').strip()
            if title:
                strings.append(('title', title))

    except Exception as e:
        print(f"ERRORE parsing XML: {e}")
        return []

    # Rimuovi duplicati
    seen = set()
    unique = []
    for _, text in strings:
        if text not in seen:
            seen.add(text)
            unique.append(text)

    print(f"XML: trovate {len(unique)} stringhe uniche")
    return unique


# ===== 2. ESTRAI STRINGHE DA FILE PYTHON (usando xgettext) =====
def extract_python_strings():
    """Estrae stringhe da tutti i file .py usando xgettext"""
    py_strings = []

    try:
        # Crea file .pot temporaneo da Python
        temp_pot = os.path.join(PLUGIN_DIR, "temp_python.pot")

        # Trova tutti i file .py
        py_files = []
        for root_dir, _, files in os.walk(PLUGIN_DIR):
            for f in files:
                if f.endswith('.py') and not f.startswith('test_'):
                    py_files.append(os.path.join(root_dir, f))

        if not py_files:
            print("Nessun file .py trovato")
            return []

        # Comando xgettext
        cmd = [
            'xgettext',
            '--no-wrap',
            '-L', 'Python',
            '--from-code=UTF-8',
            '-kpgettext:1c,2',
            '--add-comments=TRANSLATORS:',
            '-d', PLUGIN_NAME,
            '-s',
            '-o', temp_pot
        ] + py_files

        # Esegui xgettext
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"ERRORE xgettext: {result.stderr}")
            return []

        # Leggi le stringhe dal file .pot temporaneo
        if os.path.exists(temp_pot):
            with open(temp_pot, 'r', encoding='utf-8') as f:
                content = f.read()
                # Estrai tutti i msgid
                for match in re.finditer(r'msgid "([^"]+)"', content):
                    text = match.group(1)
                    if text and text.strip():
                        py_strings.append(text.strip())

            os.remove(temp_pot)

        print(f"Python: trovate {len(py_strings)} stringhe")
        return py_strings

    except Exception as e:
        print(f"ERRORE estrazione Python: {e}")
        return []


# ===== 3. CREA/MODIFICA IL FILE .POT =====
def update_pot_file(xml_strings, py_strings):
    """Crea o aggiorna il file .pot finale"""

    # Assicurati che la cartella esista
    os.makedirs(LOCALE_DIR, exist_ok=True)

    # Unisci tutte le stringhe
    all_strings = list(set(xml_strings + py_strings))
    all_strings.sort()  # Ordina alfabeticamente

    print(f"TOTALE: {len(all_strings)} stringhe uniche")

    # Leggi il file .pot esistente per preservare i commenti
    existing_translations = {}
    pot_header = ""

    if os.path.exists(POT_FILE):
        with open(POT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

            # Separa header (tutto prima del primo msgid)
            parts = content.split('msgid "')
            if len(parts) > 1:
                pot_header = parts[0]

            # Estrai traduzioni esistenti
            for match in re.finditer(r'msgid "([^"]+)"\s*\nmsgstr "([^"]*)"', content, re.DOTALL):
                msgid = match.group(1)
                msgstr = match.group(2)
                existing_translations[msgid] = msgstr

    # Scrivi il nuovo file .pot
    with open(POT_FILE, 'w', encoding='utf-8') as f:
        # Header
        if pot_header:
            f.write(pot_header)
        else:
            f.write(f'''# {PLUGIN_NAME} translations
# Copyright (C) 2025 Calendar Team
# This file is distributed under the same license as the Calendar package.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2025.
#
msgid ""
msgstr ""
"Project-Id-Version: {PLUGIN_NAME}\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: \\n"
"PO-Revision-Date: \\n"
"Last-Translator: \\n"
"Language-Team: \\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

''')

        # Scrivi tutte le stringhe
        for msgid in all_strings:
            f.write('\n')
            f.write(f'msgid "{msgid}"\n')
            f.write(f'msgstr "{existing_translations.get(msgid, "")}"\n')

    print(f"File .pot aggiornato: {POT_FILE}")
    return len(all_strings)


# ===== 4. AGGIORNA I FILE .PO ESISTENTI =====
def update_po_files():
    """Aggiorna tutti i file .po con le nuove stringhe"""

    if not os.path.exists(POT_FILE):
        print("ERRORE: File .pot non trovato")
        return

    # Trova tutte le cartelle delle lingue
    for lang_dir in os.listdir(LOCALE_DIR):
        po_dir = os.path.join(LOCALE_DIR, lang_dir, "LC_MESSAGES")
        po_file = os.path.join(po_dir, f"{PLUGIN_NAME}.po")

        if os.path.isdir(os.path.join(LOCALE_DIR, lang_dir)) and lang_dir != 'templates':
            if os.path.exists(po_file):
                print(f"Aggiornando: {lang_dir}")

                # Usa msgmerge per aggiornare il .po
                cmd = [
                    'msgmerge',
                    '--update',
                    '--backup=none',
                    '--no-wrap',
                    '-s',
                    po_file,
                    POT_FILE
                ]

                try:
                    subprocess.run(cmd, check=True, capture_output=True, text=True)
                    print(f"  ✓ {lang_dir} aggiornato")
                except subprocess.CalledProcessError as e:
                    print(f"  ✗ ERRORE aggiornamento {lang_dir}: {e.stderr}")
            else:
                # Crea nuovo file .po
                os.makedirs(po_dir, exist_ok=True)
                cmd = ['msginit', '-i', POT_FILE, '-o', po_file, '-l', lang_dir]
                try:
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"  ✓ Creato nuovo file per: {lang_dir}")
                except:
                    print(f"  ✗ ERRORE creazione file per: {lang_dir}")


# ===== 5. COMPILA I FILE .MO =====
def compile_mo_files():
    """Compila tutti i file .po in .mo"""

    for lang_dir in os.listdir(LOCALE_DIR):
        po_dir = os.path.join(LOCALE_DIR, lang_dir, "LC_MESSAGES")
        po_file = os.path.join(po_dir, f"{PLUGIN_NAME}.po")
        mo_file = os.path.join(po_dir, f"{PLUGIN_NAME}.mo")

        if os.path.exists(po_file):
            try:
                cmd = ['msgfmt', po_file, '-o', mo_file]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✓ Compilato: {lang_dir}/LC_MESSAGES/{PLUGIN_NAME}.mo")
            except subprocess.CalledProcessError as e:
                print(f"✗ ERRORE compilazione {lang_dir}: {e.stderr}")


# ===== MAIN =====
def main():
    print("=" * 50)
    print(f"AGGIORNAMENTO TRADUZIONI: {PLUGIN_NAME}")
    print("=" * 50)

    # 1. Estrai stringhe
    xml_strings = extract_xml_strings()
    py_strings = extract_python_strings()

    if not xml_strings and not py_strings:
        print("Nessuna stringa trovata!")
        return

    # 2. Aggiorna .pot
    total = update_pot_file(xml_strings, py_strings)

    # 3. Aggiorna .po esistenti
    update_po_files()

    # 4. Compila .mo
    compile_mo_files()

    print("\n" + "=" * 50)
    print(f"COMPLETATO: {total} stringhe nel catalogo")
    print("Ora puoi usare PoEdit su Windows senza problemi!")
    print("=" * 50)


if __name__ == "__main__":
    main()
