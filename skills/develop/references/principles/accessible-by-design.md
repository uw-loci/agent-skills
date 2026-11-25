# Accessible by Design

Apply when designing user-facing commands, GUIs, CLIs, parameters, error messages, installation paths, or public APIs and docs.

Our users are primarily bench scientists, microscopists, pathologists, and research engineers — not just software developers. Ease of access and user experience are core requirements, not afterthoughts.

- **Respect how scientists actually enter the tool.** Interactive GUIs (Fiji, QuPath, napari) are primary access points for many users, while CLIs and Python/Java APIs serve scripted and batch workflows. Design clean, intuitive entry points for the target surface rather than treating UI or ergonomics as throwaway glue.
- **Clear defaults, names, and units.** Choose sensible defaults, self-explanatory parameter labels, explicit physical/array units and axis conventions, and macro/script recordability where the host platform supports it.
- **Actionable errors.** Return plain-language error messages stating what failed, why, and what the user can do next. Never surface a raw stack trace or opaque internal code as the only feedback.
- **Low-friction distribution & docs.** Deliver through standard community channels (Fiji update sites, Maven/SciJava, PyPI/`uv`, conda-forge) rather than fragile manual build steps. Keep public API Javadoc/docstrings clear and complete.
- **Extensibility over one-offs.** Prefer modular libraries, plugins, and reusable ops that other labs can build on over monolithic single-study scripts.
