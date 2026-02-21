"""
Astro Matching Engine — Core Calculation Logic
Implements all 10 Poruthams with full accuracy.
"""

from master_data import (
    NAKSHATRAS, RASIS, PORUTHAMS,
    GANA_TABLE, NADI_TABLE, YONI_TABLE,
    RAJJU_SCORES, STAR_RAJJU,
    VARNA_RANK, MAHENDRA_GOOD, STREE_DEERGA_THRESHOLD,
    VEDHA_PAIRS, PLANET_FRIENDS, PLANET_ENEMIES,
    RASI_COMPATIBILITY, DINA_COMPATIBILITY,
    get_nakshatra_by_name, get_rasi_by_name,
    get_padham_navamsa, TOTAL_MAX_SCORE
)


class MatchResult:
    """Holds result for a single Porutham."""
    def __init__(self, name: str, tamil: str, score: int, max_score: int,
                 compatibility: str, details: str, is_critical: bool,
                 category: str, dosha: bool = False):
        self.name = name
        self.tamil = tamil
        self.score = score
        self.max_score = max_score
        self.compatibility = compatibility
        self.details = details
        self.is_critical = is_critical
        self.category = category
        self.dosha = dosha
        self.percentage = round((score / max_score) * 100, 1) if max_score else 0

    def to_dict(self):
        return {
            "name": self.name,
            "tamil": self.tamil,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": self.percentage,
            "compatibility": self.compatibility,
            "details": self.details,
            "is_critical": self.is_critical,
            "category": self.category,
            "dosha": self.dosha,
        }


