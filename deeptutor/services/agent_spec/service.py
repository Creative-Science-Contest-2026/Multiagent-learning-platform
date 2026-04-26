from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from deeptutor.services.path_service import get_path_service

SPEC_FILES: tuple[str, ...] = (
    "IDENTITY.md",
    "SOUL.md",
    "CURRICULUM.md",
    "RULES.md",
    "ASSESSMENT.md",
    "WORKFLOW.md",
    "KNOWLEDGE.md",
    "MARKETPLACE.md",
)

STRUCTURED_FILES = {"IDENTITY.md", "SOUL.md", "RULES.md"}


DEFAULT_RAW_FILES: dict[str, str] = {
    "CURRICULUM.md": "# Curriculum\n\n## Core Topics\n\n- Add the priority topics for this agent.\n",
    "ASSESSMENT.md": "# Assessment\n\n## Evidence Signals\n\n- Define what the agent should watch for.\n",
    "WORKFLOW.md": "# Workflow\n\n## Session Flow\n\n1. Teach\n2. Practice\n3. Check\n4. Remediate\n",
    "KNOWLEDGE.md": "# Knowledge\n\n## Retrieval Policy\n\n- Prefer teacher-authored materials first.\n",
    "MARKETPLACE.md": "# Marketplace\n\n## Metadata\n\n- Audience:\n- Difficulty:\n- Share status: private\n",
}

IDENTITY_FIELDS = (
    ("agent_name", "Agent Name"),
    ("subject", "Subject"),
    ("grade_band", "Grade Band"),
    ("tone", "Tone"),
    ("primary_language", "Primary Language"),
)

