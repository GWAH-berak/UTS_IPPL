import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soal1 import (
    validate_input,
    hitung_nilai_akhir,
    tentukan_grade,
)


# ─── 1. Test Valid Input ───────────────────────────────────────────────────

class TestValidInput:
    def test_nilai_normal(self):
        hasil = hitung_nilai_akhir(80, 75, 90)
        assert isinstance(hasil, float)
        assert hasil == pytest.approx(82.5, 0.01)

    def test_grade_A(self):
        hasil = hitung_nilai_akhir(90, 90, 90)
        assert tentukan_grade(hasil) == "A"

    def test_grade_B(self):
        hasil = hitung_nilai_akhir(75, 75, 80)
        grade = tentukan_grade(hasil)
        assert grade == "B"

    def test_grade_C(self):
        hasil = hitung_nilai_akhir(70, 65, 70)
        grade = tentukan_grade(hasil)
        assert grade == "C"

    def test_grade_D(self):
        hasil = hitung_nilai_akhir(60, 50, 55)
        grade = tentukan_grade(hasil)
        assert grade == "D"

    def test_grade_E(self):
        hasil = hitung_nilai_akhir(30, 40, 30)
        grade = tentukan_grade(hasil)
        assert grade == "E"

    def test_rumus_perhitungan(self):
        hasil = hitung_nilai_akhir(70, 80, 90)
        assert hasil == pytest.approx(81.0, 0.01)

    def test_input_float(self):
        hasil = hitung_nilai_akhir(77.5, 82.5, 88.0)
        assert isinstance(hasil, float)


# ─── 2. Test Boundary Values ──────────────────────────────────────────────

class TestBoundaryValues:
    def test_tugas_minimum(self):
        hasil = hitung_nilai_akhir(0, 50, 50)
        assert isinstance(hasil, float)
        assert hasil == pytest.approx(35.0, 0.01)

    def test_tugas_minimum_plus_1(self):
        hasil = hitung_nilai_akhir(1, 50, 50)
        assert isinstance(hasil, float)

    def test_tugas_maximum_minus_1(self):
        hasil = hitung_nilai_akhir(99, 50, 50)
        assert isinstance(hasil, float)

    def test_tugas_maximum(self):
        hasil = hitung_nilai_akhir(100, 50, 50)
        assert isinstance(hasil, float)
        assert hasil == pytest.approx(65.0, 0.01)

    def test_uts_minimum(self):
        hasil = hitung_nilai_akhir(50, 0, 50)
        assert isinstance(hasil, float)

    def test_uts_maximum(self):
        hasil = hitung_nilai_akhir(50, 100, 50)
        assert isinstance(hasil, float)

    def test_uas_minimum(self):
        hasil = hitung_nilai_akhir(50, 50, 0)
        assert isinstance(hasil, float)

    def test_uas_maximum(self):
        hasil = hitung_nilai_akhir(50, 50, 100)
        assert isinstance(hasil, float)

    def test_semua_minimum(self):
        hasil = hitung_nilai_akhir(0, 0, 0)
        assert hasil == pytest.approx(0.0, 0.01)
        assert tentukan_grade(hasil) == "E"

    def test_semua_maximum(self):
        hasil = hitung_nilai_akhir(100, 100, 100)
        assert hasil == pytest.approx(100.0, 0.01)
        assert tentukan_grade(hasil) == "A"

    def test_batas_grade_E_D(self):
        # 30*x + 30*x + 40*x = 100x = 50 → x = 50
        hasil = hitung_nilai_akhir(50, 50, 50)
        assert tentukan_grade(hasil) == "D"

    def test_batas_grade_C_B(self):
        hasil = hitung_nilai_akhir(75, 75, 75)
        assert tentukan_grade(hasil) == "B"

    def test_batas_grade_B_A(self):
        hasil = hitung_nilai_akhir(85, 85, 85)
        assert tentukan_grade(hasil) == "A"


# ─── 3. Test Invalid Input ────────────────────────────────────────────────

class TestInvalidInput:
    def test_tugas_out_of_bound_bawah(self):
        hasil = hitung_nilai_akhir(-1, 50, 50)
        assert isinstance(hasil, str)
        assert "ERROR" in hasil

    def test_tugas_out_of_bound_atas(self):
        hasil = hitung_nilai_akhir(101, 50, 50)
        assert isinstance(hasil, str)
        assert "ERROR" in hasil

    def test_uts_out_of_bound_bawah(self):
        hasil = hitung_nilai_akhir(50, -1, 50)
        assert isinstance(hasil, str)

    def test_uts_out_of_bound_atas(self):
        hasil = hitung_nilai_akhir(50, 101, 50)
        assert isinstance(hasil, str)

    def test_uas_out_of_bound_bawah(self):
        hasil = hitung_nilai_akhir(50, 50, -1)
        assert isinstance(hasil, str)

    def test_uas_out_of_bound_atas(self):
        hasil = hitung_nilai_akhir(50, 50, 101)
        assert isinstance(hasil, str)

    def test_input_string(self):
        hasil = hitung_nilai_akhir("80", 50, 50)
        assert isinstance(hasil, str)
        assert "ERROR" in hasil

    def test_input_none(self):
        hasil = hitung_nilai_akhir(None, 50, 50)
        assert isinstance(hasil, str)
        assert "ERROR" in hasil

    def test_input_list(self):
        hasil = hitung_nilai_akhir([80], 50, 50)
        assert isinstance(hasil, str)

    def test_input_sangat_negatif(self):
        hasil = hitung_nilai_akhir(-999, 50, 50)
        assert isinstance(hasil, str)

    def test_input_sangat_besar(self):
        hasil = hitung_nilai_akhir(9999, 50, 50)
        assert isinstance(hasil, str)


# ─── 4. Test validate_input langsung ──────────────────────────────────────

class TestValidateInput:
    def test_valid_integer(self):
        valid, _ = validate_input(75, "Tugas")
        assert valid is True

    def test_valid_float(self):
        valid, _ = validate_input(75.5, "UTS")
        assert valid is True

    def test_invalid_string(self):
        valid, msg = validate_input("70", "UAS")
        assert valid is False
        assert "numerik" in msg

    def test_invalid_none(self):
        valid, msg = validate_input(None, "Tugas")
        assert valid is False

    def test_invalid_below_zero(self):
        valid, msg = validate_input(-5, "UTS")
        assert valid is False
        assert "rentang" in msg

    def test_invalid_above_100(self):
        valid, msg = validate_input(105, "UAS")
        assert valid is False
        assert "rentang" in msg

    def test_zero_is_valid(self):
        valid, _ = validate_input(0, "Tugas")
        assert valid is True

    def test_hundred_is_valid(self):
        valid, _ = validate_input(100, "Tugas")
        assert valid is True


# ─── 5. Test tentukan_grade ───────────────────────────────────────────────

class TestTentukanGrade:
    @pytest.mark.parametrize("nilai,expected", [
        (0,   "E"), (49.9, "E"),
        (50,  "D"), (64.9, "D"),
        (65,  "C"), (74.9, "C"),
        (75,  "B"), (84.9, "B"),
        (85,  "A"), (100,  "A"),
    ])
    def test_semua_grade(self, nilai, expected):
        assert tentukan_grade(nilai) == expected

    def test_grade_untuk_string_error(self):
        assert tentukan_grade("ERROR: invalid") == "INVALID"

def test_nilai_normal_output():
    hasil = hitung_nilai_akhir(80, 75, 90)
    print(f"Hasil nilai akhir: {hasil}")
    assert isinstance(hasil, float)