import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# urutan kerusakan buatan, tiap mutan berdiri sendiri (bukan menumpuk)
MUTANTS = [
    ("M1 hapus penerapan diskon", HERE / "pricing_no_discount.py"),
    ("M2 ubah tarif pajak 0.11 ke 0.10", HERE / "pricing_tax_changed.py"),
    ("M3 hapus validasi kuantitas", HERE / "pricing_no_quantity_check.py"),
]

def run_tests(pricing_file):
    # tests dijalankan di folder sementara, pricing.py asli tidak disentuh
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copy(pricing_file, tmp / "pricing.py")
        shutil.copy(ROOT / "pytest.ini", tmp / "pytest.ini")
        shutil.copytree(ROOT / "tests", tmp / "tests", ignore=shutil.ignore_patterns("__pycache__"))
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider"],
            cwd=tmp, capture_output=True, text=True,
        )
    failed = re.findall(r"^FAILED tests/test_pricing\.py::(\S+)", result.stdout, re.M)
    summary = re.sub(r" in [\d.]+s", "", result.stdout.strip().splitlines()[-1])
    return failed, summary

def show_diff(mutant_file):
    original = (ROOT / "pricing.py").read_text().splitlines()
    mutant = mutant_file.read_text().splitlines()
    for line in difflib.unified_diff(original, mutant, n=0, lineterm=""):
        if line[:1] in "+-" and line[:3] not in ("+++", "---"):
            print("   ", line)

def main():
    failed, summary = run_tests(ROOT / "pricing.py")
    print(f"kode asli: {summary}")
    if failed:
        sys.exit("kode asli harus lulus semua dulu")
    rows = []
    for label, path in MUTANTS:
        failed, summary = run_tests(path)
        print(f"\n{label} ({path.name})")
        show_diff(path)
        print(f"  hasil: {summary}")
        for name in failed:
            print(f"  - {name}")
        verdict = f"terdeteksi, {len(failed)} test gagal" if failed else "LOLOS, tidak terdeteksi"
        rows.append((label, ", ".join(failed) or "-", verdict))
    print("\n| Kerusakan buatan | Test yang gagal | Kesimpulan daya deteksi |")
    print("|---|---|---|")
    for row in rows:
        print("| " + " | ".join(row) + " |")

if __name__ == "__main__":
    main()
