import sys
import os
import numpy as np
import matplotlib.pyplot as plt

def calculate_entropy(data_block):
    """
    Calculates the Shannon entropy of a byte array.
    """
    if not data_block:
        return 0.0
    
    # Fast count of byte frequencies using numpy
    counts = np.bincount(np.frombuffer(data_block, dtype=np.uint8), minlength=256)
    
    # Calculate probabilities of each byte
    probabilities = counts / len(data_block)
    
    # Filter out zero probabilities to avoid log2(0) errors
    non_zero_probs = probabilities[probabilities > 0]
    
    # Shannon entropy formula
    entropy = -np.sum(non_zero_probs * np.log2(non_zero_probs))
    return entropy

def analyze_file(file_path, block_size=1024):
    """
    Reads a file in chunks and calculates entropy for each chunk.
    """
    entropies = []
    offsets = []
    
    try:
        with open(file_path, 'rb') as f:
            offset = 0
            while True:
                block = f.read(block_size)
                if not block:
                    break
                entropies.append(calculate_entropy(block))
                offsets.append(offset)
                offset += block_size
        return offsets, entropies
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

def plot_entropy(offsets, entropies, file_path):
    """
    Plots the entropy graph with a dark/neon aesthetic.
    """
    # Set dark theme for a terminal/cyberpunk feel
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the entropy data (Neon Cyan)
    ax.plot(offsets, entropies, color='#00ffcc', linewidth=1.5, label='Block Entropy')
    
    # Draw a threshold line at 7.2 (Neon Red) indicating compression/encryption
    ax.axhline(y=7.2, color='#ff003c', linestyle='--', linewidth=2, label='Suspicious Threshold (7.2)')
    
    # Highlight areas that exceed the threshold
    ax.fill_between(offsets, entropies, 7.2, where=(np.array(entropies) > 7.2), 
                    color='#ff003c', alpha=0.3, interpolate=True)

    # Formatting
    ax.set_title(f"Entropy Analysis: {os.path.basename(file_path)}", fontsize=14, fontweight='bold')
    ax.set_xlabel("File Offset (Bytes)", fontsize=12)
    ax.set_ylabel("Shannon Entropy (0 - 8)", fontsize=12)
    ax.set_ylim(0, 8.5)
    
    # Grid and legend
    ax.grid(True, color='#333333', linestyle=':')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python entropy_scanner.py <path_to_binary_file>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    
    # 1024 bytes is a standard block size. 
    # Smaller = higher resolution but more noise. Larger = smoother but less precise.
    block_size = 1024 
    
    print(f"Analyzing {target_file} with block size {block_size} bytes...")
    offsets, entropies = analyze_file(target_file, block_size)
    
    print("Analysis complete. Generating graph...")
    plot_entropy(offsets, entropies, target_file)