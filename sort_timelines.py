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
    time_str = time_str_orig.upper()
    
    m_val = 0
    d_val = 0
    
    if "CUỐI" in time_str or "LATE" in time_str:
        m_val = 11
    elif "ĐẦU" in time_str or "EARLY" in time_str:
        m_val = 2
    elif "GIỮA" in time_str or "MID" in time_str:
        m_val = 6
        
    is_bc = "TCN" in time_str or "BC" in time_str
    
    if "NĂM TRƯỚC" in time_str or "YEARS AGO" in time_str:
        nums = re.findall(r'\d+(?:\.\d+)?(?:,\d+)?', time_str)
        if nums:
            val = float(nums[0].replace('.', '').replace(',', ''))
            val = val - (m_val / 15.0 + d_val / 500.0)
            return -val
            
    if "THẾ KỶ" in time_str or "CENTURY" in time_str or "CENTURIES" in time_str:
        romans = re.findall(r'\b[IVXLCDM]+\b', time_str)
        if romans:
            y = roman_to_int(romans[0]) * 100
        else:
            nums = re.findall(r'\d+', time_str)
            y = int(nums[0]) * 100 if nums else 0
        if is_bc:
            if m_val == 11: 
                y -= 90 
            elif m_val == 2:
                y -= 10 
            elif m_val == 6:
                y -= 50
            return -y
        else:
            return y + m_val/15.0

    if "THIÊN NIÊN KỶ" in time_str or "MILLENNIUM" in time_str:
        romans = re.findall(r'\b[IVXLCDM]+\b', time_str)
        if romans:
            y = roman_to_int(romans[0]) * 1000
        else:
            nums = re.findall(r'\d+', time_str)
            y = int(nums[0]) * 1000 if nums else 0
        if is_bc:
            if m_val == 11:
                y -= 900
            elif m_val == 2:
                y -= 100
            elif m_val == 6:
                y -= 500
            return -y
        else:
            return y + m_val/15.0
            
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    # DD/MM - DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})\s*-\s*(\d{1,2})/(\d{1,2})/(\d{2,4})', time_str)
    if match:
        d1, m1, d2, m2, y = match.groups()
        m_val = int(m1)
        d_val = int(d1)
        val = int(y) + m_val/15.0 + d_val/500.0
        return -val if is_bc else val
        
    # MM - MM/YYYY
    match = re.search(r'(\d{1,2})\s*-\s*(\d{1,2})/(\d{2,4})', time_str)
    if match:
        m1, m2, y = match.groups()
        m_val = int(m1)
        val = int(y) + m_val/15.0
        return -val if is_bc else val

    # Check for Month DD, YYYY or Month DD YYYY
    match = re.search(r'([A-Z]{3,})\.?\s+(\d{1,2}),?\s+(\d{2,4})', time_str)
    if match:
        m_str, d, y = match.groups()
        for i, m in enumerate(months):
            if m in m_str:
                m_val = i + 1
                break
        d_val = int(d)
        val = int(y) + m_val/15.0 + d_val/500.0
        return -val if is_bc else val

    # Check for Month YYYY
    match = re.search(r'([A-Z]{3,})\.?\s+(\d{2,4})', time_str)
    if match:
        m_str, y = match.groups()
        for i, m in enumerate(months):
            if m in m_str:
                m_val = i + 1
                break
        val = int(y) + m_val/15.0
        return -val if is_bc else val

    # DD/MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', time_str)
    if match:
        d, m, y = match.groups()
        m_val = int(m)
        d_val = int(d)
        val = int(y) + m_val/15.0 + d_val/500.0
        return -val if is_bc else val
        
    # MM/YYYY
    match = re.search(r'(\d{1,2})/(\d{2,4})', time_str)
    if match:
        m, y = match.groups()
        m_val = int(m)
        val = int(y) + m_val/15.0
        return -val if is_bc else val

    # Plain year with possible named month
    if m_val == 0:
        for i, m in enumerate(months):
            if m in time_str:
                m_val = i + 1
                break

    nums = re.findall(r'\d+(?:\.\d+)?(?:,\d+)?', time_str)
    if nums:
        val_str = nums[0].replace('.', '').replace(',', '')
        y = int(val_str)
        val = y + m_val/15.0
        return -val if is_bc else val
        
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
