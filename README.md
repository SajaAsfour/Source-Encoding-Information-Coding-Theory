# 📊 Source Encoding – Information & Coding Theory

## 📌 Overview

This project analyzes different **source encoding techniques** and compares their efficiency when compressing a sequence of characters.

The implementation evaluates several encoding methods:

* ASCII Encoding
* Fixed-Length Encoding
* Huffman Coding
* Lempel–Ziv (LZ78) Compression

The goal is to measure how different compression methods reduce the number of bits required to represent the same data sequence.

The project was implemented using **Python** and analyzes entropy, coding efficiency, and compression ratios. 

---

# 🎯 Objectives

* Calculate the number of bits required using **ASCII encoding**
* Implement **fixed-length encoding**
* Compute **source entropy using Shannon’s formula**
* Generate **Huffman codes**
* Measure **Huffman coding efficiency**
* Implement **Lempel–Ziv (LZ78) compression**
* Compare compression performance across methods

---

# 🧾 Input Data

The project uses a long sequence of characters composed of a small alphabet:

```
A, B, C, D, E, F
```

Example sequence snippet:

```
ACBAAACDBACABAEACACBABDACAEABACBACADBACABEAACABDACBAC
```

This sequence is analyzed to determine symbol frequencies and compression potential.

---

# ⚙️ Technologies Used

* **Python**
* `math` library
* `heapq` (for Huffman tree)
* `collections.Counter`
* Data compression algorithms

---

# 📂 Project Structure

```
Source-Encoding
│
├── allNew.py            # Python implementation
├── Coding2Saja1210737.pdf
└── README.md
```

---

# 🔢 Encoding Methods Implemented

---

# 1️⃣ ASCII Encoding

ASCII assigns **8 bits per character** regardless of frequency.

For the sequence:

```
Length = 259 characters
```

Total bits required:

```
259 × 8 = 2072 bits
```

Although simple, ASCII is inefficient for small alphabets.

---

# 2️⃣ Fixed-Length Encoding

Fixed-length encoding assigns the same number of bits to each symbol based on alphabet size.

Alphabet size:

```
k = 6 symbols
```

Bits per character:

```
ceil(log₂(6)) = 3 bits
```

Total bits:

```
259 × 3 = 777 bits
```

This already provides significant compression compared to ASCII.

---

# 3️⃣ Source Entropy

Entropy measures the **average information per symbol** using Shannon’s formula:

```
H(X) = − Σ P(xᵢ) log₂(P(xᵢ))
```

Calculated entropy:

```
H ≈ 2.02 bits/character
```

This value represents the **theoretical lower bound for lossless compression**.

---

# 4️⃣ Huffman Coding

Huffman coding assigns **shorter codes to more frequent symbols**.

Algorithm steps:

1. Count symbol frequencies
2. Build a priority queue
3. Merge lowest-frequency nodes
4. Construct binary Huffman tree
5. Assign binary codes

Example codes:

```
A → 0
B → 111
C → 10
D → 1101
E → 11001
F → 11000
```

---

# 📉 Huffman Compression Results

Total bits required:

```
564 bits
```

Comparison:

| Method       | Bits |
| ------------ | ---- |
| ASCII        | 2072 |
| Fixed-Length | 777  |
| Huffman      | 564  |

Savings compared to ASCII:

```
2072 - 564 = 1508 bits
```

Huffman achieved the **best compression performance**. 

---

# 📊 Huffman Efficiency

Efficiency is calculated as:

```
Efficiency = H(X) / L_avg
```

Where:

* `H(X)` = entropy
* `L_avg` = average code length

Result:

```
Efficiency ≈ 95.8%
```

This indicates Huffman coding is very close to the theoretical limit.

---

# 5️⃣ Lempel–Ziv (LZ78) Compression

The LZ78 algorithm compresses data by building a **dictionary of repeated patterns**.

For the given sequence:

```
Number of phrases = 70
Dictionary size = 71
```

Two symbol representations were tested.

---

### LZ78 Results

| Method               | Bits |
| -------------------- | ---- |
| ASCII                | 2072 |
| Huffman              | 564  |
| LZ78 (fixed symbols) | 700  |
| LZ78 (ASCII symbols) | 1050 |

LZ78 provides compression but remains less efficient than Huffman for this dataset. 

---

# 📊 Compression Comparison

| Encoding Method | Bits | Compression          |
| --------------- | ---- | -------------------- |
| ASCII           | 2072 | Baseline             |
| Fixed-Length    | 777  | 62% reduction        |
| Huffman         | 564  | **Best performance** |
| LZ78 (fixed)    | 700  | Good compression     |
| LZ78 (ASCII)    | 1050 | Moderate compression |

Huffman coding performs best because the **symbol probabilities are uneven**, allowing frequent symbols to use shorter codes.

---

# 🧠 Key Concepts Learned

* Shannon entropy and information theory
* Prefix-free coding
* Huffman tree construction
* Dictionary-based compression
* Compression efficiency analysis

---

# 👩‍💻 Author

**Saja Asfour**

---

# 📚 References

* Shannon, C. E. – A Mathematical Theory of Communication
* Huffman Coding Algorithm
* Lempel–Ziv Compression Methods
* Python Documentation
