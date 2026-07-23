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

    # Check for Month DD, YYYY or Month DD YYYY
    month_regex = r'\b(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)[A-Z]*\b'
    match = re.search(rf'({month_regex})\.?\s+(\d{1,2}),?\s+(\d{2,4})(?!\d)', time_str)
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
    match = re.search(rf'({month_regex})\.?\s+(\d{2,4})(?!\d)', time_str)
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
        elif re.match(r'^\*\s+\*\*.*?\*\*', line):
            if current_block:
                blocks.append(current_block)
            match = re.match(r'^\*\s+\*\*(.*?)\*\*', line)
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


def sort_file(filename):
    print(f"Processing {filename}...")
    blocks = parse_blocks(filename)
    
    sections = []
    current_section = []
    for b in blocks:
        if b['type'] == 'header':
            if current_section:
                sections.append(current_section)
            current_section = [b]
        else:
            current_section.append(b)
            
    if current_section:
        sections.append(current_section)
        
    new_blocks = []
    for section in sections:
        events = [b for b in section if b['type'] == 'event']
        if events:
            events_sorted = sorted(events, key=lambda b: extract_date(b['time_str']))
            
            event_idx = 0
            for i, b in enumerate(section):
                if b['type'] == 'event':
                    section[i] = events_sorted[event_idx]
                    event_idx += 1
                    
        new_blocks.extend(section)
        
    with open(filename, "w", encoding="utf-8") as f:
        for b in new_blocks:
            f.writelines(b['lines'])
            
    print(f"Finished sorting {filename}.")

if __name__ == "__main__":
    sort_file("timelines_en.md")
    sort_file("timelines_vi.md")
