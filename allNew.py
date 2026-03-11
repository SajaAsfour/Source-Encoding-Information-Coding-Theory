import math
import heapq
from collections import Counter
import sys
sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------
# Input sequence (remove newlines)
# ---------------------------
sequence = """
ACBAAACDBACABAEACACBABDACAEABACBACADBACABEAACABDACBAC
ACBAABACACDACBAEABACABDACACBAEABACBACDACABEAACBACABDA
CABACBACADBACABEAACABACDACBACABAEABACBACDABACABEAACBA
DACBACABACDACBAEABACBACABDACABEAACBACDACABAEABACBACD
ABACABEAACBACABDACBACAFABACBACDACABAEABACBACABDA
""".replace("\n", "").replace(" ", "")

# ============================================================
# Helpers
# ============================================================

def print_header(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def safe_log2(x: int) -> float:
    return math.log2(x) if x > 0 else 0.0

def remove_empty_last_phrase(phrases):
    if phrases and phrases[-1][1] == "":
        return phrases[:-1]
    return phrases


# ---------------------------
# (c) Entropy
# ---------------------------
def source_entropy(counter: Counter, n: int) -> float:
    H = 0.0
    for sym, cnt in counter.items():
        p = cnt / n
        H -= p * math.log2(p)
    return H

# ---------------------------
# (d) Huffman Coding
# ---------------------------
class HuffNode:
    __slots__ = ("freq", "sym", "left", "right")
    def __init__(self, freq, sym=None, left=None, right=None):
        self.freq = freq
        self.sym = sym
        self.left = left
        self.right = right

    def __lt__(self, other):
        # For heap ordering by frequency
        return self.freq < other.freq

def build_huffman(counter: Counter):
    heap = []
    for sym, freq in counter.items():
        heapq.heappush(heap, HuffNode(freq=freq, sym=sym))

    if len(heap) == 1:
        only = heapq.heappop(heap)
        return HuffNode(freq=only.freq, left=only, right=None)

    step = 1
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merged = HuffNode(freq=a.freq + b.freq, left=a, right=b)
        heapq.heappush(heap, merged)
        print(f"[Huffman merge step {step}] merge ({a.sym},{a.freq}) + ({b.sym},{b.freq}) -> freq={merged.freq}")
        step += 1

    return heap[0]

def extract_codes(root: HuffNode):
    codes = {}

    def dfs(node, path):
        if node is None:
            return
        if node.sym is not None:
            codes[node.sym] = path if path else "0"
            return
        dfs(node.left, path + "0")
        dfs(node.right, path + "1")

    dfs(root, "")
    return codes

def avg_code_length(counter: Counter, codes: dict, n: int) -> float:
    L = 0.0
    for sym, cnt in counter.items():
        p = cnt / n
        L += p * len(codes[sym])
    return L

def total_bits_huffman(sequence: str, codes: dict) -> int:
    return sum(len(codes[ch]) for ch in sequence)

# ---------------------------
# (g) LZ78 Encoding (index, next_char)
# ---------------------------
def lz78_encode(data: str):
    dictionary = {"": 0}  
    dict_size = 1
    result = []
    current = ""

    step = 1
    for ch in data:
        combined = current + ch
        if combined in dictionary:
            current = combined
        else:
            result.append((dictionary[current], ch))
            dictionary[combined] = dict_size
            print(f"[LZ78 step {step}] New phrase '{combined}' -> index {dict_size}. Output ({dictionary[current]}, '{ch}')")
            dict_size += 1
            current = ""
            step += 1

    if current:
        result.append((dictionary[current], ""))
        print(f"[LZ78 final] leftover phrase '{current}' -> Output ({dictionary[current]}, '')")

    return result, dictionary

def lz78_bits_dynamic(phrases, alphabet_bits: int):
    """
    Dynamic index bits: for each phrase i, index bits = ceil(log2(dict_size_so_far)).
    dict_size_so_far starts at 1 (only "" entry), then increments after each new phrase.
    """
    total = 0
    dict_size_so_far = 1
    breakdown = []

    for i, (idx, ch) in enumerate(phrases, start=1):
        idx_bits = max(1, math.ceil(safe_log2(dict_size_so_far)))
        ch_bits = 0 if ch == "" else alphabet_bits
        bits = idx_bits + ch_bits
        breakdown.append((i, dict_size_so_far, idx, ch, idx_bits, ch_bits, bits))
        total += bits
        dict_size_so_far += 1

    return total, breakdown

def lz78_bits_fixed_final(phrases, alphabet_bits: int, final_dict_size: int):
    """
    Fixed index bits using final dictionary size:
    index bits = ceil(log2(final_dict_size))
    """
    idx_bits = max(1, math.ceil(safe_log2(final_dict_size)))
    total = 0
    breakdown = []
    for i, (idx, ch) in enumerate(phrases, start=1):
        ch_bits = 0 if ch == "" else alphabet_bits
        bits = idx_bits + ch_bits
        breakdown.append((i, idx, ch, idx_bits, ch_bits, bits))
        total += bits
    return total, idx_bits, breakdown


# ============================================================
# Main
# ============================================================

print_header("Sequence Info")
print("Sequence:", sequence)
print("Length (characters):", len(sequence))

counter = Counter(sequence)
symbols = sorted(counter.keys())
n = len(sequence)

print("\nSymbol counts:")
for s in symbols:
    print(f"  {s}: {counter[s]}")
print("Unique symbols:", symbols)
print("Number of unique symbols:", len(symbols))

# ---------------------------
# (a) ASCII bits
# ---------------------------
print_header("(a) Bits needed using ASCII")
ascii_bits_per_char = 8
ascii_total_bits = n * ascii_bits_per_char
print(f"ASCII uses {ascii_bits_per_char} bits/character.")
print(f"Total bits = length * 8 = {n} * 8 = {ascii_total_bits} bits")

# ---------------------------
# (b) Fixed length bits
# ---------------------------
print_header("(b) Bits needed using Fixed-Length encoding")
k = len(symbols)
fixed_bits_per_char = math.ceil(safe_log2(k))
fixed_total_bits = n * fixed_bits_per_char

print(f"Number of symbols k = {k}")
print(f"Bits/character = ceil(log2(k)) = ceil(log2({k})) = {fixed_bits_per_char}")
print(f"Total bits = n * bits/char = {n} * {fixed_bits_per_char} = {fixed_total_bits} bits")

# ---------------------------
# (c) Entropy
# ---------------------------
print_header("(c) Source Entropy (bits/character)")
H = source_entropy(counter, n)
print("Probabilities:")
for s in symbols:
    p = counter[s] / n
    print(f"  P({s}) = {counter[s]}/{n} = {p:.6f}")

print(f"\nEntropy H = -Σ p(x) log2 p(x) = {H:.6f} bits/character")

# ---------------------------
# (d) Huffman codes
# ---------------------------
print_header("(d) Huffman codes for the characters")
print("Building Huffman tree (merge steps):")
root = build_huffman(counter)

codes = extract_codes(root)
print("\nHuffman codes:")
for s in symbols:
    print(f"  {s}: {codes[s]}  (length={len(codes[s])})")

# ---------------------------
# (e) Huffman efficiency relative to entropy
# ---------------------------
print_header("(e) Efficiency of Huffman relative to entropy")
L_avg = avg_code_length(counter, codes, n)
eff = H / L_avg if L_avg > 0 else 0.0

print(f"Average Huffman code length L = Σ p(x)*l(x) = {L_avg:.6f} bits/character")
print(f"Entropy H = {H:.6f} bits/character")
print(f"Efficiency η = H / L = {H:.6f} / {L_avg:.6f} = {eff:.6f} (={eff*100:.2f}%)")

# ---------------------------
# (f) Huffman total bits and compare to ASCII
# ---------------------------
print_header("(f) Bits needed using Huffman code + comparison to ASCII")
huff_total_bits = total_bits_huffman(sequence, codes)

print("Per-symbol contribution:")
for s in symbols:
    bits_sym = counter[s] * len(codes[s])
    print(f"  {s}: count={counter[s]}, code_len={len(codes[s])}, bits={counter[s]}*{len(codes[s])}={bits_sym}")

print(f"\nTotal Huffman bits = Σ count(x)*l(x) = {huff_total_bits} bits")
print(f"ASCII total bits (from part a) = {ascii_total_bits} bits")

saved_vs_ascii = ascii_total_bits - huff_total_bits
print(f"Bits saved vs ASCII = {ascii_total_bits} - {huff_total_bits} = {saved_vs_ascii} bits")
print(f"Compression ratio vs ASCII = Huffman/ASCII = {huff_total_bits}/{ascii_total_bits} = {huff_total_bits/ascii_total_bits:.6f}")

# ---------------------------
# (g) Lempel-Ziv (LZ78) bits and comparison
# ---------------------------
print_header("(g) Bits needed using Lempel-Ziv (LZ78) + comparisons")

print("LZ78 encoding steps:")
phrases, lz_dict = lz78_encode(sequence)
phrases = remove_empty_last_phrase(phrases)

print("\nLZ78 phrases (index, char):")
for i, (idx, ch) in enumerate(phrases, start=1):
    print(f"  {i:>3}: ({idx}, '{ch}')")

final_dict_size = len(phrases) + 1   # +1 for empty string
print(f"\nNumber of phrases = {len(phrases)}")
print(f"Final dictionary size (including empty) = {final_dict_size}")

# ============================================================
# (g-1) LZ78 with FIXED-LENGTH symbols (ceil(log2(k)))
# ============================================================
alphabet_bits_fixed = math.ceil(safe_log2(k))
print_header("(g-1) LZ78 using fixed-length symbols")
print(f"Character bits = ceil(log2(k)) = ceil(log2({k})) = {alphabet_bits_fixed} bits")

lz_total_fixed_fixed, fixed_idx_bits_fixed, fixed_breakdown_fixed = \
    lz78_bits_fixed_final(phrases, alphabet_bits_fixed, final_dict_size)

print(f"Index bits = ceil(log2(final_dict_size)) = {fixed_idx_bits_fixed} bits")
print("\nFixed-bit accounting:")

print(f"\nTotal LZ78 bits (fixed index, fixed-length symbols) = {lz_total_fixed_fixed} bits")

# ============================================================
# (g-2) LZ78 with ASCII symbols (8 bits per character)
# ============================================================
alphabet_bits_ascii = 8
print_header("(g-2) LZ78 using ASCII symbols")
print(f"Character bits = {alphabet_bits_ascii} bits (ASCII)")

lz_total_fixed_ascii, fixed_idx_bits_ascii, fixed_breakdown_ascii = \
    lz78_bits_fixed_final(phrases, alphabet_bits_ascii, final_dict_size)

print(f"Index bits = ceil(log2(final_dict_size)) = {fixed_idx_bits_ascii} bits")
print("\nFixed-bit accounting:")

print(f"\nTotal LZ78 bits (fixed index, ASCII symbols) = {lz_total_fixed_ascii} bits")

# ============================================================
# Final comparison
# ============================================================
print_header("(g) Final comparison")
print(f"ASCII total bits   = {ascii_total_bits}")
print(f"Huffman total bits = {huff_total_bits}")

print("\nLZ78 totals:")
print(f"  Fixed-length symbols : {lz_total_fixed_fixed} bits")
print(f"  ASCII symbols        : {lz_total_fixed_ascii} bits")

print("\nCompression ratios vs ASCII:")
print(f"  LZ78 (fixed-length symbols) / ASCII = {lz_total_fixed_fixed/ascii_total_bits:.6f}")
print(f"  LZ78 (ASCII symbols)        / ASCII = {lz_total_fixed_ascii/ascii_total_bits:.6f}")

print("\nCompression ratios vs Huffman:")
print(f"  LZ78 (fixed-length symbols) / Huffman = {lz_total_fixed_fixed/huff_total_bits:.6f}")
print(f"  LZ78 (ASCII symbols)        / Huffman = {lz_total_fixed_ascii/huff_total_bits:.6f}")
