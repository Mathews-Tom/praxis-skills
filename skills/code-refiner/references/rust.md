# Rust Refinement Patterns

## Table of Contents
1. [Error Handling](#error-handling)
2. [Iterator Patterns](#iterator-patterns)
3. [Ownership and Borrowing](#ownership-and-borrowing)
4. [Type Design](#type-design)
5. [Anti-Patterns](#anti-patterns)

---

## Error Handling

### `?` Operator over Match Chains
```rust
// Before
fn read_config(path: &str) -> Result<Config, Error> {
    let file = match File::open(path) {
        Ok(f) => f,
        Err(e) => return Err(e.into()),
    };
    let contents = match read_to_string(file) {
        Ok(c) => c,
        Err(e) => return Err(e.into()),
    };
    Ok(parse(contents)?)
}

// After
fn read_config(path: &str) -> Result<Config, Error> {
    let contents = std::fs::read_to_string(path)?;
    Ok(parse(&contents)?)
}
```

### Custom Error Types with `thiserror`
```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error("config not found: {path}")]
    ConfigNotFound { path: PathBuf },
    #[error("parse error at line {line}")]
    ParseError { line: usize, #[source] cause: serde_json::Error },
    #[error(transparent)]
    Io(#[from] std::io::Error),
}
```

### `anyhow` for Application Code, `thiserror` for Libraries
Applications use `anyhow::Result` for convenience. Libraries define explicit error types.

---

## Iterator Patterns

### Chain over Manual Loops
```rust
// Before
let mut results = Vec::new();
for item in items {
    if item.is_active() {
        results.push(item.name().to_lowercase());
    }
}

// After
let results: Vec<String> = items.iter()
    .filter(|item| item.is_active())
    .map(|item| item.name().to_lowercase())
    .collect();
```

### `flat_map` for Nested Iteration
```rust
let all_tags: Vec<&str> = posts.iter()
    .flat_map(|post| post.tags.iter())
    .map(|tag| tag.as_str())
    .collect();
```

### `fold` / `reduce` for Accumulation
Prefer `.sum()`, `.product()`, `.min()`, `.max()` when they apply directly.
Use `.fold()` for custom accumulation.

### Avoid `.clone()` in Iterator Chains
If you're cloning inside `.map()`, check if you can restructure to borrow instead.
Sometimes moving the `.collect()` earlier or changing the return type eliminates the need.

---

## Ownership and Borrowing

### Accept `&str` not `String` in Function Parameters
Unless the function needs to own the string:
```rust
fn greet(name: &str) -> String {        // borrows
    format!("Hello, {name}")
}
fn store_name(name: String) { ... }      // takes ownership — caller decides when to clone
```

### `impl Trait` in Argument Position
Prefer `impl AsRef<Path>` over `&Path` for flexibility:
```rust
fn read_file(path: impl AsRef<Path>) -> io::Result<String> {
    std::fs::read_to_string(path)
}
```

### Cow for Conditional Ownership
```rust
fn normalize(input: &str) -> Cow<'_, str> {
    if input.contains(' ') {
        Cow::Owned(input.replace(' ', "_"))
    } else {
        Cow::Borrowed(input)
    }
}
```

---

## Type Design

### Newtype Pattern
Prevent primitive obsession and make the type system work for you:
```rust
struct UserId(u64);
struct OrderId(u64);
// These are distinct types — can't accidentally pass UserId where OrderId expected
```

### Builder Pattern for Complex Construction
When a struct has >3 optional fields, use a builder instead of dozens of `new_with_*` variants.

### `From` / `Into` for Type Conversions
Implement `From<A> for B` to get `Into<B> for A` automatically.
Idiomatic for error type conversion and newtype unwrapping.

### Enum State Machines
Encode valid states as enum variants. Invalid transitions become compile errors:
```rust
enum Connection {
    Disconnected,
    Connecting { attempt: u32 },
    Connected { session: Session },
}
```

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `.unwrap()` in library code | Return `Result` or `Option` |
| `.clone()` to satisfy borrow checker without understanding why | Restructure lifetimes or use `Rc`/`Arc` if shared ownership is needed |
| `String` in struct fields that are always static | Use `&'static str` or `Cow<'static, str>` |
| `Box<dyn Error>` in library error types | Use `thiserror` enum |
| Manual `impl Display` + `impl Error` | Use `thiserror` derive |
| `Arc<Mutex<Vec<T>>>` as default concurrency pattern | Consider channels, `dashmap`, or redesign for less sharing |
| Returning `impl Iterator` when the caller needs to store it | Return a concrete type or `Box<dyn Iterator>` |
