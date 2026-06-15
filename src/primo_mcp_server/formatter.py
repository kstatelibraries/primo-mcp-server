"""Format Primo records into WCAG 2.2-friendly Markdown unordered lists."""
from __future__ import annotations

from primo_mcp_server.models import PrimoRecord
from primo_mcp_server.models import SearchResponse

# Appended to tool output so the consuming LLM relays the structure as-is.
# Placing the instruction adjacent to the results is far more reliable than
# a system prompt, especially for small local models.
PRESENTATION_HINT = (
    '---\n'
    'PRESENTATION RULES: Present the results above to the user as Markdown '
    'unordered lists, preserving the exact field structure (Author(s), Year, '
    'Title, Source/Publisher, Availability, Record ID). Do NOT reformat them '
    'into a table. Do NOT guess missing values; keep "N/A" as-is. This '
    'structure is required for WCAG 2.2 accessibility.'
)


def _normalize_record_id(record_id: str) -> str:
    """Strip source system prefix from record ID for display and API use.

    For Alma records, removes the 'alma' prefix.
    For CDI records, keeps the full ID.

    Examples:
        'alma9933212933402401' -> '9933212933402401'
        'cdi_proquest_ebookcentral_EBC6170646' -> 'cdi_proquest_ebookcentral_EBC6170646'
    """
    # Remove common Alma prefix
    if record_id.startswith('alma'):
        return record_id[4:]

    # Keep CDI and other prefixes as-is for display
    return record_id


def _format_authors(creators: list[str], max_authors: int = 3) -> str:
    """Format an author list, truncating with 'et al.' if needed."""
    if not creators:
        return 'Unknown author'
    if len(creators) <= max_authors:
        return '; '.join(creators)
    return '; '.join(creators[:max_authors]) + ' et al.'


def _format_identifiers(record: PrimoRecord) -> str:
    """Format the most useful identifier for a record."""
    parts = []
    if record.doi:
        parts.append(f'DOI: {record.doi}')
    if record.isbn:
        parts.append(f'ISBN: {record.isbn[0]}')
    if record.issn:
        parts.append(f'ISSN: {record.issn[0]}')
    return ' | '.join(parts) if parts else ''


def _format_availability(record: PrimoRecord) -> str:
    """Format availability information; 'N/A' when nothing is known (never guess)."""
    parts = []
    if record.fulltext_available:
        parts.append('Full text available')
    if record.delivery_category:
        parts.append(record.delivery_category)
    return ' | '.join(parts) if parts else 'N/A'


def _format_source(record: PrimoRecord) -> str:
    """Format the journal or publisher as the Source/Publisher field."""
    if record.journal_title:
        source = record.journal_title
        if record.volume:
            source += f', {record.volume}'
        if record.issue:
            source += f'({record.issue})'
        if record.start_page:
            source += f', pp. {record.start_page}'
            if record.end_page:
                source += f'-{record.end_page}'
        return source
    if record.publisher:
        return record.publisher
    return 'N/A'


def format_search_results(response: SearchResponse, query: str, offset: int = 0) -> str:
    """Format search results as a WCAG 2.2-accessible Markdown unordered list.

    Each result is a top-level bullet (the title) with the required fields
    nested beneath it: Author(s), Year, Title, Source/Publisher, Availability,
    and Record ID. Missing values are 'N/A' rather than guessed.
    """
    if not response.records:
        return (
            f'No results found for "{query}".\n\n'
            'Suggestions:\n'
            '- Broaden your search terms\n'
            '- Check spelling\n'
            '- Try a different search field (title, creator, subject)\n'
            '- Remove filters (resource type, date range)'
        )

    total = f'{response.info.total:,}'
    showing_start = offset + 1
    showing_end = offset + len(response.records)

    lines = [
        f'Found {total} results for "{query}" (showing {showing_start}-{showing_end})',
        '',
    ]

    for record in response.records:
        type_badge = record.resource_type.replace('_', ' ').title() if record.resource_type else 'N/A'
        year = record.creation_date[:4] if record.creation_date else 'N/A'

        status_parts = []
        if record.peer_reviewed:
            status_parts.append('Peer-reviewed')
        status_parts.append(_format_availability(record))

        lines.append(f'- **{record.title}**')
        lines.append(f'  - **Author(s):** {_format_authors(record.creators)}')
        lines.append(f'  - **Year:** {year}')
        lines.append(f'  - **Type:** {type_badge}')
        lines.append(f'  - **Source/Publisher:** {_format_source(record)}')

        ident = _format_identifiers(record)
        if ident:
            lines.append(f'  - **Identifiers:** {ident}')

        lines.append(f"  - **Availability:** {' | '.join(status_parts)}")
        lines.append(f'  - **Record ID:** {_normalize_record_id(record.record_id)}')
        lines.append('')

    lines.append(PRESENTATION_HINT)
    return '\n'.join(lines).rstrip()


def format_record_detail(record: PrimoRecord) -> str:
    """Format a single record's full details as an accessible unordered list."""
    year = record.creation_date[:4] if record.creation_date else 'N/A'
    type_badge = record.resource_type.replace('_', ' ').title() if record.resource_type else 'N/A'

    lines = [
        f'- **Title:** {record.title}',
        f'- **Author(s):** {_format_authors(record.creators, max_authors=10)}',
    ]

    if record.contributors:
        lines.append(f"- **Contributor(s):** {'; '.join(record.contributors)}")

    lines.append(f'- **Year:** {year}')
    lines.append(f'- **Type:** {type_badge}')
    lines.append(f'- **Source/Publisher:** {_format_source(record)}')

    if record.language:
        lines.append(f'- **Language:** {record.language}')

    # Identifiers
    if record.doi:
        lines.append(f'- **DOI:** {record.doi}')
    if record.isbn:
        lines.append(f"- **ISBN:** {', '.join(record.isbn)}")
    if record.issn:
        lines.append(f"- **ISSN:** {', '.join(record.issn)}")

    if record.subjects:
        lines.append(f"- **Subjects:** {'; '.join(record.subjects)}")
    if record.keywords:
        lines.append(f"- **Keywords:** {'; '.join(record.keywords)}")

    lines.append(f"- **Peer-reviewed:** {'Yes' if record.peer_reviewed else 'No'}")

    if record.description:
        # Truncate long descriptions
        desc = record.description
        if len(desc) > 500:
            desc = desc[:497] + '...'
        lines.append(f'- **Description:** {desc}')

    lines.append(f'- **Availability:** {_format_availability(record)}')
    if record.source_label:
        lines.append(f'- **Source:** {record.source_label}')

    lines.append(f'- **Record ID:** {_normalize_record_id(record.record_id)}')

    lines.append('')
    lines.append(PRESENTATION_HINT)
    return '\n'.join(lines)


def format_suggestions(suggestions: list[str], query: str) -> str:
    """Format autocomplete suggestions."""
    if not suggestions:
        return f'No suggestions found for "{query}".'

    lines = [f'Suggestions for "{query}":', '']
    for s in suggestions:
        lines.append(f'  - {s}')
    return '\n'.join(lines)
