#!/usr/bin/env python3
"""Validate DOCX ZIP/XML structure and internal package relationships."""
import argparse
import posixpath
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree


REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
INLINE_NS = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
def _owner_part(rels_path):
    if rels_path == "_rels/.rels":
        return ""
    folder, _, filename = rels_path.rpartition("/_rels/")
    if not filename.endswith(".rels"):
        raise ValueError(f"Caminho .rels inesperado: {rels_path}")
    return posixpath.join(folder, filename[:-5])


def _target_part(owner, target):
    target = unquote(target.split("#", 1)[0])
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(owner), target))


def validate_docx(path, expect_images=None):
    path = Path(path)
    errors = []
    if not path.is_file():
        return [f"Arquivo não encontrado: {path}"], None

    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Pacote ZIP inválido: {exc}"], None

    with archive:
        names = set(archive.namelist())
        required = {
            "[Content_Types].xml",
            "_rels/.rels",
            "word/document.xml",
            "word/_rels/document.xml.rels",
        }
        missing = sorted(required - names)
        if missing:
            errors.append(f"Partes obrigatórias ausentes: {', '.join(missing)}")

        bad_member = archive.testzip()
        if bad_member:
            errors.append(f"CRC inválido no membro ZIP: {bad_member}")

        xml_roots = {}
        for name in sorted(names):
            if not name.endswith((".xml", ".rels")):
                continue
            try:
                xml_roots[name] = ElementTree.fromstring(archive.read(name))
            except (ElementTree.ParseError, KeyError) as exc:
                errors.append(f"XML inválido em {name}: {exc}")

        relationships = {}
        for rels_path, root in xml_roots.items():
            if not rels_path.endswith(".rels"):
                continue
            owner = _owner_part(rels_path)
            rels = {}
            for rel in root:
                rel_id = rel.attrib.get("Id")
                target = rel.attrib.get("Target")
                if not rel_id or not target:
                    errors.append(f"Relação incompleta em {rels_path}")
                    continue
                rels[rel_id] = rel
                if rel.attrib.get("TargetMode") == "External":
                    continue
                part = _target_part(owner, target)
                if part not in names:
                    errors.append(
                        f"Destino interno ausente em {rels_path}: {rel_id} -> {part}"
                    )
            relationships[owner] = rels

        for part_path, root in xml_roots.items():
            if part_path.endswith(".rels"):
                continue
            rel_ids = relationships.get(part_path, {})
            for element in root.iter():
                for attr, value in element.attrib.items():
                    if attr.startswith(REL_NS) and value not in rel_ids:
                        errors.append(
                            f"Relação {value!r} não encontrada para {part_path}"
                        )

        root_rels = relationships.get("", {})
        if root_rels and not any(
            rel.attrib.get("Type", "").endswith("/officeDocument")
            for rel in root_rels.values()
        ):
            errors.append("Relação principal officeDocument ausente")

        document = xml_roots.get("word/document.xml")
        if document is None:
            return errors, None
        text = "".join(
            node.text or ""
            for node in document.iter()
            if node.tag == f"{WORD_NS}t"
        )
        if not text.strip():
            errors.append("O documento não contém texto visível")

        inline_images = sum(
            1 for node in document.iter() if node.tag == f"{INLINE_NS}inline"
        )
        if inline_images == 0:
            errors.append("O documento não contém imagens incorporadas")
        if expect_images is not None and inline_images != expect_images:
            errors.append(
                f"Quantidade de imagens diferente do esperado: "
                f"{inline_images} (esperado: {expect_images})"
            )

        document_rels = relationships.get("word/document.xml", {})
        image_rels = {
            rel_id: rel for rel_id, rel in document_rels.items()
            if rel.attrib.get("Type", "").endswith("/image")
        }
        referenced_images = {
            value
            for element in document.iter()
            for attr, value in element.attrib.items()
            if attr.startswith(REL_NS) and value in image_rels
        }
        if not referenced_images:
            errors.append("Nenhuma imagem do documento aponta para um recurso interno")
        for rel_id in referenced_images:
            rel = image_rels[rel_id]
            if rel.attrib.get("TargetMode") == "External":
                errors.append(f"Imagem externa não incorporada: {rel_id}")

    summary = {
        "xml_parts": sum(1 for name in names if name.endswith((".xml", ".rels"))),
        "inline_images": inline_images,
        "image_relationships_used": len(referenced_images),
        "text_characters": len(text.strip()),
    }
    return errors, summary


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Verifica ZIP/XML, relações internas e imagens do DOCX. "
            "Não substitui validação de esquema OOXML nem renderização visual."
        )
    )
    parser.add_argument("docx", type=Path, help="Arquivo DOCX a verificar")
    parser.add_argument("--expect-images", type=int)
    args = parser.parse_args(argv)
    errors, summary = validate_docx(args.docx, args.expect_images)
    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1
    print(
        "DOCX estruturalmente válido: "
        f"{summary['xml_parts']} partes XML, {summary['inline_images']} imagens "
        f"({summary['image_relationships_used']} referências), "
        f"{summary['text_characters']} caracteres de texto."
    )
    print(
        "Nota: a verificação estrutural não valida o esquema OOXML completo "
        "nem a aparência após renderização."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
