# Tugas Praktik Sesi 10 · Unit Test Modul `pricing.py`

Software Development Fundamentals. Unit test untuk modul `pricing.py` ditulis dengan PyTest, lalu daya deteksinya diuji lewat tiga mutan buatan.

## Anggota Kelompok

| Nama | NIM |
|---|---|
| HALIMAH SUKMAWATY | 25120300037 |
| KEVIN APRIANTO | 25120300004 |
| RIDHO MARWANSYAH | 25120300020 |
| MUHAMMAD AZHAR KHAIRA | 25120300010 |

## Struktur

```
sdf-tugas-10/
├── pricing.py                      # modul acuan, tidak diubah
├── pytest.ini                      # testpaths = tests, pythonpath = .
├── requirements.txt
├── tests/
│   └── test_pricing.py             # 18 fungsi test, 25 kasus
├── mutation/
│   ├── pricing_no_discount.py      # M1
│   ├── pricing_tax_changed.py      # M2
│   ├── pricing_no_quantity_check.py  # M3
│   └── run_mutation.py             # menjalankan test pada tiap mutan
└── hasil/
    ├── pytest-v.txt                # keluaran pytest -v pada kode asli
    └── mutasi.txt                  # keluaran run_mutation.py
```

## Cara menjalankan

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
python mutation/run_mutation.py
```

Perintah `pytest` cukup dijalankan tanpa argumen. Berkas `tests/test_pricing.py` mengikuti pola `test_*.py` sehingga ditemukan otomatis dan `pythonpath = .` di `pytest.ini` membuat `import pricing` terbaca dari folder `tests`.

## Pemetaan aturan bisnis ke test

| Aturan | Test |
|---|---|
| 1. Subtotal = harga satuan × kuantitas | `test_subtotal_is_unit_price_times_quantity` (3 kombinasi), `test_subtotal_with_float_price_uses_approx`, `test_subtotal_with_zero_price_is_allowed` |
| 2. Harga satuan negatif ditolak | `test_negative_unit_price_raises_value_error` (-1, -0.01, -50000) |
| 3. Kuantitas nol atau negatif ditolak | `test_zero_quantity_raises_value_error`, `test_negative_quantity_raises_value_error` (-1, -5), `test_total_rejects_zero_quantity` |
| 4. Diskon anggota 10%, non-anggota bayar penuh | `test_member_gets_ten_percent_discount`, `test_non_member_pays_full_price` |
| 5. Pajak 11% dari nilai setelah diskon | `test_add_tax_adds_eleven_percent` (100, 90000, 0), `test_total_non_member_is_subtotal_plus_tax`, `test_total_member_taxes_the_discounted_amount`, `test_total_default_is_non_member`, `test_member_total_is_below_subtotal` |
| 6. Setiap baris struk diakhiri baris baru | `test_receipt_every_line_ends_with_newline`, `test_receipt_single_line_still_ends_with_newline`, `test_receipt_overwrites_old_content`, `test_receipt_is_written_as_utf8` |

Kasus tepi yang ikut diuji adalah kuantitas 1, harga 0, harga negatif terkecil -0.01, pajak atas nilai 0 dan struk satu baris.

Penggunaan fitur wajib:

| Fitur | Dipakai di |
|---|---|
| `pytest.mark.parametrize` | 4 test (subtotal 3 kombinasi, harga negatif 3, kuantitas negatif 2, pajak 3) |
| `pytest.raises` | 4 test, semuanya memakai `match` sehingga pesan error ikut diperiksa |
| `pytest.approx` | 6 test yang hasilnya bilangan float |
| `tmp_path` | fixture `receipt_path`, dipakai 4 test struk |

## Keluaran `pytest -v` pada kode asli

```
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.1.1, pluggy-1.6.0 -- /Users/azharkhaira/Documents/azhar/cakrawala/class/sdf/task/sdf-tugas-10/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/azharkhaira/Documents/azhar/cakrawala/class/sdf/task/sdf-tugas-10
configfile: pytest.ini
testpaths: tests
collecting ... collected 25 items

