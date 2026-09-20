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

GENERIC_QUESTION_FRAGMENTS = (
    "最需要把握的核心内容",
    "学习方法最恰当",
    "学习，下列做法最需要避免",
    "较合理的步骤",
    "最可靠的判断依据",
)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_schema(name: str):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def matching_files(pattern: str) -> list[Path]:
    return [
        Path(item)
        for item in sorted(glob.glob(str(ROOT / pattern), recursive=True))
    ]


def collect_schema_errors(
    validator: Draft202012Validator,
    value: dict,
    path: Path,
    errors: list[str],
) -> None:
    for error in validator.iter_errors(value):
        errors.append(f"{path.relative_to(ROOT)}: {error.message}")


def validate_knowledge_content(point: dict, errors: list[str]) -> None:
    point_id = point.get("id", "")
    knowledge_items = point.get("knowledge_items", [])
    item_ids = [item.get("id") for item in knowledge_items]
    item_names = [item.get("name") for item in knowledge_items]
    if len(item_ids) != len(set(item_ids)):
        errors.append(f"{point_id}: duplicate detailed knowledge item ids")
    if len(item_names) != len(set(item_names)):
        errors.append(f"{point_id}: duplicate detailed knowledge item names")
    if point.get("subject") != "math":
        return
    formulas = [
        formula
        for item in knowledge_items
        for formula in item.get("formulas", [])
    ]
    if not formulas:
        errors.append(f"{point_id}: math point must include formulas")
    for formula in formulas:
        if formula.count("{") != formula.count("}"):
            errors.append(f"{point_id}: unbalanced LaTeX braces in {formula}")
    for item in knowledge_items:
        if item.get("type") == "theorem" and (
            "conditions" not in item or not item.get("conclusion")
        ):
            errors.append(
                f"{point_id}.{item.get('id')}: theorem requires conditions and conclusion"
            )


def validate_question_quality(
    question: dict,
    bank: dict,
    canonical_points: dict[str, dict],
    question_signatures: dict[tuple[str, tuple[str, ...]], str],
    errors: list[str],
) -> None:
    question_id = question.get("id", "")
    options = question.get("options", [])
    option_ids = [option.get("id") for option in options]
    option_texts = [option.get("text") for option in options]
    if question.get("question_type") == "single_choice":
        if len(set(option_ids)) != 4 or len(set(option_texts)) != 4:
            errors.append(f"{question_id}: single-choice options must contain four unique values")
        if question.get("correct_option_id") not in option_ids:
            errors.append(f"{question_id}: correct option is missing")
    if not set(question.get("knowledge_point_ids", [])).issubset(
        set(bank.get("canonical_knowledge_ids", []))
    ):
        errors.append(f"{question_id}: knowledge scope exceeds its question bank")
    if not set(question.get("curriculum_scopes", [])).issubset(
        set(bank.get("curriculum_scopes", []))
    ):
        errors.append(f"{question_id}: curriculum scope exceeds its question bank")
    if question.get("education_stage") != bank.get("education_stage"):
        errors.append(f"{question_id}: education stage differs from its question bank")
    if not set(question.get("grade_scope", [])).issubset(set(bank.get("grade_scope", []))):
        errors.append(f"{question_id}: grade scope exceeds its question bank")

    point_ids = question.get("knowledge_point_ids", [])
    points = [canonical_points[item] for item in point_ids if item in canonical_points]
    if bank.get("subject") == "history" and len(points) == len(point_ids):
        item_names = {
            item["name"]
            for point in points
            for item in point.get("knowledge_items", [])
        }
        if question.get("difficulty") == "basic" and not set(option_texts).issubset(
            item_names
        ):
            errors.append(f"{question_id}: basic history distractors must be same-point topics")
        if question.get("difficulty") != "basic" and any(
            option in item_names or len(option) < 10 for option in option_texts
        ):
            errors.append(f"{question_id}: analytical history options must be substantive claims")

    stem = question.get("stem", "")
    if any(fragment in stem for fragment in GENERIC_QUESTION_FRAGMENTS):
        errors.append(f"{question_id}: generic meta-learning prompt is forbidden")
    signature = (stem, tuple(option_texts))
    if signature in question_signatures:
        errors.append(f"{question_id}: duplicates {question_signatures[signature]}")
    else:
        question_signatures[signature] = question_id


