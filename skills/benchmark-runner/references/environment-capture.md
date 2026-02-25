# Environment Capture

What hardware, software, and configuration context to record for reproducible
benchmark results.

---

## Hardware Context

### Required Fields

| Field | How to Capture | Example |
|-------|---------------|---------|
| CPU model | `lscpu | grep "Model name"` or `sysctl -n machdep.cpu.brand_string` | Apple M2 Pro, Intel i9-13900K |
| CPU cores | `nproc` or `sysctl -n hw.ncpu` | 12 cores (8P + 4E) |
| RAM | `free -h` or `sysctl -n hw.memsize` | 32 GB |
| GPU | `nvidia-smi` or system profiler | NVIDIA A100 40GB |
| Storage | `lsblk` or disk utility | NVMe SSD, 1TB |

### Optional Fields (for rigorous benchmarks)

| Field | How to Capture |
|-------|---------------|
| CPU frequency | `lscpu | grep MHz` |
| CPU cache sizes | `lscpu | grep cache` |
| NUMA topology | `numactl --hardware` |
| Thermal state | `sensors` or CPU temp monitor |

### macOS Capture Script

```bash
echo "CPU: $(sysctl -n machdep.cpu.brand_string)"
echo "Cores: $(sysctl -n hw.ncpu)"
echo "RAM: $(( $(sysctl -n hw.memsize) / 1073741824 )) GB"
echo "OS: $(sw_vers -productVersion)"
```

### Linux Capture Script

```bash
echo "CPU: $(lscpu | grep 'Model name' | sed 's/.*: *//')"
echo "Cores: $(nproc)"
echo "RAM: $(free -h | awk '/Mem:/ {print $2}')"
echo "OS: $(uname -r)"
```

---

## Software Context

### Required Fields

| Field | How to Capture | Example |
|-------|---------------|---------|
| OS version | `uname -r` | Darwin 25.3.0, Linux 6.5.0 |
| Language runtime | `python --version`, `node --version` | Python 3.12.1 |
| Package versions | `pip freeze`, `npm list` | numpy==1.26.3 |
| Key dependency versions | Extract from lockfile | PyTorch 2.2.0, CUDA 12.1 |

### Python Environment Capture

```bash
python --version
pip freeze > benchmark_requirements.txt
echo "Virtual env: $VIRTUAL_ENV"
```

### Node.js Environment Capture

```bash
node --version
npm --version
npm list --depth=0 > benchmark_packages.txt
```

---

## Configuration Context

### Application-Level Configuration

Document any settings that affect performance:

| Setting Type | Examples |
|-------------|---------|
| Thread count | `WORKERS=4`, `OMP_NUM_THREADS=8` |
| Batch size | `BATCH_SIZE=32` |
| Cache settings | `CACHE_SIZE=1GB`, `CACHE_ENABLED=true` |
| Connection pool | `MAX_CONNECTIONS=100` |
| Memory limits | `JAVA_OPTS=-Xmx4g` |
| Optimization flags | `-O2`, `--release`, `NODE_ENV=production` |

### Database Configuration (if applicable)

| Setting | Impact |
|---------|--------|
| `shared_buffers` | Query cache size |
| `work_mem` | Sort/hash operation memory |
| `max_connections` | Connection pool size |
| `effective_cache_size` | Query planner behavior |

---

## Reproducibility Checklist

### Minimum Reproducibility

- [ ] All hardware fields documented
- [ ] All software versions captured
- [ ] Configuration settings recorded
- [ ] Input data described (or provided)
- [ ] Warmup iterations specified
- [ ] Measurement iterations specified
- [ ] Commands to run the benchmark documented

### Full Reproducibility

- [ ] Docker/container image provided
- [ ] Input data included (or script to generate it)
- [ ] Random seeds fixed
- [ ] Environment variables documented
- [ ] Background process state noted
- [ ] Time of day noted (for cloud benchmarks)

---

## Reporting Template

Include this block at the top of benchmark results:

```markdown
## Environment

| Component | Value |
|-----------|-------|
| CPU | {model, cores} |
| RAM | {size} |
| GPU | {model} (if applicable) |
| OS | {name, version} |
| Runtime | {language, version} |
| Key deps | {package versions} |

### Configuration
| Setting | Value |
|---------|-------|
| Threads | {N} |
| Batch size | {N} |
| {other relevant settings} | {values} |

### Benchmark Parameters
| Parameter | Value |
|-----------|-------|
| Warmup iterations | {N} |
| Measurement iterations | {N} |
| Input sizes | {list} |
```
