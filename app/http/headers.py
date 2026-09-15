from dataclasses import dataclass, field

from .constants import CRLF


@dataclass
class Headers:
    entries: list[tuple[str, str]] = field(default_factory=list)

    @classmethod
    def parse(cls, raw_block: str) -> Headers:
        header_lines = raw_block.lstrip().split(CRLF)
        if not header_lines:
            return cls()

        headers = cls()
        for line in header_lines:
            if not line:
                continue
            key, value = line.split(": ", maxsplit=1)
            headers.add_header(key, value)
        return headers

    def get_header(self, key: str) -> str:
        for current_key, value in self.entries:
            if key == current_key:
                return value
        return ""

    def add_header(self, key: str, value: str) -> None:
        self.entries.append((key, value))

    def __str__(self) -> str:
        lines = (f"{key}: {value}" for key, value in self.entries)
        return f"{CRLF.join(lines)}{CRLF}"
