# License Compatibility

License classification, compatibility matrix, and copyleft detection for dependency auditing.

---

## License Categories

### Permissive Licenses

Allow use in proprietary software with minimal obligations.

| License      | SPDX ID      | Key Obligation                              | Commercial Safe |
| ------------ | ------------ | ------------------------------------------- | --------------- |
| MIT          | MIT          | Include copyright notice                    | Yes             |
| BSD 2-Clause | BSD-2-Clause | Include copyright notice                    | Yes             |
| BSD 3-Clause | BSD-3-Clause | Include notice, no endorsement clause       | Yes             |
| ISC          | ISC          | Include copyright notice                    | Yes             |
| Apache 2.0   | Apache-2.0   | Include notice, state changes, patent grant | Yes             |
| Unlicense    | Unlicense    | None                                        | Yes             |
| CC0 1.0      | CC0-1.0      | None                                        | Yes             |
| 0BSD         | 0BSD         | None                                        | Yes             |
| Zlib         | Zlib         | Mark altered versions                       | Yes             |

### Weak Copyleft Licenses

Copyleft applies to the library itself, not to code that links against it.

| License  | SPDX ID       | Key Obligation                                               | Commercial Safe |
| -------- | ------------- | ------------------------------------------------------------ | --------------- |
| LGPL 2.1 | LGPL-2.1-only | Modifications to library must be open-sourced; linking is OK | With care       |
| LGPL 3.0 | LGPL-3.0-only | Same as LGPL 2.1 + tivoization clause                        | With care       |
| MPL 2.0  | MPL-2.0       | Modified files must be open-sourced (file-level copyleft)    | With care       |
| EPL 2.0  | EPL-2.0       | Modifications must be open-sourced                           | With care       |
| CDDL 1.0 | CDDL-1.0      | Modified files must be open-sourced                          | With care       |

### Strong Copyleft Licenses

Copyleft extends to all linked/combined code. Using a GPL library in a proprietary
project makes the entire project subject to GPL.

| License  | SPDX ID       | Key Obligation                                      | Commercial Safe |
| -------- | ------------- | --------------------------------------------------- | --------------- |
| GPL 2.0  | GPL-2.0-only  | Entire combined work must be GPL                    | No              |
| GPL 3.0  | GPL-3.0-only  | Entire combined work must be GPL + anti-tivoization | No              |
| AGPL 3.0 | AGPL-3.0-only | GPL + network use triggers disclosure               | No              |
| SSPL     | SSPL-1.0      | Service code must be open-sourced                   | No              |
| EUPL 1.2 | EUPL-1.2      | Copyleft with broad compatibility list              | No              |

### Non-Open / Restrictive

| License             | SPDX ID      | Issue                                                  |
| ------------------- | ------------ | ------------------------------------------------------ |
| BSL 1.1             | BSL-1.1      | Time-delayed open source; restricted until change date |
| Elastic License 2.0 | Elastic-2.0  | Cannot provide as managed service                      |
| Commons Clause      | N/A          | Restricts selling the software                         |
| CC-BY-NC            | CC-BY-NC-4.0 | Non-commercial use only                                |
| Proprietary         | N/A          | Must review terms individually                         |

---

## Compatibility Matrix

### Project License → Dependency License Compatibility

Can I use a dependency with license X in a project with license Y?

| Dependency ↓ / Project → | MIT   | Apache 2.0 | LGPL 3.0 | GPL 3.0     | AGPL 3.0 | Proprietary     |
| ------------------------ | ----- | ---------- | -------- | ----------- | -------- | --------------- |
| MIT                      | Yes   | Yes        | Yes      | Yes         | Yes      | Yes             |
| BSD 2/3                  | Yes   | Yes        | Yes      | Yes         | Yes      | Yes             |
| Apache 2.0               | Yes\* | Yes        | Yes      | Yes         | Yes      | Yes             |
| LGPL 2.1                 | No    | No         | Yes      | Yes         | Yes      | With care\*\*   |
| LGPL 3.0                 | No    | No         | Yes      | Yes         | Yes      | With care\*\*   |
| MPL 2.0                  | No    | No         | Yes      | Yes         | Yes      | With care\*\*\* |
| GPL 2.0                  | No    | No         | No       | Yes\*\*\*\* | No       | No              |
| GPL 3.0                  | No    | No         | No       | Yes         | Yes      | No              |
| AGPL 3.0                 | No    | No         | No       | No          | Yes      | No              |

\* Apache 2.0 has patent grant — compatible with MIT but MIT doesn't reciprocate patent protection.
\*\* LGPL allows dynamic linking without copyleft. Python imports are generally considered dynamic linking. \*** MPL 2.0 is file-level copyleft — only modified MPL files need to stay MPL.
\*\*** GPL 2.0 is not compatible with GPL 3.0 unless "or later" clause is present.

