"""TDD tests for IUPAC ambiguity code support in PAM matching."""
from src.crispr.grna_design import _pam_matches_iupac


class TestPAMMatchesIUPAC:
    """Test IUPAC ambiguity code matching."""

    def test_exact_match(self):
        assert _pam_matches_iupac("NGG", "AGG") is True

    def test_n_wildcard(self):
        assert _pam_matches_iupac("NGG", "TGG") is True
        assert _pam_matches_iupac("NGG", "CGG") is True
        assert _pam_matches_iupac("NGG", "GGG") is True

    def test_r_purine(self):
        assert _pam_matches_iupac("RG", "AG") is True
        assert _pam_matches_iupac("RG", "GG") is True
        assert _pam_matches_iupac("RG", "CG") is False

    def test_y_pyrimidine(self):
        assert _pam_matches_iupac("YC", "TC") is True
        assert _pam_matches_iupac("YC", "CC") is True
        assert _pam_matches_iupac("YC", "AC") is False

    def test_s_strong(self):
        assert _pam_matches_iupac("SG", "CG") is True
        assert _pam_matches_iupac("SG", "GG") is True
        assert _pam_matches_iupac("SG", "AG") is False

    def test_w_weak(self):
        assert _pam_matches_iupac("WA", "TA") is True
        assert _pam_matches_iupac("WA", "AA") is True
        assert _pam_matches_iupac("WA", "GA") is False

    def test_k_keto(self):
        assert _pam_matches_iupac("KT", "GT") is True
        assert _pam_matches_iupac("KT", "TT") is True
        assert _pam_matches_iupac("KT", "AT") is False

    def test_m_amino(self):
        assert _pam_matches_iupac("MA", "AA") is True
        assert _pam_matches_iupac("MA", "CA") is True
        assert _pam_matches_iupac("MA", "GA") is False

    def test_b_not_a(self):
        assert _pam_matches_iupac("BC", "CC") is True
        assert _pam_matches_iupac("BC", "TC") is True
        assert _pam_matches_iupac("BC", "GC") is True
        assert _pam_matches_iupac("BC", "AC") is False

    def test_d_not_c(self):
        assert _pam_matches_iupac("DA", "AA") is True
        assert _pam_matches_iupac("DA", "GA") is True
        assert _pam_matches_iupac("DA", "TA") is True
        assert _pam_matches_iupac("DA", "CA") is False

    def test_h_not_g(self):
        assert _pam_matches_iupac("HA", "AA") is True
        assert _pam_matches_iupac("HA", "CA") is True
        assert _pam_matches_iupac("HA", "TA") is True
        assert _pam_matches_iupac("HA", "GA") is False

    def test_v_not_t(self):
        assert _pam_matches_iupac("VA", "AA") is True
        assert _pam_matches_iupac("VA", "CA") is True
        assert _pam_matches_iupac("VA", "GA") is True
        assert _pam_matches_iupac("VA", "TA") is False

    def test_n_any(self):
        assert _pam_matches_iupac("NA", "AA") is True
        assert _pam_matches_iupac("NA", "CA") is True
        assert _pam_matches_iupac("NA", "GA") is True
        assert _pam_matches_iupac("NA", "TA") is True

    def test_cas12a_tttv(self):
        assert _pam_matches_iupac("TTTV", "TTTA") is True
        assert _pam_matches_iupac("TTTV", "TTTC") is True
        assert _pam_matches_iupac("TTTV", "TTTG") is True
        assert _pam_matches_iupac("TTTV", "TTTT") is False

    def test_mixed_iupac(self):
        assert _pam_matches_iupac("NRG", "AAG") is True
        assert _pam_matches_iupac("NRG", "CGG") is True
        assert _pam_matches_iupac("NRG", "TGA") is False