def main() -> int:
    manifest = load_yaml(ROOT / "manifest.yaml")
    manifest_validator = Draft202012Validator(load_schema("manifest.schema.json"))
    catalog_validator = Draft202012Validator(load_schema("catalog.schema.json"))
    knowledge_validator = Draft202012Validator(load_schema("canonical-knowledge.schema.json"))
    mapping_validator = Draft202012Validator(load_schema("curriculum-mapping.schema.json"))
    bank_validator = Draft202012Validator(load_schema("question-bank.schema.json"))
    errors: list[str] = []
    collect_schema_errors(manifest_validator, manifest, ROOT / "manifest.yaml", errors)
    question_signatures: dict[tuple[str, tuple[str, ...]], str] = {}
    canonical_points: dict[str, dict] = {}
    question_banks: dict[str, dict] = {}
    all_question_ids: set[str] = set()
    referenced_canonical_ids: set[str] = set()
    referenced_bank_ids: set[str] = set()
    all_mapping_ids: set[str] = set()

    for domain in manifest.get("knowledge_domains", []):
        paths = matching_files(domain["knowledge_glob"])
        if not paths:
            errors.append(f"{domain['knowledge_glob']}: knowledge glob matched no files")
        for path in paths:
            point = load_yaml(path)
            collect_schema_errors(knowledge_validator, point, path, errors)
            point_id = point.get("id", "")
            if point_id in canonical_points:
                errors.append(f"duplicate canonical knowledge id: {point_id}")
            canonical_points[point_id] = point
            if point.get("subject") != domain.get("subject"):
                errors.append(f"{point_id}: subject differs from knowledge domain")
            if point.get("education_stage") != domain.get("education_stage"):
                errors.append(f"{point_id}: education stage differs from knowledge domain")
            validate_knowledge_content(point, errors)

    for bank_entry in manifest.get("question_banks", []):
        paths = matching_files(bank_entry["question_glob"])
        if not paths:
            errors.append(f"{bank_entry['question_glob']}: question glob matched no files")
        for path in paths:
            bank = load_yaml(path)
            collect_schema_errors(bank_validator, bank, path, errors)
            bank_id = bank.get("id", "")
            if bank_id in question_banks:
                errors.append(f"duplicate question bank id: {bank_id}")
            question_banks[bank_id] = bank
            if bank.get("subject") != bank_entry.get("subject"):
                errors.append(f"{bank_id}: subject differs from manifest bank")
            if bank.get("education_stage") != bank_entry.get("education_stage"):
                errors.append(f"{bank_id}: education stage differs from manifest bank")
            missing_points = sorted(
                set(bank.get("canonical_knowledge_ids", [])) - set(canonical_points)
            )
            if missing_points:
                errors.append(f"{bank_id}: missing canonical knowledge: {missing_points}")
            for question in bank.get("questions", []):
                question_id = question.get("id", "")
                if question_id in all_question_ids:
                    errors.append(f"duplicate question id: {question_id}")
                all_question_ids.add(question_id)
                validate_question_quality(
                    question, bank, canonical_points, question_signatures, errors
                )

    for curriculum in manifest.get("curricula", []):
        catalog_path = ROOT / curriculum["catalog"]
        catalog = load_yaml(catalog_path)
        collect_schema_errors(catalog_validator, catalog, catalog_path, errors)

        referenced = []
        for volume in catalog.get("volumes", []):
            for chapter in volume.get("chapters", []):
                for section in chapter.get("sections", []):
                    referenced.extend(section.get("knowledge_points", []))
        duplicates = [item for item, count in collections.Counter(referenced).items() if count > 1]
        if duplicates:
            errors.append(f"{curriculum['id']}: duplicate catalog references: {duplicates}")

        mappings = {}
        curriculum_question_count = 0
        mapping_paths = matching_files(curriculum["knowledge_mapping_glob"])
        if not mapping_paths:
            errors.append(
                f"{curriculum['knowledge_mapping_glob']}: mapping glob matched no files"
            )
        for path in mapping_paths:
            mapping = load_yaml(path)
            collect_schema_errors(mapping_validator, mapping, path, errors)
            point_id = mapping.get("id", "")
            if point_id in all_mapping_ids:
                errors.append(f"duplicate curriculum mapping id: {point_id}")
            all_mapping_ids.add(point_id)
            mappings[point_id] = mapping
            canonical_id = mapping.get("canonical_id", "")
            point = canonical_points.get(canonical_id)
            if point is None:
                errors.append(f"{point_id}: missing canonical knowledge {canonical_id}")
            elif point.get("subject") != mapping.get("subject"):
                errors.append(f"{point_id}: canonical knowledge subject mismatch")
            if mapping.get("curriculum_id") != curriculum.get("id"):
                errors.append(f"{point_id}: curriculum id mismatch")
            if mapping.get("subject") != curriculum.get("subject"):
                errors.append(f"{point_id}: curriculum subject mismatch")
            referenced_canonical_ids.add(canonical_id)

            questions = []
            for bank_id in mapping.get("question_bank_ids", []):
                referenced_bank_ids.add(bank_id)
                bank = question_banks.get(bank_id)
                if bank is None:
                    errors.append(f"{point_id}: missing question bank {bank_id}")
                    continue
                if curriculum["id"] not in bank.get("curriculum_scopes", []):
                    errors.append(f"{point_id}: question bank {bank_id} is outside curriculum scope")
                if canonical_id not in bank.get("canonical_knowledge_ids", []):
                    errors.append(f"{point_id}: question bank {bank_id} is outside knowledge scope")
                if mapping.get("education_stage") != bank.get("education_stage"):
                    errors.append(f"{point_id}: question bank {bank_id} has a different stage")
                if not set(mapping.get("grade_scope", [])).issubset(
                    set(bank.get("grade_scope", []))
                ):
                    errors.append(f"{point_id}: question bank {bank_id} misses mapped grades")
                questions.extend(bank.get("questions", []))
            difficulties = collections.Counter(
                question.get("difficulty") for question in questions
            )
            if difficulties != {"basic": 2, "medium": 2, "advanced": 1}:
                errors.append(f"{point_id}: invalid difficulty distribution {dict(difficulties)}")
            for question in questions:
                if mapping.get("display_name") not in question.get("tags", []):
                    errors.append(
                        f"{question.get('id')}: tags must include curriculum display name"
                    )
            curriculum_question_count += len(questions)

        missing = sorted(set(referenced) - set(mappings))
        unreferenced = sorted(set(mappings) - set(referenced))
        if missing:
            errors.append(f"{curriculum['id']}: missing curriculum mappings: {missing}")
        if unreferenced:
            errors.append(f"{curriculum['id']}: unreferenced curriculum mappings: {unreferenced}")
        print(
            f"{curriculum['label']}: {len(catalog.get('volumes', []))} volumes, "
            f"{len(mappings)} curriculum mappings, {curriculum_question_count} questions"
        )

    orphan_points = sorted(set(canonical_points) - referenced_canonical_ids)
    orphan_banks = sorted(set(question_banks) - referenced_bank_ids)
    if orphan_points:
        errors.append(f"unreferenced canonical knowledge: {orphan_points}")
    if orphan_banks:
        errors.append(f"unreferenced question banks: {orphan_banks}")
    total_items = sum(
        len(point.get("knowledge_items", [])) for point in canonical_points.values()
    )
    print(
        f"TOTAL: {len(canonical_points)} canonical knowledge points, "
        f"{len(all_mapping_ids)} curriculum mappings, {total_items} detailed items, "
        f"{len(all_question_ids)} questions"
    )
    if errors:
        print("\nVALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
