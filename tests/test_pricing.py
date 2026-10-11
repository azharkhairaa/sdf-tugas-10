import pytest

from pricing import (
    add_tax,
    apply_member_discount,
    calculate_subtotal,
    calculate_total,
    write_receipt,
)

# aturan 1: subtotal = harga satuan x kuantitas

@pytest.mark.parametrize(
    "unit_price, quantity, expected",
    [
        (10_000, 3, 30_000),
        (2_500, 1, 2_500),
        (15_000, 12, 180_000),
    ],
)
def test_subtotal_is_unit_price_times_quantity(unit_price, quantity, expected):
    assert calculate_subtotal(unit_price, quantity) == expected

def test_subtotal_with_float_price_uses_approx():
    # 0.1 * 3 = 0.30000000000000004, tidak persis 0.3
    assert calculate_subtotal(0.1, 3) == pytest.approx(0.3)

def test_subtotal_with_zero_price_is_allowed():
    # batas bawah harga: 0 bukan negatif, jadi tidak ditolak
    assert calculate_subtotal(0, 5) == 0

# aturan 2: harga satuan negatif ditolak

@pytest.mark.parametrize("unit_price", [-1, -0.01, -50_000])
def test_negative_unit_price_raises_value_error(unit_price):
    with pytest.raises(ValueError, match="unit_price must not be negative"):
        calculate_subtotal(unit_price, 1)

# aturan 3: kuantitas nol atau negatif ditolak

def test_zero_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(10_000, 0)

@pytest.mark.parametrize("quantity", [-1, -5])
def test_negative_quantity_raises_value_error(quantity):
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_subtotal(10_000, quantity)

def test_total_rejects_zero_quantity():
    # error validasi harus ikut naik lewat calculate_total, bukan jadi total 0
    with pytest.raises(ValueError, match="quantity must be positive"):
        calculate_total(10_000, 0, is_member=True)

# aturan 4: anggota diskon 10%, non-anggota bayar penuh

def test_member_gets_ten_percent_discount():
    assert apply_member_discount(100_000, True) == pytest.approx(90_000)

def test_non_member_pays_full_price():
    assert apply_member_discount(100_000, False) == 100_000

# aturan 5: pajak 11% dihitung dari nilai setelah diskon

@pytest.mark.parametrize(
    "amount, expected",
    [
        (100, 111),
        (90_000, 99_900),
        (0, 0),
    ],
)
def test_add_tax_adds_eleven_percent(amount, expected):
    assert add_tax(amount) == pytest.approx(expected)

def test_total_non_member_is_subtotal_plus_tax():
    # 30.000 + 11% = 33.300
    assert calculate_total(10_000, 3) == pytest.approx(33_300)

def test_total_member_taxes_the_discounted_amount():
    # 30.000 - 10% = 27.000, lalu + 11% = 29.970
    assert calculate_total(10_000, 3, is_member=True) == pytest.approx(29_970)

def test_total_default_is_non_member():
    assert calculate_total(10_000, 3) == calculate_total(10_000, 3, is_member=False)

def test_member_total_is_below_subtotal():
    # 0.9 x 1.11 = 0.999, jadi total anggota sedikit di bawah subtotal
    subtotal = calculate_subtotal(100_000, 1)
    total = calculate_total(100_000, 1, is_member=True)
    assert total == pytest.approx(99_900)
    assert total < subtotal

# aturan 6: setiap baris struk diakhiri newline, termasuk baris terakhir

@pytest.fixture
def receipt_path(tmp_path):
    # tmp_path = folder sementara per test, berkas proyek tidak tersentuh
    return tmp_path / "receipt.txt"

def test_receipt_every_line_ends_with_newline(receipt_path):
    write_receipt(receipt_path, ["Kopi Gayo x2", "Subtotal: 60000", "Total: 66600"])
    assert receipt_path.read_text(encoding="utf-8") == (
        "Kopi Gayo x2\nSubtotal: 60000\nTotal: 66600\n"
    )

def test_receipt_single_line_still_ends_with_newline(receipt_path):
    write_receipt(receipt_path, ["Total: 111"])
    assert receipt_path.read_text(encoding="utf-8") == "Total: 111\n"

def test_receipt_overwrites_old_content(receipt_path):
    receipt_path.write_text("struk lama\n", encoding="utf-8")
    write_receipt(receipt_path, ["struk baru"])
    assert receipt_path.read_text(encoding="utf-8") == "struk baru\n"

def test_receipt_is_written_as_utf8(receipt_path):
    write_receipt(receipt_path, ["Café Latte"])
    assert "Café Latte".encode("utf-8") in receipt_path.read_bytes()
