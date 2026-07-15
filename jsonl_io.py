"""Thread-safe atomic JSONL read/write with file locking.

Uses fcntl.flock for inter-process safety in concurrent batch evaluations.
Supports deduplication via job keys and automatic directory creation.
"""

import json
import os
import fcntl
from typing import Dict, Any


def job_key(game: str, difficulty: int, language: str, context: int,
            eval_mode: str = "standard") -> str:
    """Generate a unique deduplication key for a job.

    Format: "GAME100:d1:en:c0:standard"
    """
    return f"{game}:d{difficulty}:{language}:c{context}:{eval_mode}"


def exists(path: str, key: str) -> bool:
    """Check if a record with the given _job_key already exists in a JSONL file.

    Uses a shared lock (LOCK_SH) to allow concurrent reads.
    """
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            fd = f.fileno()
            fcntl.flock(fd, fcntl.LOCK_SH)
            try:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        if json.loads(line).get("_job_key") == key:
                            return True
                    except json.JSONDecodeError:
                        continue
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
    except Exception:
        pass
    return False


def append(path: str, rec: Dict[str, Any]) -> None:
    """Atomically append a JSON record to a JSONL file.

    Creates parent directories if needed.
    Uses an exclusive lock (LOCK_EX) to prevent concurrent writes from
    interleaving.

    Args:
        path: Path to the JSONL file.
        rec: Dict to serialize as a single JSON line.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        fd = f.fileno()
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
