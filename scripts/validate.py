#!/usr/bin/env python3
from __future__ import annotations

import collections
import glob
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_schema(name: str):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def main() -> int:
    manifest = load_yaml(ROOT / "manifest.yaml")
    catalog_validator = Draft202012Validator(load_schema("catalog.schema.json"))
    point_validator = Draft202012Validator(load_schema("knowledge-point.schema.json"))
    errors: list[str] = []
    all_ids: set[str] = set()
    total_points = total_questions = 0

    for curriculum in manifest.get("curricula", []):
        catalog_path = ROOT / curriculum["catalog"]
        catalog = load_yaml(catalog_path)
        for error in catalog_validator.iter_errors(catalog):
            errors.append(f"{catalog_path.relative_to(ROOT)}: {error.message}")

        referenced = []
        for volume in catalog.get("volumes", []):
            for chapter in volume.get("chapters", []):
                for section in chapter.get("sections", []):
                    referenced.extend(section.get("knowledge_points", []))
        duplicates = [item for item, count in collections.Counter(referenced).items() if count > 1]
        if duplicates:
            errors.append(f"{curriculum['id']}: duplicate catalog references: {duplicates}")

        point_files = [Path(item) for item in sorted(glob.glob(str(ROOT / curriculum["knowledge_glob"])))]
        points = {}
        for path in point_files:
            point = load_yaml(path)
            for error in point_validator.iter_errors(point):
                errors.append(f"{path.relative_to(ROOT)}: {error.message}")
            point_id = point.get("id", "")
            if point_id in all_ids:
                errors.append(f"duplicate knowledge point id: {point_id}")
            all_ids.add(point_id)
            points[point_id] = point
            total_points += 1

            question_ids = [question.get("id") for question in point.get("questions", [])]
            if len(question_ids) != len(set(question_ids)):
                errors.append(f"{point_id}: duplicate question ids")
            difficulties = collections.Counter(
                question.get("difficulty") for question in point.get("questions", [])
            )
            if difficulties != {"basic": 2, "medium": 2, "advanced": 1}:
                errors.append(f"{point_id}: invalid difficulty distribution {dict(difficulties)}")
            for question in point.get("questions", []):
                option_ids = [option.get("id") for option in question.get("options", [])]
                option_texts = [option.get("text") for option in question.get("options", [])]
                if len(set(option_ids)) != 4 or len(set(option_texts)) != 4:
                    errors.append(f"{question.get('id')}: options must be unique")
                if question.get("correct_option_id") not in option_ids:
                    errors.append(f"{question.get('id')}: correct option is missing")
            total_questions += len(point.get("questions", []))

        missing = sorted(set(referenced) - set(points))
        unreferenced = sorted(set(points) - set(referenced))
        if missing:
            errors.append(f"{curriculum['id']}: missing knowledge files: {missing}")
        if unreferenced:
            errors.append(f"{curriculum['id']}: unreferenced knowledge files: {unreferenced}")
        print(
            f"{curriculum['label']}: {len(catalog.get('volumes', []))} volumes, "
            f"{len(points)} knowledge points, {sum(len(p['questions']) for p in points.values())} questions"
        )

    print(f"TOTAL: {total_points} knowledge points, {total_questions} questions")
    if errors:
        print("\nVALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