---

## Detecting License Issues

### Where to Find License Information

Priority order for identifying a package's license:

1. **Package metadata** — `pip show <pkg>`, `npm info <pkg> license`, `cargo info <pkg>`
2. **Lock file / registry** — PyPI JSON API, npmjs.com, crates.io
3. **LICENSE / COPYING file** — In the package's repository root
4. **SPDX header** — In individual source files
5. **README** — Sometimes mentions license (least reliable)

### Common Detection Problems

| Problem                   | Example                                  | Resolution                        |
| ------------------------- | ---------------------------------------- | --------------------------------- |
| Missing license metadata  | PyPI shows "UNKNOWN"                     | Check repository for LICENSE file |
| License mismatch          | Metadata says MIT, LICENSE file says GPL | LICENSE file takes precedence     |
| Dual licensing            | "MIT OR Apache-2.0"                      | Choose the more permissive one    |
| Custom license            | Non-standard license text                | Legal review required             |
| "License" field is a URL  | Points to custom terms                   | Fetch and read the terms          |
| Version-dependent license | Changed from MIT to BSL in v2.0          | Check the specific version in use |

### SPDX Expression Parsing

Dependencies may declare compound licenses:

```text
MIT                          → Single license
MIT OR Apache-2.0            → Choice (use either)
MIT AND BSD-3-Clause         → Both apply (must comply with both)
GPL-2.0-only WITH Classpath  → License with exception
(MIT OR Apache-2.0) AND BSD  → Complex expression
```

Rules:

- `OR` → Take the more favorable option
- `AND` → Must satisfy both
- `WITH` → Exception relaxes the base license

---

## Copyleft Detection Checklist

### Strong Copyleft Indicators

Flag any dependency matching:

- [ ] License contains "GNU General Public License" (GPL)
- [ ] License contains "Affero" (AGPL)
- [ ] License contains "Server Side Public License" (SSPL)
- [ ] SPDX ID starts with `GPL-` or `AGPL-`
- [ ] License requires "derivative works" to use same license
- [ ] License requires source disclosure for "network use"

### Weak Copyleft Indicators

Investigate further:

- [ ] License contains "Lesser General Public License" (LGPL)
- [ ] License contains "Mozilla Public License" (MPL)
- [ ] License contains "Eclipse Public License" (EPL)
- [ ] SPDX ID starts with `LGPL-`, `MPL-`, or `EPL-`

### Transitive Copyleft Risk

A project's effective license is determined by its most restrictive dependency:

```text
Your project (MIT)
├── lib-a (MIT)          → OK
├── lib-b (Apache 2.0)   → OK
│   └── lib-d (MIT)      → OK
└── lib-c (BSD-3)        → OK
    └── lib-e (GPL-3.0)  → PROBLEM: Makes entire project GPL-3.0
```

Even though `lib-e` is a transitive dependency, its GPL license "infects" up through
`lib-c` to the project.

---

## Language-Specific License Tools

| Language | Tool            | Command                              |
| -------- | --------------- | ------------------------------------ |
| Python   | pip-licenses    | `uv run pip-licenses --format=table` |
| Python   | piplicenses     | `uv run piplicenses --with-system`   |
| Node.js  | license-checker | `npx license-checker --summary`      |
| Node.js  | license-report  | `npx license-report`                 |
| Rust     | cargo-license   | `cargo license`                      |
| Go       | go-licenses     | `go-licenses check .`                |

---

## Common Ecosystem License Patterns

### Python (PyPI)

Most popular Python packages use permissive licenses:

- MIT: requests, flask, django, fastapi, pytest
- Apache 2.0: tensorflow, google-cloud-\*, boto3
- BSD: numpy, scipy, pandas, scikit-learn
- PSF: Python standard library extensions

Watch for:

- GPL: some scientific/academic packages (e.g., MySQL connector)
- LGPL: PyQt (LGPL or commercial), some GNU tools

### Node.js (npm)

npm ecosystem is predominantly permissive:

- MIT: express, react, lodash, axios
- Apache 2.0: angular, firebase
- ISC: many small utilities

Watch for:

- Packages with no license field (surprisingly common in npm)
- License changes on major versions
- "Artistic License" variants

### Rust (crates.io)

Rust ecosystem strongly favors dual licensing:

- "MIT OR Apache-2.0": most Rust packages
- Apache 2.0: some corporate packages
- MIT: standalone

Watch for:

- GPL crates (uncommon but exist)
- "license-file" pointing to custom text
