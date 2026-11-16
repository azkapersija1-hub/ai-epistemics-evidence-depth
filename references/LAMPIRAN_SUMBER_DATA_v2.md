# Appendix: Source of the claim data, version 2 (bibliographic metadata)

This version adds bibliographic metadata for the 36 source articles, taken from the internal catalog (sheet "Katalog Lengkap"). It supersedes the statement in LAMPIRAN_SUMBER_DATA.md that author, year, and journal fields were unavailable for these articles. The per-article table is provided in artikel_asal_36_klaim_lengkap.csv. The claim-pool description in version 1 is unchanged.

## Summary of metadata for the 36 source articles

| Item | Value |
|---|---|
| Source articles | 36 (one claim per article) |
| Matching method | DOI match for all 36 (11 also matched on normalized title) |
| Articles not found in the catalog | 0 |
| Ambiguous matches (more than one catalog row) | 0 |
| Metadata status: LENGKAP (author, title, year, and venue all present) | 1 |
| Metadata status: SEBAGIAN (at least one of these fields empty) | 35 |
| Metadata status: TIDAK_DITEMUKAN | 0 |
| Publication year range | 2016 to 2026 |
| Articles per year | 2016: 1; 2020: 2; 2022: 4; 2023: 9; 2024: 8; 2025: 11; 2026: 1 |
| Language, catalog label: Indonesian | 19 |
| Language, catalog label: English | 17 |
| Language, catalog label: unknown | 0 |
| Document type | Not recorded in the catalog; not reported |
| Field: venue (journal) filled | 1 of 36 |
| Field: author filled | 35 of 36 |
| Field: volume filled | 31 of 36 |
| Field: issue filled | 28 of 36 |
| Field: page range | Not available as a catalog column |

Note on language labels: the language label in the working pool differs from the catalog label for 8 of the 36 articles (pool: 16 Indonesian, 14 English, 6 unknown). The catalog label is the one recorded in the metadata table; the pool label is kept in the claim data.

## Limitations

- DOI and bibliographic metadata come from the internal catalog. They have not been re-verified against publishers.
- Many catalog fields are sparse. The journal (venue) field is empty for 35 of 36 articles, so the metadata status is partial for almost all articles.
- Some catalog title values contain journal names, page headers, or citation strings rather than article titles. They are flagged in the log and were not corrected.
- These limits apply to the completeness of the metadata. They do not change the claim set.
