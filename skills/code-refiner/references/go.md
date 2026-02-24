# Go Refinement Patterns

## Table of Contents
1. [Error Handling](#error-handling)
2. [Structural Patterns](#structural-patterns)
3. [Interface Design](#interface-design)
4. [Concurrency](#concurrency)
5. [Anti-Patterns](#anti-patterns)

---

## Error Handling

### Wrap Errors with Context
```go
// Before
if err != nil {
    return err
}

// After — adds context for debugging
if err != nil {
    return fmt.Errorf("parsing config %s: %w", path, err)
}
```

### Sentinel Errors for Expected Conditions
```go
var ErrNotFound = errors.New("record not found")

// Callers check with errors.Is:
if errors.Is(err, ErrNotFound) { ... }
```

### Error Type Assertion
```go
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    log.Printf("failed path: %s", pathErr.Path)
}
```

### Don't Log and Return
Either log the error (if you're the handler) or return it (if you're a library).
Never both — it creates duplicate noise.

---

## Structural Patterns

### Table-Driven Tests
Replace repetitive test functions with a test table:
```go
tests := []struct {
    name     string
    input    string
    expected int
    wantErr  bool
}{
    {"empty", "", 0, true},
    {"valid", "42", 42, false},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Parse(tt.input)
        if (err != nil) != tt.wantErr {
            t.Errorf("unexpected error: %v", err)
        }
        if got != tt.expected {
            t.Errorf("got %d, want %d", got, tt.expected)
        }
    })
}
```

### Functional Options
Replace large config structs with functional options for optional configuration:
```go
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080} // sensible defaults
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Guard Clauses
Same principle as other languages — exit early, keep the happy path at the lowest indent:
```go
func (s *Service) Process(ctx context.Context, req *Request) error {
    if req == nil {
        return errors.New("nil request")
    }
    if err := req.Validate(); err != nil {
        return fmt.Errorf("invalid request: %w", err)
    }
    // Happy path at indent level 1
    return s.store.Save(ctx, req)
}
```

---

## Interface Design

### Accept Interfaces, Return Structs
Functions should accept the narrowest interface they need and return concrete types.

### Small Interfaces
Prefer 1-2 method interfaces. Compose larger behaviors from small interfaces.
```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type ReadWriter interface { Reader; Writer }
```

### Define Interfaces at the Consumer
The package that *uses* the interface should define it, not the package that implements it.
This keeps dependencies flowing in one direction.

---

## Concurrency

### Use `errgroup` for Parallel Work with Error Collection
```go
g, ctx := errgroup.WithContext(ctx)
for _, url := range urls {
    g.Go(func() error {
        return fetch(ctx, url)
    })
}
if err := g.Wait(); err != nil {
    return err
}
```

### Don't Start Goroutines in Library Code Without Lifecycle Control
If you must, accept a context and/or return a cleanup function.

### Channel Direction Annotations
```go
func producer(ch chan<- int) { ... }  // send only
func consumer(ch <-chan int) { ... }  // receive only
```

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `init()` with side effects | Move to explicit initialization function |
| Package-level `var` for mutable state | Pass dependencies explicitly |
| `interface{}` / `any` when concrete type is known | Use the concrete type or a constrained generic |
| Panicking in library code | Return errors |
| Ignoring errors with `_` | Handle or wrap. If truly ignorable, add a comment explaining why |
| `sync.Mutex` protecting a single field | Consider `atomic` types |
| Channels for simple mutual exclusion | Use `sync.Mutex` |
| Deeply nested `if err != nil` chains | Extract into helper functions with named returns |
