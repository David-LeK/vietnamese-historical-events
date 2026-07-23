# -*- coding: utf-8 -*-
import unittest
from sort_timelines import extract_date

class TestExtractDate(unittest.TestCase):
    def check(self, time_str, expected):
        self.assertAlmostEqual(extract_date(time_str), expected, places=2, msg=f"Failed on: {time_str}")

    def test_vietnamese_formats(self):
        self.check("01/01/1201", 1201.07)
        self.check("Đầu 1994", 1994.14)
        self.check("Thế kỷ XIII", 1201.07)
        self.check("Khoảng giữa thế kỷ XIV", 1301.43)
        self.check("Khoảng thế kỷ XIV", 1301.07)
        self.check("Đầu 1425 (25/01 năm Ất Tỵ)", 1425.14)
        self.check("Đầu 1423 (24/12 năm Nhâm Dần)", 1423.14)
        self.check("Rằm tháng 8/1773", 1773.56)
        self.check("Trung tuần tháng 9/1773", 1773.63)
        self.check("Mùa Đông 1773", 1773.78)
        self.check("Đầu năm 1774", 1774.14)
        self.check("Tháng 5 âm lịch năm 1801", 1801.33)
        self.check("1890 - 1898", 1890.0)
        self.check("Cuối năm 1947", 1947.78)
        self.check("25/12/1950 - 18/01/1951", 1950.85)
        self.check("Mùa khô 1966-1967", 1966.78)
        self.check("Tháng 01/1967", 1967.07)
        self.check("06/1965 - 09/1966", 1965.4)
        self.check("Những năm 1970", 1970.0)
        self.check("08/02 - 24/03/1971", 1971.15)
        self.check("Giữa năm 1972", 1972.43)
        self.check("02/1979", 1979.13)
        self.check("Tháng 5/2000 - 22/12/2001", 2000.33)
        self.check("18/01 - 28/02/1077", 1077.10)
        self.check("Khoảng 1.100 - 700 TCN", -1100.0)
        self.check("Khoảng 1.000 TCN - 200 SCN", -1000.0)
        self.check("Khoảng 23.500 TCN (25.510 năm trước)", -23500.0)
        self.check("Khoảng 534.000 - 400.000 năm trước", -534000.0)

    def test_english_formats(self):
        self.check("01/01/1201", 1201.07)
        self.check("Early 1994", 1994.14)
        self.check("13th Century", 1201.07)
        self.check("Mid-14th Century", 1301.43)
        self.check("14th Century", 1301.07)
        self.check("Early 1425 (Jan 25, Year of At Ty)", 1425.14)
        self.check("Early 1423 (Dec 24, Year of Nham Dan)", 1423.14)
        self.check("15th of 8th Lunar Month 1773", 1773.56)
        self.check("Mid-September 1773", 1773.63)
        self.check("Winter 1773", 1773.78)
        self.check("Early 1774", 1774.14)
        self.check("5th Lunar Month 1801", 1801.33)
        self.check("Late 1947", 1947.78)
        self.check("Dry season 1966-1967", 1966.78)
        self.check("Jan 1967", 1967.07)
        self.check("1970s", 1970.0)
        self.check("Mid 1972", 1972.43)
        self.check("Approximately 1,100 - 700 BC", -1100.0)
        self.check("Approximately 1,000 BC - 200 AD", -1000.0)
        self.check("Approximately 23,500 BC (25,510 years ago)", -23500.0)
        self.check("Approximately 534,000 - 400,000 years ago", -534000.0)
        # New English date format tests
        self.check("Aug. 19, 980:", 980.57)
        self.check("Jan. 19 - 20, 1785:", 1785.10)
        self.check("Night of Sep. 22-23, 1945:", 1945.64)
        self.check("Apr. 11 - 12, 1884:", 1884.29)
        self.check("Dec. 25, 1950 - Jan. 18, 1951:", 1950.85)

    def test_chronological_ordering(self):
        go_mun = extract_date("Khoảng 1.100 - 700 TCN")
        sa_huynh = extract_date("Khoảng 1.000 TCN - 200 SCN")
        self.assertLess(go_mun, sa_huynh, "Gò Mun (1.100 - 700 TCN) must be ordered before Sa Huỳnh (1.000 TCN - 200 SCN)")
        
        d1201 = extract_date("01/01/1201")
        century13 = extract_date("Thế kỷ XIII")
        d1226 = extract_date("10/01/1226")
        self.assertEqual(d1201, century13, "01/01/1201 and generic 13th Century date both map to start of 13th century (1201)")
        self.assertLess(century13, d1226, "Thế kỷ XIII (starts in 1201) must be ordered before 10/01/1226")

    def test_timeline_integrity_and_sorting(self):
        from sort_timelines import parse_blocks
        for filename in ["timelines_vi.md", "timelines_en.md"]:
            with open(filename, "r", encoding="utf-8") as f:
                original_lines = f.readlines()

            blocks = parse_blocks(filename)
            reconstructed_lines = []
            for b in blocks:
                reconstructed_lines.extend(b['lines'])

            self.assertEqual(len(original_lines), len(reconstructed_lines),
                             f"Line count mismatch in {filename} after parsing blocks!")
            self.assertEqual(original_lines, reconstructed_lines,
                             f"Reconstructed lines do not match original lines in {filename}!")

            # Verify event date ordering within each section
            sections = []
            curr = []
            for b in blocks:
                if b['type'] == 'header':
                    if curr: sections.append(curr)
                    curr = [b]
                else:
                    curr.append(b)
            if curr: sections.append(curr)

            for sec in sections:
                hdr = sec[0]['lines'][0].strip() if sec[0]['type'] == 'header' else 'Top'
                events = [b for b in sec if b['type'] == 'event']
                for i in range(len(events) - 1):
                    t1, t2 = events[i]['time_str'], events[i+1]['time_str']
                    d1, d2 = extract_date(t1), extract_date(t2)
                    self.assertLessEqual(d1, d2,
                        f"In {filename} section [{hdr}]: '{t1}' (date {d1}) must be <= '{t2}' (date {d2})")


if __name__ == '__main__':
    unittest.main()


