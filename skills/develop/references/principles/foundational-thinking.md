# Foundational Thinking

Apply before writing logic: choosing core types and data structures, sequencing scaffold-before-feature work, and asking what concurrent actors share.

- Get the data shape right before writing logic. Define core types early, trace every access pattern, and pick structures that match the dominant paths. DRY the structure, not every line.
- Before sharing state between actors, ask what happens if another actor modifies it concurrently. If the answer is not "nothing", isolate first.
- Scaffold first. Whatever supports every later phase (shared types, schemas, tests, CI checks) lands first, right after removing dead code. Keep commits small and single-purpose.
