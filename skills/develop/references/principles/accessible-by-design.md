# Accessible by Design

Apply when designing user-facing commands, GUIs, CLIs, parameters, public APIs, error messages, installation paths, or public docs.

Our users are primarily bench scientists, microscopists, pathologists, and research engineers, in addition to software developers. Ease of access, predictability, and user experience are core requirements, not afterthoughts.

- **Principle of least surprise.** Match host-ecosystem and sibling-API conventions (parameter and axis ordering, units, return shapes, error and exit-code signaling) so commands, flags, defaults, and public APIs do what a newcomer reasonably expects from their names and signatures. Never run surprising destructive, network, or write side effects without explicit opt-in or confirmation.
- **Respect how users actually enter the tool.** Interactive GUIs (Fiji, QuPath, napari) are primary entry points for many scientists, while CLIs and Python or Java APIs serve scripted and batch workflows. Design clean, intuitive entry points for the target interface rather than treating UI or ergonomics as throwaway glue.
- **Clear, stable defaults, names, and units.** Choose sensible defaults, self-explanatory parameter labels, explicit physical or array units and axis conventions, accessible visuals (such as colorblind-safe colormaps and keyboard access where applicable), and macro or script recordability where the host platform supports it. Never silently change default values or units in ways that alter existing scientific results without a clear warning or version boundary.
- **Actionable errors.** Return plain-language error messages stating what failed, why, and what the user can do next. Never show a raw stack trace or opaque internal code as the only feedback.
- **Low-friction distribution and docs.** Deliver through standard community channels (Fiji update sites, Maven/SciJava, PyPI/`uv`, conda-forge) rather than fragile manual build steps. Keep public API Javadoc and docstrings clear and complete.
- **Extensibility over one-offs.** Prefer modular libraries, plugins, and reusable ops that other labs can build on over monolithic single-study scripts.
