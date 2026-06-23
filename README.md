# bintropy


---

# Binary Entropy Scanner

A lightweight static analysis tool designed to calculate and map the **Shannon Entropy** of binary files using a sliding window approach. This script helps reverse engineers and security researchers quickly identify packed, compressed, or encrypted payloads within executable files without executing them.

---

## Theoretical Overview

In information theory, **Shannon Entropy** quantifies the amount of randomness or unpredictability within a dataset. For a binary file, if we treat individual byte values ($0$ to $255$) as discrete events, the entropy $H$ of a given block of data is defined mathematically as:

$$H = -\sum_{i=1}^{n} p_i \log_2(p_i)$$

Where $p_i$ is the probability of the byte value $i$ occurring within that block.

* **Structured Data (Native Code/Text):** Contains repetitive opcodes, null padding, and standard string constants. This yields low entropy, typically ranging between **4.5 and 6.0**.
* **Random Data (Packed/Encrypted Payloads):** Destroys predictable byte patterns, resulting in a uniform distribution where every byte value occurs with near-equal frequency. This drives the entropy score up toward its theoretical maximum of **8.0**.

---

## Features

* **Sliding Window Analysis:** Processes files in configurable block sizes (default: 1024 bytes) to retain localized structural fidelity.
* **Fast Execution:** Uses vectorised `numpy` array operations for high-speed byte frequency computation.
* **Cyberpunk Visual Dashboard:** Generates high-contrast, dark-themed charts plotting entropy spikes against file offsets.
* **Suspicious Threshold Mapping:** Visually highlights sections exceeding an entropy score of `7.2` (the standard benchmark for obfuscation).

---

## Requirements

Ensure you have Python 3 installed along with the following dependencies:

```bash
pip install numpy matplotlib

```

---

## Usage

Run the script from your terminal by passing the path to the target binary as an argument:

```bash
python entropy_scanner.py <path_to_binary_file>

```

### Example Commands

Analyzing a standard Linux system binary:

```bash
python entropy_scanner.py /usr/bin/ls

```

Analyzing a suspicious sample or archived payload:

```bash
python entropy_scanner.py suspicious_sample.exe

```

---

## Important Limitation: The Image False-Positive Caveat

When triaging binaries, this tool can yield **false positives** by flagging entirely benign applications as highly suspicious. This most frequently occurs when a file contains embedded graphics, icons, or high-resolution images.

### The Technical Reason

1. **Lossy and Lossless Compression:** Modern image formats (such as `.png`, `.jpeg`, or `.gif`) rely heavily on compression algorithms like DEFLATE or Huffman coding to minimize file size. Compression functions explicitly by removing redundant patterns and maximizing information density per byte.
2. **Uniform Distribution:** From an information-theoretic standpoint, perfectly compressed data is indistinguishable from encrypted data or raw cryptographic keys. The frequency distribution of byte values becomes flat and uniform.
3. **High Entropy Signature:** Because the scanner analyzes raw byte frequencies without parsing the file format's structural layout, an embedded asset folder containing complex UI graphics or large images will generate a sustained entropy plateau between **7.5 and 8.0**.

> **Analysis Tip:** When evaluating an unknown binary that throws a high-entropy alert, cross-reference the offset locations with a PE/ELF parser (like `pefile` or `readelf`) to check if the high-entropy block maps to a standard resource section (like `.rsrc`) rather than code execution sections (like `.text`).

---

### On system binaries (/bin/cat): As expected below threshold
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fb0d0d9d-a0e2-4f77-8e5e-0523650713cc" />

### On compressed files (jpg) : Above threshold due to compressed data
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/19340d01-c1f2-420c-8078-096d6ee981cd" />