tests/test_pricing.py::test_subtotal_is_unit_price_times_quantity[10000-3-30000] PASSED [  4%]
tests/test_pricing.py::test_subtotal_is_unit_price_times_quantity[2500-1-2500] PASSED [  8%]
tests/test_pricing.py::test_subtotal_is_unit_price_times_quantity[15000-12-180000] PASSED [ 12%]
tests/test_pricing.py::test_subtotal_with_float_price_uses_approx PASSED [ 16%]
tests/test_pricing.py::test_subtotal_with_zero_price_is_allowed PASSED   [ 20%]
tests/test_pricing.py::test_negative_unit_price_raises_value_error[-1] PASSED [ 24%]
tests/test_pricing.py::test_negative_unit_price_raises_value_error[-0.01] PASSED [ 28%]
tests/test_pricing.py::test_negative_unit_price_raises_value_error[-50000] PASSED [ 32%]
tests/test_pricing.py::test_zero_quantity_raises_value_error PASSED      [ 36%]
tests/test_pricing.py::test_negative_quantity_raises_value_error[-1] PASSED [ 40%]
tests/test_pricing.py::test_negative_quantity_raises_value_error[-5] PASSED [ 44%]
tests/test_pricing.py::test_total_rejects_zero_quantity PASSED           [ 48%]
tests/test_pricing.py::test_member_gets_ten_percent_discount PASSED      [ 52%]
tests/test_pricing.py::test_non_member_pays_full_price PASSED            [ 56%]
tests/test_pricing.py::test_add_tax_adds_eleven_percent[100-111] PASSED  [ 60%]
tests/test_pricing.py::test_add_tax_adds_eleven_percent[90000-99900] PASSED [ 64%]
tests/test_pricing.py::test_add_tax_adds_eleven_percent[0-0] PASSED      [ 68%]
tests/test_pricing.py::test_total_non_member_is_subtotal_plus_tax PASSED [ 72%]
tests/test_pricing.py::test_total_member_taxes_the_discounted_amount PASSED [ 76%]
tests/test_pricing.py::test_total_default_is_non_member PASSED           [ 80%]
tests/test_pricing.py::test_member_total_is_below_subtotal PASSED        [ 84%]
tests/test_pricing.py::test_receipt_every_line_ends_with_newline PASSED  [ 88%]
tests/test_pricing.py::test_receipt_single_line_still_ends_with_newline PASSED [ 92%]
tests/test_pricing.py::test_receipt_overwrites_old_content PASSED        [ 96%]
tests/test_pricing.py::test_receipt_is_written_as_utf8 PASSED            [100%]

