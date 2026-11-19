"""Corpus Loader for regulatory directives and infrastructure compliance statutes."""

from dataclasses import dataclass
import glob
import os
import re
from typing import Any, Dict, List


@dataclass
class DocumentChunk:
    chunk_id: str
    document_name: str
    section_title: str
    text: str
    token_count: int


class RegulatoryCorpusLoader:
    """Loads and chunks compliance statutes from EU CSDDD, SEC ESG, and NERC CIP."""

    def __init__(self, corpus_dir: str = "data/regulatory_corpus"):
        self.corpus_dir = corpus_dir

    def load_documents(self) -> Dict[str, str]:
        """Loads all text files in the corpus directory."""
        files = glob.glob(os.path.join(self.corpus_dir, "*.txt"))
        documents = {}
        for fpath in files:
            doc_name = os.path.basename(fpath)
            with open(fpath, "r", encoding="utf-8") as f:
                documents[doc_name] = f.read()
        return documents

    def chunk_corpus(self, chunk_size: int = 600, overlap: int = 100) -> List[DocumentChunk]:
        """Splits corpus into structured chunks by Article/Section headers or character windows."""
        documents = self.load_documents()
        chunks = []
        chunk_idx = 0

        for doc_name, content in documents.items():
            # Split by major headings (Article, Item, Section)
            sections = re.split(r"\n(?=(?:Article|Item|Section)\s+\d+)", content)

            for sec in sections:
                sec_text = sec.strip()
                if not sec_text:
                    continue

                lines = sec_text.split("\n")
                section_title = lines[0].strip()

                # If section exceeds chunk_size, split by sliding window
                if len(sec_text) <= chunk_size:
                    chunks.append(DocumentChunk(
                        chunk_id=f"chk_{chunk_idx:04d}",
                        document_name=doc_name,
                        section_title=section_title,
                        text=sec_text,
                        token_count=len(sec_text.split())
                    ))
                    chunk_idx += 1
                else:
                    start = 0
                    while start < len(sec_text):
                        end = min(start + chunk_size, len(sec_text))
                        sub_text = sec_text[start:end].strip()
                        if sub_text:
                            chunks.append(DocumentChunk(
                                chunk_id=f"chk_{chunk_idx:04d}",
                                document_name=doc_name,
                                section_title=f"{section_title} (part)",
                                text=sub_text,
                                token_count=len(sub_text.split())
                            ))
                            chunk_idx += 1
                        start += (chunk_size - overlap)

        return chunks
