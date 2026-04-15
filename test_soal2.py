import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soal2_elearning import evaluasi_kelulusan


# ─── Rule 1: Semua syarat terpenuhi → LULUS ───────────────────────────────

class TestRuleLulus:
    def test_semua_syarat_terpenuhi(self):
        """R1: Kehadiran≥75, Nilai≥60, Lunas → LULUS"""
        r = evaluasi_kelulusan(80, 70, "Lunas")
        assert r['keputusan'] == "LULUS"

    def test_nilai_batas_lulus(self):
        """Batas minimum: Kehadiran=75, Nilai=60, Lunas → LULUS"""
        r = evaluasi_kelulusan(75, 60, "Lunas")
        assert r['keputusan'] == "LULUS"

    def test_nilai_maksimal_lulus(self):
        """Semua nilai maksimal: 100, 100, Lunas → LULUS"""
        r = evaluasi_kelulusan(100, 100, "Lunas")
        assert r['keputusan'] == "LULUS"

    def test_kehadiran_pas_75(self):
        """Kehadiran tepat 75% → masih LULUS jika syarat lain terpenuhi"""
        r = evaluasi_kelulusan(75, 80, "Lunas")
        assert r['keputusan'] == "LULUS"

    def test_nilai_pas_60(self):
        """Nilai Akhir tepat 60 → masih LULUS jika syarat lain terpenuhi"""
        r = evaluasi_kelulusan(80, 60, "Lunas")
        assert r['keputusan'] == "LULUS"


# ─── Rule 2: Kehadiran < 75% → TIDAK LULUS ───────────────────────────────

class TestRuleKehadiran:
    def test_kehadiran_kurang(self):
        """Kehadiran=60% → TIDAK LULUS meskipun nilai & bayar OK"""
        r = evaluasi_kelulusan(60, 90, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_kehadiran_nol(self):
        """Kehadiran=0% → TIDAK LULUS"""
        r = evaluasi_kelulusan(0, 100, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_kehadiran_74_9(self):
        """Kehadiran=74.9% (tepat di bawah batas) → TIDAK LULUS"""
        r = evaluasi_kelulusan(74.9, 90, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_alasan_kehadiran(self):
        """Pastikan alasan 'Kehadiran < 75%' tercatat"""
        r = evaluasi_kelulusan(50, 80, "Lunas")
        assert "Kehadiran" in r['alasan']


# ─── Rule 3: Pembayaran tidak lunas → TIDAK LULUS ────────────────────────

class TestRulePembayaran:
    def test_pembayaran_tidak_lunas(self):
        """Pembayaran Tidak Lunas → TIDAK LULUS meskipun nilai & kehadiran OK"""
        r = evaluasi_kelulusan(85, 90, "Tidak Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_pembayaran_string_kosong(self):
        """Status bayar string kosong → TIDAK LULUS"""
        r = evaluasi_kelulusan(85, 90, "")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_pembayaran_case_insensitive(self):
        """Status 'LUNAS' (kapital) → LULUS (case-insensitive)"""
        r = evaluasi_kelulusan(85, 90, "LUNAS")
        assert r['keputusan'] == "LULUS"

    def test_alasan_pembayaran(self):
        """Pastikan alasan 'Pembayaran tidak lunas' tercatat"""
        r = evaluasi_kelulusan(80, 80, "Belum Bayar")
        assert "Pembayaran" in r['alasan']


# ─── Rule 4: Nilai Akhir < 60 → TIDAK LULUS ──────────────────────────────

class TestRuleNilai:
    def test_nilai_kurang(self):
        """Nilai=55 → TIDAK LULUS meskipun kehadiran & bayar OK"""
        r = evaluasi_kelulusan(80, 55, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_nilai_nol(self):
        """Nilai=0 → TIDAK LULUS"""
        r = evaluasi_kelulusan(100, 0, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_nilai_59_9(self):
        """Nilai=59.9 (tepat di bawah 60) → TIDAK LULUS"""
        r = evaluasi_kelulusan(90, 59.9, "Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_alasan_nilai(self):
        """Pastikan alasan 'Nilai Akhir < 60' tercatat"""
        r = evaluasi_kelulusan(80, 40, "Lunas")
        assert "Nilai" in r['alasan']


# ─── Rule 5: Semua kondisi gagal ─────────────────────────────────────────

class TestRuleSemuaGagal:
    def test_semua_gagal(self):
        """Semua kondisi gagal → TIDAK LULUS"""
        r = evaluasi_kelulusan(50, 40, "Tidak Lunas")
        assert r['keputusan'] == "TIDAK LULUS"

    def test_kondisi_output_dict_keys(self):
        """Output harus berisi key yang diperlukan"""
        r = evaluasi_kelulusan(80, 70, "Lunas")
        assert all(k in r for k in ['keputusan', 'alasan', 'C1_hadir', 'C2_nilai', 'C3_bayar'])

    def test_kondisi_benar_untuk_lulus(self):
        """Semua kondisi C1, C2, C3 True saat LULUS"""
        r = evaluasi_kelulusan(80, 70, "Lunas")
        assert r['C1_hadir'] is True
        assert r['C2_nilai'] is True
        assert r['C3_bayar'] is True


# ─── Parametrized tests ───────────────────────────────────────────────────

@pytest.mark.parametrize("kehadiran,nilai,bayar,expected", [
    (80,  70, "Lunas",       "LULUS"),
    (75,  60, "Lunas",       "LULUS"),
    (74,  70, "Lunas",       "TIDAK LULUS"),
    (80,  59, "Lunas",       "TIDAK LULUS"),
    (80,  70, "Tidak Lunas", "TIDAK LULUS"),
    (60,  50, "Tidak Lunas", "TIDAK LULUS"),
    (100, 100,"Lunas",       "LULUS"),
    (75,  60, "Tidak Lunas", "TIDAK LULUS"),
])
def test_parametrized_kelulusan(kehadiran, nilai, bayar, expected):
    r = evaluasi_kelulusan(kehadiran, nilai, bayar)
    assert r['keputusan'] == expected