============================== 25 passed in 0.03s ==============================
```

## Pengujian mutasi

Setiap mutan adalah salinan `pricing.py` dengan satu kerusakan. Skrip `mutation/run_mutation.py` menyalin folder `tests` dan satu mutan (dinamai `pricing.py`) ke folder sementara lalu menjalankan pytest di sana. Mutan dijalankan berurutan M1, M2 lalu M3 dan masing-masing berangkat dari kode asli, jadi kerusakannya tidak menumpuk. Berkas `pricing.py` asli tidak pernah diubah. Keluaran lengkapnya ada di `hasil/mutasi.txt`.

| Kerusakan buatan | Test yang gagal | Kesimpulan daya deteksi |
|---|---|---|
| **M1** · `apply_member_discount` mengembalikan `subtotal` tanpa diskon | `test_member_gets_ten_percent_discount`, `test_total_member_taxes_the_discounted_amount`, `test_member_total_is_below_subtotal` (3 dari 25) | Terdeteksi di tingkat fungsi diskon dan di tingkat total. Test non-anggota tetap lulus dan memang seharusnya begitu karena perilaku non-anggota tidak berubah. |
| **M2** · `TAX_RATE` diubah dari 0.11 menjadi 0.10 | `test_add_tax_adds_eleven_percent[100-111]`, `test_add_tax_adds_eleven_percent[90000-99900]`, `test_total_non_member_is_subtotal_plus_tax`, `test_total_member_taxes_the_discounted_amount`, `test_member_total_is_below_subtotal` (5 dari 25) | Terdeteksi. Kasus `add_tax(0)` tetap lulus karena 0 dikali tarif berapa pun hasilnya 0, jadi kasus itu tidak bisa membedakan tarif. Mutan ini tertangkap karena nilai harapan ditulis langsung (111, 33300) dan tidak dihitung ulang dari `pricing.TAX_RATE`. |
| **M3** · validasi `quantity <= 0` dihapus | `test_zero_quantity_raises_value_error`, `test_negative_quantity_raises_value_error[-1]`, `test_negative_quantity_raises_value_error[-5]`, `test_total_rejects_zero_quantity` (4 dari 25) | Terdeteksi. Tanpa validasi, kuantitas 0 menghasilkan subtotal 0 dan kuantitas negatif menghasilkan subtotal negatif tanpa error. Test validasi harga tetap lulus karena validasi harga tidak disentuh. |

Ketiga mutan terdeteksi. Satu test lolos dari ketiganya, yaitu `test_total_default_is_non_member`. Test itu dibahas di pertanyaan nomor 3.

## Jawaban Pertanyaan Analisis

### 1. Mengapa memakai `pytest.approx` untuk hasil floating point

Bilangan float disimpan dalam bentuk biner sehingga banyak pecahan desimal seperti 0.1 dan 1.11 tidak bisa disimpan persis. Di modul ini `add_tax(100)` menghasilkan `111.00000000000001` dan `calculate_subtotal(0.1, 3)` menghasilkan `0.30000000000000004`. Secara bisnis hasil itu benar tetapi `assert add_tax(100) == 111` akan gagal karena selisih di digit ke-14.

`pytest.approx` membandingkan dengan toleransi. Bawaannya relatif 1e-6 (sepersejuta nilai harapan) dengan batas absolut minimal 1e-12, jadi `pytest.approx(111)` menerima 111 ± 0.000111. Selisih pembulatan lolos sedangkan kesalahan nyata tetap gagal, misalnya pajak 10% yang menghasilkan 110. Test jadi gagal hanya ketika logikanya salah dan tidak gagal karena cara komputer menyimpan angka.

### 2. Risiko memakai berkas nyata di direktori proyek dibanding `tmp_path`

`write_receipt` membuka berkas dengan mode `"w"` yang langsung menimpa isi lama. Kalau test menulis ke path di dalam proyek, berkas yang kebetulan bernama sama ikut tertimpa. Berkas sisa test juga bisa ikut ter-commit ke repo.

Masalah lain adalah test menjadi tidak mandiri. Berkas yang tertinggal dari run sebelumnya atau dari test lain bisa membuat test lulus padahal fungsi yang diuji tidak menulis apa pun. Hasil test juga bisa bergantung pada urutan eksekusi. Kalau beberapa test dijalankan paralel, semuanya berebut berkas yang sama.

`tmp_path` memberi folder kosong yang berbeda untuk setiap test di luar folder proyek. Pytest yang membuat dan membersihkannya (bawaannya hanya folder dari 3 sesi terakhir yang disimpan), jadi setiap test mulai dari kondisi bersih dan proyek tidak tersentuh.

### 3. Test yang paling lemah

Test yang paling lemah adalah `test_total_default_is_non_member`.

```python
def test_total_default_is_non_member():
    assert calculate_total(10_000, 3) == calculate_total(10_000, 3, is_member=False)
```

Kedua sisi assertion berasal dari fungsi yang sedang diuji. Kalau perhitungannya salah, kedua sisi salah dengan cara yang sama dan test tetap lulus. Hasil mutasi membuktikannya. Test ini lolos di M1, M2 dan M3. Pada M2 kedua sisi sama-sama menghasilkan 33000 padahal seharusnya 33300. Test ini hanya akan gagal kalau nilai bawaan `is_member` berubah menjadi `True`.

Perbaikannya adalah membandingkan dengan angka yang dihitung manual dan memastikan hasilnya berbeda dari harga anggota.

```python
def test_total_default_is_non_member():
    total = calculate_total(10_000, 3)
    assert total == pytest.approx(33_300)
    assert total != pytest.approx(calculate_total(10_000, 3, is_member=True))
