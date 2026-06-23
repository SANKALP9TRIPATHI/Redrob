"""
Memory-efficient JSONL data loader with streaming support.
"""

import json
import gzip
from pathlib import Path


def load_candidates(path, max_candidates=None):
    """
    Load candidates from JSONL or gzipped JSONL file.
    Streams line-by-line to keep memory usage low.
    """
    path = Path(path)

    if path.suffix == '.gz':
        opener = lambda: gzip.open(path, 'rt', encoding='utf-8')
    elif path.suffix == '.json':
        # Handle the sample_candidates.json (plain JSON array)
        with open(path, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
        if max_candidates:
            candidates = candidates[:max_candidates]
        return candidates
    else:
        opener = lambda: open(path, 'r', encoding='utf-8')

    candidates = []
    with opener() as f:
        for i, line in enumerate(f):
            if max_candidates and i >= max_candidates:
                break
            line = line.strip()
            if line:
                candidates.append(json.loads(line))

    return candidates


def stream_candidates(path, batch_size=5000):
    """
    Yield candidates in batches for memory-efficient processing.
    """
    path = Path(path)

    if path.suffix == '.gz':
        opener = lambda: gzip.open(path, 'rt', encoding='utf-8')
    elif path.suffix == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            candidates = json.load(f)
        for i in range(0, len(candidates), batch_size):
            yield candidates[i:i + batch_size]
        return
    else:
        opener = lambda: open(path, 'r', encoding='utf-8')

    batch = []
    with opener() as f:
        for line in f:
            line = line.strip()
            if line:
                batch.append(json.loads(line))
                if len(batch) >= batch_size:
                    yield batch
                    batch = []
    if batch:
        yield batch
