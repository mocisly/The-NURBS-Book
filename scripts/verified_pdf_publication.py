"""Publish a reviewed PDF atomically without writing into an editor build's open file."""
from pathlib import Path
import hashlib
import os
import shutil
import time
import uuid

def publish_pdf(source, destination, expected_sha256):
    source,destination=Path(source),Path(destination)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==expected_sha256
    temporary=destination.with_name('.'+destination.stem+'-verified-'+uuid.uuid4().hex+'.pdf')
    shutil.copy2(source,temporary)
    assert hashlib.sha256(temporary.read_bytes()).hexdigest()==expected_sha256
    try:
        for attempt in range(15):
            try:
                os.replace(temporary,destination)
                break
            except PermissionError:
                if attempt==14:raise
                time.sleep(1)
        assert hashlib.sha256(destination.read_bytes()).hexdigest()==expected_sha256
    finally:
        if temporary.exists():temporary.unlink()
