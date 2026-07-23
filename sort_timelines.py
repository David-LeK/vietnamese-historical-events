import re
import sys

def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

def extract_date(time_str_orig):
    # Pre-check: if parentheses contain an explicit approx year e.g. (approx. 1653 - 1657) or (approx. 1653)
    # use that explicit year if present, otherwise strip parentheses.
    time_str_check = time_str_orig.strip()
    approx_match = re.search(r'\(\s*(?:approx\.?|khoảng)\s*(\d{3,4})', time_str_check, re.IGNORECASE)
    if approx_match and ("CENTURY" in time_str_check.upper() or "THẾ KỶ" in time_str_check.upper()):
        y_val = int(approx_match.group(1))
        return float(y_val)

    # Remove contents in parentheses for main date extraction 
    # to avoid falsely matching lunar dates like (25/01 năm Ất Tỵ)
    time_str = re.sub(r'\(.*?\)', '', time_str_orig).strip().upper()
    time_str = re.sub(r'\b\d{1,3}(?:[.,]\d{3})+\b', lambda m: m.group(0).replace('.', '').replace(',', ''), time_str)
    
    m_val = 0
    d_val = 0
    default_m_val = 0
    default_d_val = 0
    
    if "CUỐI" in time_str or "LATE" in time_str or "MÙA ĐÔNG" in time_str or "WINTER" in time_str or "MÙA KHÔ" in time_str or "DRY SEASON" in time_str:
        default_m_val = 11
        default_d_val = 25
    elif "ĐẦU" in time_str or "EARLY" in time_str or "MÙA XUÂN" in time_str or "SPRING" in time_str:
        default_m_val = 2
        default_d_val = 5
    elif "GIỮA" in time_str or "MID" in time_str or "MÙA HÈ" in time_str or "SUMMER" in time_str or "MÙA THU" in time_str or "AUTUMN" in time_str:
        default_m_val = 6
        default_d_val = 15
        
    if "RẰM" in time_str or "TRUNG TUẦN" in time_str or "15TH" in time_str:
        d_val = 15
        
    is_bc = "TCN" in time_str or "BC" in time_str
    
    strict_roman_regex = r'\b(?=[MDCLXVI])M*(?:C[MD]|D?C{0,3})(?:X[CL]|L?X{0,3})(?:I[XV]|V?I{0,3})\b'
    
    def finalize_val(y_val):
        nonlocal m_val, d_val
        if m_val == 0: m_val = default_m_val
        if d_val == 0: d_val = default_d_val
        val = y_val + m_val/15.0 + d_val/500.0
        return -val if is_bc else val

    if "NĂM TRƯỚC" in time_str or "YEARS AGO" in time_str:
        nums = re.findall(r'\d+(?:\.\d+)?(?:,\d+)?', time_str)
        if nums:
            val = float(nums[0].replace('.', '').replace(',', ''))
            val = val - (default_m_val / 15.0 + default_d_val / 500.0)
            return -val
            
    if "THẾ KỶ" in time_str or "CENTURY" in time_str or "CENTURIES" in time_str:
        romans = re.findall(strict_roman_regex, time_str)
        romans = [r for r in romans if r]
        if romans:
            c_num = roman_to_int(romans[0])
        else:
            nums = re.findall(r'\d+', time_str)
            c_num = int(nums[0]) if nums else 0
        if is_bc:
            y = c_num * 100
            if default_m_val == 11: 
                y -= 90 
            elif default_m_val == 2:
                y -= 10 
            elif default_m_val == 6:
                y -= 50
            return -y
        else:
            y = (c_num - 1) * 100 + 1 if c_num > 0 else 0
            m = default_m_val if default_m_val > 0 else 1
            d = default_d_val if default_d_val > 0 else 1
            return y + m/15.0 + d/500.0

    if "THIÊN NIÊN KỶ" in time_str or "MILLENNIUM" in time_str:
        romans = re.findall(strict_roman_regex, time_str)
        romans = [r for r in romans if r]
        if romans:
            m_num = roman_to_int(romans[0])
        else:
            nums = re.findall(r'\d+', time_str)
            m_num = int(nums[0]) if nums else 0
        if is_bc:
            y = m_num * 1000
            if default_m_val == 11:
                y -= 900
            elif default_m_val == 2:
                y -= 100
            elif default_m_val == 6:
                y -= 500
            return -y
        else:
            y = (m_num - 1) * 1000 + 1 if m_num > 0 else 0
            m = default_m_val if default_m_val > 0 else 1
            d = default_d_val if default_d_val > 0 else 1
            return y + m/15.0 + d/500.0
            
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month_regex = r'\b(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]*\b'

    # Range format: Month1 DD1, YYYY1 - Month2 DD2, YYYY2 (e.g. Dec. 25, 1950 - Jan. 18, 1951)
    match = re.search(rf'({month_regex})\.?\s+(\d{{1,2}}),?\s+(\d{{2,4}})\s*-\s*({month_regex})\.?\s+(\d{{1,2}}),?\s+(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str1, d1, y1, m_str2, d2, y2 = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str1:
                    m_val = i + 1
                    break
        if d_val == 0: d_val = int(d1)
        return finalize_val(int(y1))

    # Range format: Month1 DD1 - Month2 DD2, YYYY (e.g. Jan. 18 - Feb. 28, 1077)
    match = re.search(rf'({month_regex})\.?\s+(\d{{1,2}})\s*-\s*({month_regex})\.?\s+(\d{{1,2}}),?\s+(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str1, d1, m_str2, d2, y = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str1:
                    m_val = i + 1
                    break
        if d_val == 0: d_val = int(d1)
        return finalize_val(int(y))

    # Range format: Month1 YYYY1 - Month2 (DD2, )YYYY2 (e.g. Oct. 1884 - Mar. 3, 1885)
    match = re.search(rf'({month_regex})\.?\s+(\d{{2,4}})\s*-\s*({month_regex})\.?\s+(?:\d{{1,2}},?\s+)?(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str1, y1, m_str2, y2 = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str1:
                    m_val = i + 1
                    break
        return finalize_val(int(y1))

    # Range format: Month1 - Month2 YYYY (e.g. Feb. - Aug. 1677, Jun. - Oct. 1949)
    match = re.search(rf'({month_regex})\.?\s*-\s*({month_regex})\.?\s+(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str1, m_str2, y = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str1:
                    m_val = i + 1
                    break
        return finalize_val(int(y))

    # Range formats: DD/MM/YYYY - DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})\s*-\s*\d{1,2}/\d{1,2}/\d{2,4}', time_str)
    if match:
        d, m, y = match.groups()
        if m_val == 0: m_val = int(m)
        if d_val == 0: d_val = int(d)
        return finalize_val(int(y))

    # Range formats: MM/YYYY - MM/YYYY or DD/MM - DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,4})\s*-\s*\d{1,2}/(?:\d{1,2}/)?(\d{2,4})', time_str)
    if match:
        m1, y1_or_m1, y = match.groups()
        # if the second group is 4 digits, it's a year. e.g. 05/2000 - 12/2001
        if len(y1_or_m1) >= 4:
            if m_val == 0: m_val = int(m1)
            return finalize_val(int(y1_or_m1))
        else: # e.g. 18/01 - 28/02/1077 (DD/MM - DD/MM/YYYY)
            if d_val == 0: d_val = int(m1)
            if m_val == 0: m_val = int(y1_or_m1)
            return finalize_val(int(y))

    # Range formats: YYYY - YYYY
    match = re.search(r'\b(\d{2,6})\s*-\s*\d{2,6}\b', time_str)
    if match and len(match.group(1)) > 2:
        y = match.group(1)
        return finalize_val(int(y))
        
    # DD-DD/MM/YYYY
    match = re.search(r'(\d{1,2})\s*-\s*(\d{1,2})/(\d{1,2})/(\d{2,4})(?!\d)', time_str)
    if match:
        d1, d2, m, y = match.groups()
        if m_val == 0: m_val = int(m)
        if d_val == 0: d_val = int(d1)
        return finalize_val(int(y))
        
    # MM - MM/YYYY
    match = re.search(r'(\d{1,2})\s*-\s*(\d{1,2})/(\d{2,4})(?!\d)', time_str)
    if match:
        m1, m2, y = match.groups()
        if m_val == 0: m_val = int(m1)
        return finalize_val(int(y))

    # Month DD - DD, YYYY or Month DD-DD, YYYY (e.g. Jan. 19 - 20, 1785, Night of Sep. 22-23, 1945)
    match_range = re.search(rf'({month_regex})\.?\s+(\d{{1,2}})\s*-\s*\d{{1,2}},?\s+(\d{{2,4}})(?!\d)', time_str)
    if match_range:
        m_str, d, y = match_range.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str:
                    m_val = i + 1
                    break
        if d_val == 0: d_val = int(d)
        return finalize_val(int(y))

    # Check for Month DD, YYYY or Month DD YYYY
    match = re.search(rf'({month_regex})\.?\s+(\d{{1,2}}),?\s+(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str, d, y = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str:
                    m_val = i + 1
                    break
        if d_val == 0: d_val = int(d)
        return finalize_val(int(y))

    # Check for Month YYYY
    match = re.search(rf'({month_regex})\.?\s+(\d{{2,4}})(?!\d)', time_str)
    if match:
        m_str, y = match.groups()
        if m_val == 0:
            for i, m in enumerate(months):
                if m in m_str:
                    m_val = i + 1
                    break
        return finalize_val(int(y))

    # 1. THÁNG X NĂM YYYY
    match1 = re.search(r'(?:THÁNG|MONTH)\s+(\d{1,2})\b.*?(?:NĂM|YEAR)\s*(\d{2,4})\b', time_str)
    # 2. XTH LUNAR MONTH YYYY
    match2 = re.search(r'(\d{1,2})(?:TH|ST|ND|RD)?\s*(?:LUNAR)?\s*(?:THÁNG|MONTH)\s*(?:NĂM|YEAR)?\s*(\d{2,4})\b', time_str)
    # 3. THÁNG X/YYYY
    match3 = re.search(r'(?:THÁNG|MONTH)\s+(\d{1,2})\b.*?(\d{2,4})\b', time_str)
    
    if match1:
        m, y = match1.groups()
        if m_val == 0: m_val = int(m)
        return finalize_val(int(y))
    elif match2:
        m, y = match2.groups()
        if m_val == 0: m_val = int(m)
        return finalize_val(int(y))
    elif match3:
        m, y = match3.groups()
        if m_val == 0: m_val = int(m)
        return finalize_val(int(y))

    # DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})(?!\d)', time_str)
    if match:
        d, m, y = match.groups()
        if m_val == 0: m_val = int(m)
        if d_val == 0: d_val = int(d)
        return finalize_val(int(y))
        
    # MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{2,4})(?!\d)', time_str)
    if match:
        m, y = match.groups()
        if m_val == 0: m_val = int(m)
        return finalize_val(int(y))

    # Plain year with possible named month
    if m_val == 0:
        for i, m in enumerate(months):
            if m in time_str:
                m_val = i + 1
                break

    nums = re.findall(r'\b\d+(?:\.\d+)?(?:,\d+)?[S]?\b', time_str)
    if nums:
        # Get the first 4-digit number, otherwise just the first number
        four_digit_nums = [n for n in nums if len(n.replace('.', '').replace(',', '').replace('S', '')) >= 4]
        val_str = four_digit_nums[0] if four_digit_nums else nums[-1]
        y = int(val_str.replace('.', '').replace(',', '').replace('S', ''))
        return finalize_val(y)
        
    return 0

def parse_blocks(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    blocks = []
    current_block = None
    
    for line in lines:
        if line.strip().startswith('#'):
            if current_block:
                blocks.append(current_block)
            blocks.append({'type': 'header', 'lines': [line]})
            current_block = None
        elif re.match(r'^\*\s+\*\*(.*?):\*\*', line):
            if current_block:
                blocks.append(current_block)
            match = re.match(r'^\*\s+\*\*(.*?):\*\*', line)
            time_str = match.group(1) if match else ""
            current_block = {'type': 'event', 'time_str': time_str, 'lines': [line]}
        elif line.strip() == '':
            if current_block:
                blocks.append(current_block)
                current_block = None
            blocks.append({'type': 'empty', 'lines': [line]})
        else:
            if current_block and current_block['type'] == 'event':
                current_block['lines'].append(line)
            else:
                if current_block:
                    current_block['lines'].append(line)
                else:
                    current_block = {'type': 'text', 'lines': [line]}
                    
    if current_block:
        blocks.append(current_block)
        
    return blocks


SECTION_THRESHOLDS = [
    -800.0,      # 0 -> 1: Tiền sử / Bắc thuộc (Trước năm 800 TCN)
    938.9,       # 1 -> 2: Bắc thuộc / Độc lập (800 TCN - 938)
    1008.9,      # 2 -> 3: Triều Lý (939 - 1009)
    1225.99,     # 3 -> 4: Triều Trần (1009 - 1225)
    1399.9,      # 4 -> 5: Nhà Hồ (1226 - 1400)
    1407.39,     # 5 -> 6: Bắc thuộc 4 (1400 - 1407)
    1427.99,     # 6 -> 7: Nhà Lê Sơ (1407 - 1427)
    1526.99,     # 7 -> 8: Nhà Mạc (1428 - 1527)
    1592.99,     # 8 -> 9: Phân liệt Đàng Trong - Đàng Ngoài (1527 - 1592)
    1770.99,     # 9 -> 10: Tây Sơn (1593 - 1771)
    1801.99,     # 10 -> 11: Nhà Nguyễn Độc lập (1771 - 1802)
    1857.99,     # 11 -> 12: Pháp xâm lược (1802 - 1858)
    1896.99,     # 12 -> 13: 1897 - 1913
    1913.99,     # 13 -> 14: WWI (1914 - 1918)
    1918.99,     # 14 -> 15: 1919 - 1930
    1930.99,     # 15 -> 16: 1931 - 1935
    1935.99,     # 16 -> 17: 1936 - 1938
    1938.99,     # 17 -> 18: 1939 - 1945
    1945.60,     # 18 -> 19: 09/1945 - 02/1946 (Nam Bộ)
    1946.20,     # 19 -> 20: 03/1946 - 12/1946 (Hòa hoãn)
    1946.99,     # 20 -> 21: 1947 - 1950 (Toàn quốc kháng chiến)
    1950.99,     # 21 -> 22: 1951 - 07/1954 (Cuối kháng chiến chống Pháp)
    1954.55,     # 22 -> 23: 08/1954 - 1960 (Chia cắt)
    1960.99,     # 23 -> 24: 1961 - 1964 (Chống chiến tranh đặc biệt)
    1964.99,     # 24 -> 25: 1965 - 1968 (Chiến tranh cục bộ)
    1968.99,     # 25 -> 26: 1969 - 1972 (Việt Nam hóa)
    1972.99,     # 26 -> 27: 1973 - 04/1975 (Mùa Xuân 1975)
    1975.34,     # 27 -> 28: 05/1975 - 1985 (Hậu chiến, Đổi mới)
    1985.99,     # 28 -> 29: 1986 - 1990 (Đầu Đổi mới)
    1990.99,     # 29 -> 30: 1991 - 1995
    1995.99,     # 30 -> 31: 1996 - 2000
    2000.99,     # 31 -> 32: 2001 - 2005
    2005.99,     # 32 -> 33: 2006 - 2010
    2010.99,     # 33 -> 34: 2011 - 2016
    2016.99,     # 34 -> 35: 2017 - 2020
    2020.99,     # 35 -> 36: 2021-nay
]

def get_section_index(date_val):
    for idx, t in enumerate(SECTION_THRESHOLDS):
        if date_val <= t:
            return idx
    return len(SECTION_THRESHOLDS)

def sort_timelines(vi_filename="timelines_vi.md", en_filename="timelines_en.md", across_periods=True):
    print(f"Synchronized sorting for {vi_filename} and {en_filename} (across_periods={across_periods})...")
    blocks_vi = parse_blocks(vi_filename)
    blocks_en = parse_blocks(en_filename)
    
    assert len(blocks_vi) == len(blocks_en), "Block count mismatch between VI and EN files!"
    
    events_vi = [b for b in blocks_vi if b['type'] == 'event']
    events_en = [b for b in blocks_en if b['type'] == 'event']
    
    # Align true translated pairs for EN where original input had swapped indices
    paired_events_en = list(events_en)
    if len(paired_events_en) >= 625:
        # Swap 525 & 526 in EN if needed to match VI topic alignment
        if 'Ho Phi Long' in paired_events_en[525]['lines'][0] and 'Bà Tấm' in events_vi[525]['lines'][0]:
            paired_events_en[525], paired_events_en[526] = paired_events_en[526], paired_events_en[525]
        # Swap 623 & 624 in EN if needed to match VI topic alignment
        if 'Béhaine' in paired_events_en[623]['lines'][0] and 'Xiêm' in events_vi[623]['lines'][0]:
            paired_events_en[623], paired_events_en[624] = paired_events_en[624], paired_events_en[623]
            
    vi_event_idx = 0
    repaired_blocks_en = []
    for b in blocks_en:
        if b['type'] == 'event':
            repaired_blocks_en.append(paired_events_en[vi_event_idx])
            vi_event_idx += 1
        else:
            repaired_blocks_en.append(b)
            
    sections_vi = []
    sections_en = []
    curr_vi = []
    curr_en = []
    
    for bv, be in zip(blocks_vi, repaired_blocks_en):
        if bv['type'] == 'header':
            if curr_vi:
                sections_vi.append(curr_vi)
                sections_en.append(curr_en)
            curr_vi = [bv]
            curr_en = [be]
        else:
            curr_vi.append(bv)
            curr_en.append(be)
            
    if curr_vi:
        sections_vi.append(curr_vi)
        sections_en.append(curr_en)
        
    sorted_blocks_vi = []
    sorted_blocks_en = []
    
    if across_periods:
        events_zipped = list(zip(events_vi, paired_events_en))
        events_zipped_sorted = sorted(events_zipped, key=lambda pair: extract_date(pair[0]['time_str']))
        
        num_sections = len(sections_vi)
        section_buckets = [[] for _ in range(num_sections)]
        for pair in events_zipped_sorted:
            d = extract_date(pair[0]['time_str'])
            s_idx = get_section_index(d)
            if s_idx >= num_sections:
                s_idx = num_sections - 1
            section_buckets[s_idx].append(pair)
            
        for sec_idx in range(num_sections):
            sec_v = sections_vi[sec_idx]
            sec_e = sections_en[sec_idx]
            
            non_events_v = [b for b in sec_v if b['type'] != 'event']
            non_events_e = [b for b in sec_e if b['type'] != 'event']
            
            # Header block
            sorted_blocks_vi.append(non_events_v[0])
            sorted_blocks_en.append(non_events_e[0])
            
            # Additional text or non-event blocks
            for b_v, b_e in zip(non_events_v[1:], non_events_e[1:]):
                if b_v['type'] == 'text':
                    sorted_blocks_vi.append({'type': 'empty', 'lines': ['\n']})
                    sorted_blocks_en.append({'type': 'empty', 'lines': ['\n']})
                    sorted_blocks_vi.append(b_v)
                    sorted_blocks_en.append(b_e)
                    
            if section_buckets[sec_idx]:
                sorted_blocks_vi.append({'type': 'empty', 'lines': ['\n']})
                sorted_blocks_en.append({'type': 'empty', 'lines': ['\n']})
                
            for pair in section_buckets[sec_idx]:
                sorted_blocks_vi.append(pair[0])
                sorted_blocks_en.append(pair[1])
                
            if sec_idx < num_sections - 1:
                sorted_blocks_vi.append({'type': 'empty', 'lines': ['\n']})
                sorted_blocks_en.append({'type': 'empty', 'lines': ['\n']})
    else:
        for sec_vi, sec_en in zip(sections_vi, sections_en):
            event_indices = [i for i, b in enumerate(sec_vi) if b['type'] == 'event']
            events_zipped = [(sec_vi[i], sec_en[i]) for i in event_indices]
            
            events_zipped_sorted = sorted(events_zipped, key=lambda pair: extract_date(pair[0]['time_str']))
            
            sorted_idx = 0
            for i in range(len(sec_vi)):
                if sec_vi[i]['type'] == 'event':
                    sec_vi[i] = events_zipped_sorted[sorted_idx][0]
                    sec_en[i] = events_zipped_sorted[sorted_idx][1]
                    sorted_idx += 1
                    
            sorted_blocks_vi.extend(sec_vi)
            sorted_blocks_en.extend(sec_en)
            
    with open(vi_filename, "w", encoding="utf-8") as f:
        for b in sorted_blocks_vi:
            f.writelines(b['lines'])
            
    with open(en_filename, "w", encoding="utf-8") as f:
        for b in sorted_blocks_en:
            f.writelines(b['lines'])
            
    print("Finished synchronized sorting.")

def sort_file(filename):
    sort_timelines()

if __name__ == "__main__":
    across = "--by-period" not in sys.argv
    sort_timelines("timelines_vi.md", "timelines_en.md", across_periods=across)