```

Versi ini sudah dicoba pada mutan dan gagal di M1 (total anggota ikut 33300) serta di M2 (total 33000).

### 4. Bagaimana pengujian mutasi mengubah cara menilai kualitas test

Sebelum mutasi, ukuran yang terlihat hanya "25 passed". Angka itu membuktikan test tidak gagal pada kode yang benar tetapi belum membuktikan test akan gagal pada kode yang salah. Pengujian mutasi menjawab bagian kedua itu.

Dari tiga mutan terlihat dua hal. Pertama, ada test yang lulus di semua kondisi (`test_total_default_is_non_member`) dan kasus yang tidak bisa membedakan tarif pajak (`add_tax(0)`). Keduanya tetap menambah jumlah test tetapi tidak menambah daya deteksi. Kedua, cara menulis nilai harapan ikut menentukan. M2 tertangkap karena harapannya ditulis 111 dan 33300. Kalau harapan dihitung dengan `amount * (1 + pricing.TAX_RATE)`, test akan ikut berubah bersama kodenya dan mutan M2 lolos.

Kualitas test jadi dinilai dari kemampuannya gagal ketika perilaku kode rusak, bukan dari banyaknya test atau banyaknya baris kode yang tereksekusi.

### 5. Padanan fitur PyTest dan JUnit 5

| PyTest | JUnit 5 |
|---|---|
| `with pytest.raises(ValueError, match="...")` | `assertThrows(IllegalArgumentException.class, () -> ...)`, pesannya dicek dari `getMessage()` pada exception yang dikembalikan |
| `@pytest.mark.parametrize("a, b", [...])` | `@ParameterizedTest` dengan `@ValueSource` (satu argumen), `@CsvSource` (beberapa argumen) atau `@MethodSource` |
| fixture | `@BeforeEach` / `@AfterEach` untuk penyiapan per test, `@BeforeAll` / `@AfterAll` untuk sekali per kelas |
| fixture `tmp_path` | `@TempDir Path tempDir` |
| `pytest.approx(x)` | `assertEquals(expected, actual, delta)` |

Perbedaannya ada di cara pakai. Fixture PyTest diminta lewat nama parameter dan bisa disusun bertingkat. Contohnya `receipt_path` dibangun di atas `tmp_path` dan hanya test struk yang memakainya. `@BeforeEach` di JUnit berjalan untuk semua test di kelas yang sama dan hasilnya disimpan di field. `pytest.raises` dipakai sebagai blok `with` sedangkan `assertThrows` menerima lambda. Toleransi `pytest.approx` bawaannya relatif sedangkan `delta` di JUnit adalah selisih absolut yang ditulis sendiri.

### 6. Mengapa "total anggota selalu lebih besar daripada subtotal" keliru

Untuk anggota, diskon 10% diterapkan dulu lalu pajak 11% dihitung dari nilai yang sudah didiskon.

```
subtotal          = 100.000 × 1        = 100.000
setelah diskon    = 100.000 × 0,90     =  90.000
setelah pajak     =  90.000 × 1,11     =  99.900
```

Total anggota 99.900 lebih kecil dari subtotal 100.000. Secara umum total anggota = subtotal × 0,9 × 1,11 = subtotal × 0,999, jadi selalu 0,1% di bawah subtotal untuk subtotal positif. Pajak 11% dihitung dari 90.000 sehingga hanya menambah 9.900, lebih kecil dari diskon 10.000. Saat harga 0, total dan subtotal sama-sama 0 sehingga total juga tidak lebih besar.

Asumsi itu hanya benar untuk non-anggota (subtotal × 1,11). Perilaku ini dikunci oleh `test_member_total_is_below_subtotal`.