RULE_FIELDS = (
    ("do_not_solve_directly", "Do Not Solve Directly"),
    ("max_session_minutes", "Max Session Minutes"),
    ("hint_policy", "Hint Policy"),
    ("escalation_rule", "Escalation Rule"),
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug


def _parse_bullet_fields(markdown: str, fields: tuple[tuple[str, str], ...]) -> dict[str, str]:
    result = {key: "" for key, _ in fields}
    labels = {label: key for key, label in fields}
    pattern = re.compile(r"^- ([^:]+):\s*(.*)$", re.MULTILINE)
    for label, value in pattern.findall(markdown):
        key = labels.get(label.strip())
        if key:
            result[key] = value.strip()
    return result


def _extract_section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def _normalize_bool_text(value: str | bool) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    lowered = value.strip().lower()
    if lowered in {"true", "yes", "y", "1"}:
        return "yes"
    if lowered in {"false", "no", "n", "0"}:
        return "no"
    return value.strip()


def render_identity_markdown(data: dict[str, str]) -> str:
    lines = ["# Identity", ""]
    for key, label in IDENTITY_FIELDS:
        lines.append(f"- {label}: {data.get(key, '').strip()}")
    lines.extend(
        [
            "",
            "## Persona Summary",
            data.get("persona_summary", "").strip() or "Describe the role, subject focus, and classroom presence.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_identity_markdown(markdown: str) -> dict[str, str]:
    data = _parse_bullet_fields(markdown, IDENTITY_FIELDS)
    data["persona_summary"] = _extract_section(markdown, "Persona Summary")
    return data


def render_soul_markdown(data: dict[str, str]) -> str:
    sections = (
        ("Teaching Philosophy", data.get("teaching_philosophy", "")),
        ("When The Student Is Wrong", data.get("when_student_wrong", "")),
        ("When The Student Is Stuck", data.get("when_student_stuck", "")),
        ("Encouragement Style", data.get("encouragement_style", "")),
    )
    lines = ["# Soul", ""]
    for heading, content in sections:
        lines.extend(
            [
                f"## {heading}",
                content.strip() or "Fill in this section.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_soul_markdown(markdown: str) -> dict[str, str]:
    return {
        "teaching_philosophy": _extract_section(markdown, "Teaching Philosophy"),
        "when_student_wrong": _extract_section(markdown, "When The Student Is Wrong"),
        "when_student_stuck": _extract_section(markdown, "When The Student Is Stuck"),
        "encouragement_style": _extract_section(markdown, "Encouragement Style"),
    }


def render_rules_markdown(data: dict[str, str | bool]) -> str:
    lines = ["# Rules", ""]
    for key, label in RULE_FIELDS:
        value = data.get(key, "")
        if key == "do_not_solve_directly":
            value = _normalize_bool_text(value)
        lines.append(f"- {label}: {str(value).strip()}")
    lines.extend(
        [
            "",
            "## Guardrails",
            str(data.get("guardrails", "")).strip() or "List the operating guardrails for this teaching agent.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_rules_markdown(markdown: str) -> dict[str, str]:
    data = _parse_bullet_fields(markdown, RULE_FIELDS)
    data["guardrails"] = _extract_section(markdown, "Guardrails")
    return data


@dataclass
class AgentSpecPaths:
    root: Path
    versions_dir: Path
    metadata_file: Path


class AgentSpecService:
    def __init__(self, base_dir: Path | None = None) -> None:
        root = base_dir or (get_path_service().get_workspace_dir() / "agent_specs")
        self._base_dir = Path(root)

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    def list_packs(self) -> list[dict[str, object]]:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        packs: list[dict[str, object]] = []
        for entry in sorted(self._base_dir.iterdir()):
            if not entry.is_dir():
                continue
            metadata_path = entry / "metadata.json"
            if not metadata_path.exists():
                continue
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            packs.append(self._build_summary(entry.name, metadata))
        packs.sort(key=lambda item: str(item["updated_at"]), reverse=True)
        return packs

    def get_pack(self, agent_id: str) -> dict[str, object]:
        paths = self._get_paths(agent_id)
        if not paths.root.exists():
            raise FileNotFoundError(agent_id)
        metadata = self._read_metadata(paths)
        files = self._read_current_files(paths.root)
        return self._build_payload(agent_id, metadata, files)

    def create_pack(
        self,
        *,
        agent_id: str,
        display_name: str,
        description: str = "",
        structured: dict[str, dict[str, str | bool]] | None = None,
        files: dict[str, str] | None = None,
    ) -> dict[str, object]:
        normalized_agent_id = self._validate_agent_id(agent_id)
        paths = self._get_paths(normalized_agent_id)
        if paths.root.exists():
            raise ValueError(f"Agent spec '{normalized_agent_id}' already exists")

        now = _now_iso()
        metadata = {
            "agent_id": normalized_agent_id,
            "display_name": display_name.strip() or normalized_agent_id,
            "description": description.strip(),
            "created_at": now,
            "updated_at": now,
            "version": 1,
        }
        combined_files = self._assemble_files(structured or {}, files or {})
        self._write_pack(paths, metadata, combined_files)
        return self._build_payload(normalized_agent_id, metadata, combined_files)

    def save_pack(
        self,
        *,
        agent_id: str,
        display_name: str,
        description: str = "",
        structured: dict[str, dict[str, str | bool]] | None = None,
        files: dict[str, str] | None = None,
    ) -> dict[str, object]:
        normalized_agent_id = self._validate_agent_id(agent_id)
        paths = self._get_paths(normalized_agent_id)
        if not paths.root.exists():
            raise FileNotFoundError(normalized_agent_id)

        metadata = self._read_metadata(paths)
        metadata["display_name"] = display_name.strip() or normalized_agent_id
        metadata["description"] = description.strip()
        metadata["updated_at"] = _now_iso()
        metadata["version"] = int(metadata.get("version", 0)) + 1
        current_files = self._read_current_files(paths.root)
        combined_files = self._assemble_files(structured or {}, files or {}, current_files=current_files)
        self._write_pack(paths, metadata, combined_files)
        return self._build_payload(normalized_agent_id, metadata, combined_files)

    def export_pack_archive(self, agent_id: str) -> bytes:
        payload = self.get_pack(agent_id)
        files = payload["files"]
        assert isinstance(files, dict)

        buffer = io.BytesIO()
        with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
            for filename in SPEC_FILES:
                archive.writestr(f"{agent_id}/{filename}", str(files[filename]))
        return buffer.getvalue()

    def _validate_agent_id(self, agent_id: str) -> str:
        normalized = _slugify(agent_id)
        if not normalized:
            raise ValueError("Agent ID must contain at least one letter or number")
        return normalized

    def _get_paths(self, agent_id: str) -> AgentSpecPaths:
        root = self._base_dir / agent_id
        return AgentSpecPaths(
            root=root,
            versions_dir=root / "versions",
            metadata_file=root / "metadata.json",
        )

    def _assemble_files(
        self,
        structured: dict[str, dict[str, str | bool]],
        files: dict[str, str],
        *,
        current_files: dict[str, str] | None = None,
    ) -> dict[str, str]:
        current_files = current_files or {}
        merged = {name: current_files.get(name, DEFAULT_RAW_FILES.get(name, "")) for name in SPEC_FILES}

        identity = {key: str(value) for key, value in structured.get("identity", {}).items()}
        soul = {key: str(value) for key, value in structured.get("soul", {}).items()}
        rules = {
            key: (_normalize_bool_text(value) if key == "do_not_solve_directly" else str(value))
            for key, value in structured.get("rules", {}).items()
        }

        merged["IDENTITY.md"] = render_identity_markdown(identity)
        merged["SOUL.md"] = render_soul_markdown(soul)
        merged["RULES.md"] = render_rules_markdown(rules)

        for name in SPEC_FILES:
            if name in STRUCTURED_FILES:
                continue
            if name in files:
                merged[name] = files[name].strip() + ("\n" if not files[name].endswith("\n") else "")

        for name in SPEC_FILES:
            if not merged[name].strip():
                if name in DEFAULT_RAW_FILES:
                    merged[name] = DEFAULT_RAW_FILES[name]
                else:
                    raise ValueError(f"{name} cannot be empty")

        return merged

    def _write_pack(self, paths: AgentSpecPaths, metadata: dict[str, object], files: dict[str, str]) -> None:
        paths.root.mkdir(parents=True, exist_ok=True)
        paths.versions_dir.mkdir(parents=True, exist_ok=True)
        version_dir = paths.versions_dir / f"v{int(metadata['version']):04d}"
        version_dir.mkdir(parents=True, exist_ok=True)

        for filename, content in files.items():
            (paths.root / filename).write_text(content, encoding="utf-8")
            (version_dir / filename).write_text(content, encoding="utf-8")

        paths.metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        (version_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def _read_metadata(self, paths: AgentSpecPaths) -> dict[str, object]:
        return json.loads(paths.metadata_file.read_text(encoding="utf-8"))

    def _read_current_files(self, root: Path) -> dict[str, str]:
        return {filename: (root / filename).read_text(encoding="utf-8") for filename in SPEC_FILES}

    def _build_summary(self, agent_id: str, metadata: dict[str, object]) -> dict[str, object]:
        return {
            "agent_id": agent_id,
            "display_name": metadata.get("display_name") or agent_id,
            "description": metadata.get("description") or "",
            "version": int(metadata.get("version", 1)),
            "updated_at": metadata.get("updated_at"),
        }

    def _build_payload(
        self,
        agent_id: str,
        metadata: dict[str, object],
        files: dict[str, str],
    ) -> dict[str, object]:
        return {
            "agent_id": agent_id,
            "display_name": metadata.get("display_name") or agent_id,
            "description": metadata.get("description") or "",
            "version": int(metadata.get("version", 1)),
            "created_at": metadata.get("created_at"),
            "updated_at": metadata.get("updated_at"),
            "files": files,
            "structured": {
                "identity": parse_identity_markdown(files["IDENTITY.md"]),
                "soul": parse_soul_markdown(files["SOUL.md"]),
                "rules": parse_rules_markdown(files["RULES.md"]),
            },
            "summary": {
                "subject": parse_identity_markdown(files["IDENTITY.md"]).get("subject", ""),
                "language": parse_identity_markdown(files["IDENTITY.md"]).get("primary_language", ""),
                "teaching_philosophy": parse_soul_markdown(files["SOUL.md"]).get("teaching_philosophy", ""),
                "guardrails": parse_rules_markdown(files["RULES.md"]).get("guardrails", ""),
            },
        }


_service_instance: AgentSpecService | None = None


def get_agent_spec_service() -> AgentSpecService:
    global _service_instance
    if _service_instance is None:
        _service_instance = AgentSpecService()
    return _service_instance