class AstroMatchingEngine:
    """
    Main engine for computing all 10 Poruthams.
    Easily extensible — add new methods and register in calculate_all().
    """

    def __init__(self, groom: dict, bride: dict):
        """
        groom / bride = {
            "name": str,
            "star_name": str,      # Nakshatra name (English)
            "padham": int,          # 1-4
            "rasi_name": str,       # Rasi name (English)
        }
        """
        self.groom = groom
        self.bride = bride
        self.groom_star = get_nakshatra_by_name(groom["star_name"])
        self.bride_star = get_nakshatra_by_name(bride["star_name"])
        self.groom_rasi = get_rasi_by_name(groom["rasi_name"])
        self.bride_rasi = get_rasi_by_name(bride["rasi_name"])
        self.results: list[MatchResult] = []
        self.summary = {}

    # ──────────────────────────────────────────────
    # 1. DINA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_dina(self) -> MatchResult:
        g_id = self.groom_star["id"]
        b_id = self.bride_star["id"]
        count = ((g_id - b_id) % 27) + 1  # count from bride to groom
        good = DINA_COMPATIBILITY["good_counts"]
        remainder = count % 9
        if remainder in good:
            score = 3; compat = "Excellent"
        elif count % 3 == 0:
            score = 2; compat = "Good"
        else:
            score = 0; compat = "Poor"
        details = (f"Star count from Bride ({self.bride_star['name']}) to "
                   f"Groom ({self.groom_star['name']}) = {count}. "
                   f"Remainder (÷9) = {remainder}.")
        return MatchResult("Dina Porutham", "தின பொருத்தம்", score, 3, compat, details, False, "Health")

    # ──────────────────────────────────────────────
    # 2. GANA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_gana(self) -> MatchResult:
        g_gana = self.groom_star["gana"]
        b_gana = self.bride_star["gana"]
        result = GANA_TABLE.get((g_gana, b_gana), {"score": 0, "compatibility": "Unknown"})
        score = result["score"]
        compat = result["compatibility"]
        dosha = score < 3
        details = (f"Groom Gana: {g_gana} | Bride Gana: {b_gana}. "
                   f"{'⚠️ Gana Dosha present!' if dosha else 'Compatible Ganas.'}")
        return MatchResult("Gana Porutham", "கண பொருத்தம்", score, 6, compat, details, True, "Temperament", dosha)

    # ──────────────────────────────────────────────
    # 3. MAHENDRA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_mahendra(self) -> MatchResult:
        g_id = self.groom_star["id"]
        b_id = self.bride_star["id"]
        count = ((g_id - b_id) % 27) + 1
        good = count in MAHENDRA_GOOD
        score = 2 if good else 0
        compat = "Excellent — Prosperity & Children" if good else "No Mahendra — Financial Caution"
        details = (f"Count from Bride to Groom = {count}. "
                   f"Mahendra stars: multiples of 4,7,10... "
                   f"{'✅ Mahendra present!' if good else '❌ Not a Mahendra star count.'}")
        return MatchResult("Mahendra Porutham", "மகேந்திர பொருத்தம்", score, 2, compat, details, False, "Prosperity")

    # ──────────────────────────────────────────────
    # 4. STREE DEERGA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_stree_deerga(self) -> MatchResult:
        g_id = self.groom_star["id"]
        b_id = self.bride_star["id"]
        count = ((g_id - b_id) % 27) + 1  # count from bride to groom
        if count > 13:
            score = 3; compat = "Excellent — Long life & wellbeing for wife"
        elif count > 7:
            score = 2; compat = "Good — Acceptable Stree Deerga"
        else:
            score = 0; compat = "Poor — Stree Deerga Dosha"
        dosha = score == 0
        details = (f"Count from Bride star to Groom star = {count}. "
                   f"Required: > {STREE_DEERGA_THRESHOLD}. "
                   f"{'✅ Compatible' if not dosha else '⚠️ Dosha — Short count affects wife longevity'}.")
        return MatchResult("Stree Deerga", "ஸ்திரீ தீர்க்கம்", score, 3, compat, details, False, "Wife Longevity", dosha)

    # ──────────────────────────────────────────────
    # 5. YONI PORUTHAM
    # ──────────────────────────────────────────────
    def calc_yoni(self) -> MatchResult:
        g_yoni = self.groom_star["yoni"]
        b_yoni = self.bride_star["yoni"]
        pair = (g_yoni, b_yoni)
        if pair in YONI_TABLE["friendly"]:
            score = 4; compat = "Excellent — Same Yoni/Friendly"
        elif pair in YONI_TABLE["enemy"]:
            score = 0; compat = "Very Poor — Enemy Yoni Dosha"
        else:
            score = 2; compat = "Neutral — Acceptable"
        dosha = score == 0
        details = (f"Groom Yoni: {g_yoni} | Bride Yoni: {b_yoni}. "
                   f"{'⚠️ Enemy Yoni — physical incompatibility!' if dosha else 'Yoni compatible.'}")
        return MatchResult("Yoni Porutham", "யோனி பொருத்தம்", score, 4, compat, details, True, "Physical Harmony", dosha)

    # ──────────────────────────────────────────────
    # 6. RASI PORUTHAM (with Rasi Adhipathi)
    # ──────────────────────────────────────────────
    def calc_rasi(self) -> MatchResult:
        g_rasi_id = self.groom_rasi["id"]
        b_rasi_id = self.bride_rasi["id"]
        pair_score = RASI_COMPATIBILITY["pairs"].get((g_rasi_id, b_rasi_id), 1)

        # Planetary lord compatibility bonus
        g_lord = self.groom_rasi["lord"]
        b_lord = self.bride_rasi["lord"]
        lord_bonus = 0
        if b_lord in PLANET_FRIENDS.get(g_lord, []):
            lord_bonus = 2; lord_compat = "Friendly lords"
        elif b_lord in PLANET_ENEMIES.get(g_lord, []):
            lord_bonus = -1; lord_compat = "Enemy lords"
        else:
            lord_bonus = 1; lord_compat = "Neutral lords"

        # Base scores: 0→1, 1→3, 2→5
        base = [1, 3, 5][pair_score]
        final_score = max(0, min(7, base + lord_bonus))

        if final_score >= 6:
            compat = "Excellent"
        elif final_score >= 4:
            compat = "Good"
        elif final_score >= 2:
            compat = "Average"
        else:
            compat = "Poor"

        dosha = final_score < 2
        details = (f"Groom Rasi: {self.groom_rasi['name']} (Lord: {g_lord}) | "
                   f"Bride Rasi: {self.bride_rasi['name']} (Lord: {b_lord}). "
                   f"Rasi compatibility: {['Incompatible','Compatible','Highly Compatible'][pair_score]}. "
                   f"Lord compatibility: {lord_compat}. Final score: {final_score}/7.")
        return MatchResult("Rasi Porutham", "ராசி பொருத்தம்", final_score, 7, compat, details, True, "Mental Harmony", dosha)

    # ──────────────────────────────────────────────
    # 7. RAJJU PORUTHAM
    # ──────────────────────────────────────────────
    def calc_rajju(self) -> MatchResult:
        g_id = self.groom_star["id"]
        b_id = self.bride_star["id"]
        g_rajju = STAR_RAJJU.get(g_id, "Unknown")
        b_rajju = STAR_RAJJU.get(b_id, "Unknown")
        if g_rajju != b_rajju:
            result = RAJJU_SCORES["different"]
            dosha = False
        else:
            result = RAJJU_SCORES.get(g_rajju, {"score": 0, "compatibility": "Dosha"})
            dosha = True
        score = result["score"]
        compat = result["compatibility"]
        details = (f"Groom Rajju: {g_rajju} | Bride Rajju: {b_rajju}. "
                   f"{'⚠️ Same Rajju — Dosha! ' + compat if dosha else '✅ Different Rajju — No Dosha!'}")
        return MatchResult("Rajju Porutham", "ரஜ்ஜு பொருத்தம்", score, 5, compat, details, True, "Marital Bliss", dosha)

    # ──────────────────────────────────────────────
    # 8. VEDHA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_vedha(self) -> MatchResult:
        g_id = self.groom_star["id"]
        b_id = self.bride_star["id"]
        has_vedha = (g_id, b_id) in VEDHA_PAIRS
        score = 0 if has_vedha else 2
        compat = "⚠️ Vedha Dosha — Obstacle present!" if has_vedha else "✅ No Vedha Dosha"
        dosha = has_vedha
        details = (f"Groom Star: #{g_id} | Bride Star: #{b_id}. "
                   f"{'These stars cause mutual affliction (Vedha)!' if has_vedha else 'No Vedha obstruction between these stars.'}")
        return MatchResult("Vedha Porutham", "வேத பொருத்தம்", score, 2, compat, details, False, "Obstacles", dosha)

    # ──────────────────────────────────────────────
    # 9. VARNA PORUTHAM
    # ──────────────────────────────────────────────
    def calc_varna(self) -> MatchResult:
        g_varna = self.groom_star["varna"]
        b_varna = self.bride_star["varna"]
        g_rank = VARNA_RANK.get(g_varna, 0)
        b_rank = VARNA_RANK.get(b_varna, 0)
        compatible = g_rank >= b_rank
        score = 1 if compatible else 0
        compat = "Compatible" if compatible else "Varna Mismatch — Caution"
        dosha = not compatible
        details = (f"Groom Varna: {g_varna} (rank {g_rank}) | Bride Varna: {b_varna} (rank {b_rank}). "
                   f"Groom varna should be ≥ Bride varna. {'✅ Compatible' if compatible else '⚠️ Mismatch'}.")
        return MatchResult("Varna Porutham", "வர்ண பொருத்தம்", score, 1, compat, details, False, "Spiritual", dosha)

    # ──────────────────────────────────────────────
    # 10. NADI PORUTHAM
    # ──────────────────────────────────────────────
    def calc_nadi(self) -> MatchResult:
        g_nadi = self.groom_star["nadi"]
        b_nadi = self.bride_star["nadi"]
        result = NADI_TABLE.get((g_nadi, b_nadi), {"score": 0, "compatibility": "Unknown"})
        score = result["score"]
        compat = result["compatibility"]
        dosha = score == 0
        details = (f"Groom Nadi: {g_nadi} | Bride Nadi: {b_nadi}. "
                   f"{'⚠️ NADI DOSHA — Same Nadi! Health issues & lineage concerns.' if dosha else '✅ Different Nadi — Excellent health compatibility!'}")
        return MatchResult("Nadi Porutham", "நாடி பொருத்தம்", score, 8, compat, details, True, "Health & Lineage", dosha)

    # ──────────────────────────────────────────────
    # PADHAM ANALYSIS (Bonus)
    # ──────────────────────────────────────────────
    def calc_padham_analysis(self) -> dict:
        g_padham = self.groom.get("padham", 1)
        b_padham = self.bride.get("padham", 1)
        g_navamsa = get_padham_navamsa(self.groom_star["id"], g_padham)
        b_navamsa = get_padham_navamsa(self.bride_star["id"], b_padham)
        g_navamsa_rasi = get_rasi_by_name(g_navamsa)
        b_navamsa_rasi = get_rasi_by_name(b_navamsa)

        lord_compat = ""
        if g_navamsa_rasi and b_navamsa_rasi:
            g_lord = g_navamsa_rasi["lord"]
            b_lord = b_navamsa_rasi["lord"]
            if b_lord in PLANET_FRIENDS.get(g_lord, []):
                lord_compat = "Friendly — Excellent Navamsa harmony"
            elif b_lord in PLANET_ENEMIES.get(g_lord, []):
                lord_compat = "Enemy — Navamsa tension"
            else:
                lord_compat = "Neutral — Acceptable Navamsa"
        return {
            "groom_padham": g_padham,
            "bride_padham": b_padham,
            "groom_navamsa": g_navamsa,
            "bride_navamsa": b_navamsa,
            "navamsa_lord_compatibility": lord_compat,
        }

    # ──────────────────────────────────────────────
    # MAIN CALCULATE
    # ──────────────────────────────────────────────
    def calculate_all(self) -> dict:
        calculators = [
            self.calc_dina,
            self.calc_gana,
            self.calc_mahendra,
            self.calc_stree_deerga,
            self.calc_yoni,
            self.calc_rasi,
            self.calc_rajju,
            self.calc_vedha,
            self.calc_varna,
            self.calc_nadi,
        ]
        self.results = [fn() for fn in calculators]

        raw_score = sum(r.score for r in self.results)
        weighted_score = sum(
            r.score * next(p["weight"] for p in PORUTHAMS if p["name"] == r.name)
            for r in self.results
        )
        max_weighted = sum(
            p["max_score"] * p["weight"] for p in PORUTHAMS
        )
        final_percentage = round((weighted_score / max_weighted) * 100, 1)
        raw_percentage = round((raw_score / TOTAL_MAX_SCORE) * 100, 1)

        critical_doshas = [r for r in self.results if r.dosha and r.is_critical]
        minor_doshas = [r for r in self.results if r.dosha and not r.is_critical]
        all_doshas = [r for r in self.results if r.dosha]

        if final_percentage >= 80 and not critical_doshas:
            verdict = "Excellent Match ✨"
            verdict_color = "green"
        elif final_percentage >= 65 and len(critical_doshas) <= 1:
            verdict = "Good Match 👍"
            verdict_color = "blue"
        elif final_percentage >= 50:
            verdict = "Average Match — Consult Astrologer 🔍"
            verdict_color = "orange"
        else:
            verdict = "Poor Match ⚠️"
            verdict_color = "red"

        # Override if Nadi or Rajju Dosha (most critical)
        for r in critical_doshas:
            if r.name in ["Nadi Porutham", "Rajju Porutham"] and r.score == 0:
                verdict = f"⚠️ Critical Dosha: {r.name} — Strongly Caution"
                verdict_color = "red"
                break

        padham_analysis = self.calc_padham_analysis()

        self.summary = {
            "groom": self.groom,
            "bride": self.bride,
            "groom_star_details": self.groom_star,
            "bride_star_details": self.bride_star,
            "groom_rasi_details": self.groom_rasi,
            "bride_rasi_details": self.bride_rasi,
            "results": [r.to_dict() for r in self.results],
            "raw_score": raw_score,
            "raw_max": TOTAL_MAX_SCORE,
            "raw_percentage": raw_percentage,
            "weighted_score": round(weighted_score, 2),
            "max_weighted": round(max_weighted, 2),
            "final_percentage": final_percentage,
            "verdict": verdict,
            "verdict_color": verdict_color,
            "critical_doshas": [r.name for r in critical_doshas],
            "minor_doshas": [r.name for r in minor_doshas],
            "total_doshas": len(all_doshas),
            "padham_analysis": padham_analysis,
        }
        return self.summary
