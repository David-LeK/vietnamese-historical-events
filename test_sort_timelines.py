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
        # Additional English date format tests
        self.check("Aug. 19, 980:", 980.57)
        self.check("Jan. 19 - 20, 1785:", 1785.10)
        self.check("Night of Sep. 22-23, 1945:", 1945.64)
        self.check("Apr. 11 - 12, 1884:", 1884.29)
        self.check("Dec. 25, 1950 - Jan. 18, 1951:", 1950.85)
        self.check("Mid-17th Century (approx. 1653 - 1657)", 1653.0)
        self.check("Jun. - Oct. 1949", 1949.40)
        self.check("Feb. - Aug. 1677", 1677.13)
        self.check("Oct. 1884 - Mar. 3, 1885", 1884.67)

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
            self.assertEqual(sorted(original_lines), sorted(reconstructed_lines),
                             f"Multiset of lines altered in {filename}!")

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
                        f"In {filename} section [{hdr}]: '{t1}' (date {d1:.4f}) must be <= '{t2}' (date {d2:.4f})")

    def test_cross_period_sorting(self):
        from sort_timelines import parse_blocks, sort_timelines
        # Run cross-period sorting
        sort_timelines("timelines_vi.md", "timelines_en.md", across_periods=True)

        for filename in ["timelines_vi.md", "timelines_en.md"]:
            blocks = parse_blocks(filename)
            sections = []
            curr = []
            for b in blocks:
                if b['type'] == 'header':
                    if curr: sections.append(curr)
                    curr = [b]
                else:
                    curr.append(b)
            if curr: sections.append(curr)

            section_event_dates = []
            for sec in sections:
                hdr = sec[0]['lines'][0].strip() if sec[0]['type'] == 'header' else 'Top'
                events = [b for b in sec if b['type'] == 'event']
                dates = [extract_date(e['time_str']) for e in events]
                
                # Check intra-section order
                for i in range(len(dates) - 1):
                    self.assertLessEqual(dates[i], dates[i+1],
                        f"In {filename} section [{hdr}]: '{events[i]['time_str']}' ({dates[i]:.4f}) > '{events[i+1]['time_str']}' ({dates[i+1]:.4f})")
                if dates:
                    section_event_dates.append(dates)

            # Check inter-section global chronological order
            for i in range(len(section_event_dates) - 1):
                d_max_prev = max(section_event_dates[i])
                d_min_next = min(section_event_dates[i+1])
                self.assertLessEqual(d_max_prev, d_min_next,
                    f"In {filename}: Section {i} max date ({d_max_prev:.4f}) exceeds Section {i+1} min date ({d_min_next:.4f})")

    def test_line_by_line_alignment(self):
        with open("timelines_vi.md", "r", encoding="utf-8") as f:
            lines_vi = f.readlines()
        with open("timelines_en.md", "r", encoding="utf-8") as f:
            lines_en = f.readlines()

        self.assertEqual(len(lines_vi), len(lines_en), "Line count mismatch between VI and EN files!")

        for idx in range(len(lines_vi)):
            l_vi = lines_vi[idx].strip()
            l_en = lines_en[idx].strip()

            is_header_vi = l_vi.startswith("#")
            is_header_en = l_en.startswith("#")
            self.assertEqual(is_header_vi, is_header_en,
                             f"Header mismatch at line {idx+1}: VI '{l_vi[:40]}' vs EN '{l_en[:40]}'")

            is_event_vi = l_vi.startswith("*")
            is_event_en = l_en.startswith("*")
            self.assertEqual(is_event_vi, is_event_en,
                             f"Event bullet mismatch at line {idx+1}: VI '{l_vi[:40]}' vs EN '{l_en[:40]}'")

            is_empty_vi = (l_vi == "")
            is_empty_en = (l_en == "")
            self.assertEqual(is_empty_vi, is_empty_en,
                             f"Empty line mismatch at line {idx+1}")

    def test_diff_synchronization_after_sort(self):
        import subprocess
        from sort_timelines import sort_timelines

        # Run sort_timelines
        sort_timelines("timelines_vi.md", "timelines_en.md", across_periods=True)

        def get_changed_lines(target_file):
            try:
                out = subprocess.check_output(["git", "diff", "-U0", target_file], encoding="utf-8")
            except Exception:
                return []
            lines = []
            for line in out.splitlines():
                if line.startswith("@@"):
                    parts = line.split()[2].lstrip("+")
                    if "," in parts:
                        start, count = map(int, parts.split(","))
                        if count <= 1:
                            lines.append(f"{start}")
                        else:
                            lines.append(f"{start}->{start+count-1}")
                    else:
                        lines.append(parts)
            return lines

        vi_lines = get_changed_lines("timelines_vi.md")
        en_lines = get_changed_lines("timelines_en.md")
        self.assertEqual(vi_lines, en_lines,
                         f"Diff line mismatch after sort_timelines!\nVI diff lines: {vi_lines}\nEN diff lines: {en_lines}")


if __name__ == '__main__':
    unittest.main()




