You are a senior Python engineer and documentation expert working on the `AudioBookzOrganizer` project. Your tasks are:

---

## 1. 📦 Code Fixes & Enhancements

You are given an existing Python CLI utility that:

- Renames and reorganizes audiobook folders/files
- Extracts metadata (ID3 tags, etc.)
- Optionally uses the Google Books API to enrich metadata
- Provides an interactive Terminal UI (TUI)
- Supports flexible folder/naming schemes and dry-run mode

**You must do the following:**

> ⚠️ In addition to the tasks listed below, you are encouraged to improve **any part of the codebase or CLI experience** as you see fit. Refactor, optimize, simplify, or enhance as long as the result improves usability, reliability, or performance.

### 🔧 Corrections
- Identify and fix any bugs or broken behaviors (e.g., TUI glitches, threading issues, malformed output).
- Ensure proper fallbacks when metadata is missing (e.g., fallback to folder name if title/author is absent).
- Verify all command-line options are correctly parsed and used.

### 🚀 Feature Implementations

Implement the following **advanced features**:

#### 1. **Multi-Part Audiobook Detection**
- Detect folders containing multi-file books (e.g., `Disc 1/2/3`, or >1 file).
- Preserve the full folder in output instead of flattening individual files.
- Treat them as a single logical audiobook during processing.

#### 2. **Metadata Caching**
- Cache Google Books API results to avoid redundant requests (use JSON or SQLite).
- Add `--no-cache` to force re-fetching from the API.

#### 3. **Robust Genre Inference**
- Improve genre detection by scraping or parsing common terms from title/description if not in metadata.
- Fallback to `Unknown` if no valid genre can be inferred.

#### 4. **Optional Tag Editing**
- Add `--write-tags` flag to update audio file metadata based on fetched/cleaned info.
- Support ID3 (MP3) and MP4/M4B tagging with `mutagen`.

#### 5. **Logging & Error Reporting**
- Add `--log /path/to/logfile.txt` to write all rename actions, warnings, and skipped items to disk.
- Include color-coded stderr output in TUI for warnings/errors.

#### 6. **Advanced TUI Enhancements**
- Add support for sorting by filename, status, or author.
- Enable collapsible group views (e.g., collapse books with 100+ files into a single expandable line).
- Implement [J/K] navigation, [Space] to select, and [Enter] to view folder preview (text-based).
- Add a status bar or footer to show number of items, current mode (dry-run/commit), and total runtime.

#### 7. **Performance Benchmarking**
- Add `--benchmark` to print per-book and total processing time.

---

## 2. 📘 README Improvements

Update the `README.md` with the following:

### ✅ GitHub Badges (Top of file):
Add these markdown badges before the main project description:

```markdown
[![CI](https://github.com/itsbryanman/AudioBookzOrganizer/actions/workflows/main.yml/badge.svg)](https://github.com/itsbryanman/AudioBookzOrganizer/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer/branch/main/graph/badge.svg)](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
