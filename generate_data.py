import os
import re
import json
import sort_timelines

def parse_md_file(filepath):

    sections = []
    current_sec = None
    current_event = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            l = line.strip()
            if not l:
                continue
            if not line.startswith((' ', '\t')):
                if l.startswith('###'):
                    sec_name = l.replace('###', '').replace('**', '').strip()
                    current_sec = {'title': sec_name, 'events': []}
                    sections.append(current_sec)
                elif l.startswith('*'):
                    m = re.match(r'^\*\s+\*\*(.*?)\*\*:?\s*(.*)', l)
                    if m and current_sec is not None:
                        date_str = m.group(1).strip()
                        desc = m.group(2).strip()
                        if date_str.endswith(':'):
                            date_str = date_str[:-1].strip()
                        current_event = {
                            'dateStr': date_str,
                            'desc': desc,
                            'subItems': []
                        }
                        current_sec['events'].append(current_event)
            else:
                if l.startswith('*') and current_event is not None:
                    sub_text = re.sub(r'^\*\s*', '', l).strip()
                    current_event['subItems'].append(sub_text)
    return sections

def extract_date_info(date_str_en, date_str_vi):
    # Determine year, month, day, isBC, yearEnd
    d = date_str_en + ' ' + date_str_vi
    
    is_bc = bool(re.search(r'\b(BC|TCN)\b', d, re.IGNORECASE))
    
    months_en = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    month = None
    day = None
    year = None
    year_end = None
    
    # Check day/month/year patterns like October 17, 503 or 17/10/503
    m_slash = re.search(r'(\d{1,2})/(\d{1,2})/(\d{3,4})', date_str_vi)
    if m_slash:
        day = int(m_slash.group(1))
        month = int(m_slash.group(2))
        year = int(m_slash.group(3))
    else:
        # Check English Month Day, Year
        m_en_full = re.search(r'([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{1,4})', date_str_en, re.IGNORECASE)
        if m_en_full and m_en_full.group(1).lower() in months_en:
            month = months_en[m_en_full.group(1).lower()]
            day = int(m_en_full.group(2))
            year = int(m_en_full.group(3))
        else:
            # Check month/year like 09/1945 or Sep. 1945
            m_m_y = re.search(r'(\d{1,2})/(\d{3,4})', date_str_vi)
            if m_m_y:
                month = int(m_m_y.group(1))
                year = int(m_m_y.group(2))
            else:
                m_en_m_y = re.search(r'([A-Za-z]+)\.?\s+(\d{3,4})', date_str_en)
                if m_en_m_y and m_en_m_y.group(1).lower() in months_en:
                    month = months_en[m_en_m_y.group(1).lower()]
                    year = int(m_en_m_y.group(2))

    # If year is still None, extract first standalone year or year range
    if year is None:
        # Look for year ranges like 1945 - 1954 or 2879 - 258 BC
        m_range = re.search(r'(\d{1,6})\s*-\s*(\d{1,6})\s*(BC|TCN)?', d, re.IGNORECASE)
        if m_range:
            year = int(m_range.group(1))
            year_end = int(m_range.group(2))
        else:
            m_yr = re.search(r'(\d{1,6})', date_str_en)
            if m_yr:
                year = int(m_yr.group(1))
                
    if is_bc and year is not None:
        year = -abs(year)
        if year_end is not None:
            year_end = -abs(year_end)

    return {
        'year': year,
        'yearEnd': year_end,
        'month': month,
        'day': day,
        'isBC': is_bc
    }

def main():
    sort_timelines.sort_timelines('timelines_vi.md', 'timelines_en.md', across_periods=True)
    sec_en = parse_md_file('timelines_en.md')
    sec_vi = parse_md_file('timelines_vi.md')
    
    print(f"EN sections: {len(sec_en)}, VI sections: {len(sec_vi)}")
    
    eras = []
    events = []
    event_id = 1
    
    for i in range(len(sec_en)):
        title_en = sec_en[i]['title']
        title_vi = sec_vi[i]['title'] if i < len(sec_vi) else title_en
        
        eras.append({
            'index': i,
            'titleEn': title_en,
            'titleVi': title_vi
        })
        
        events_en = sec_en[i]['events']
        events_vi = sec_vi[i]['events'] if i < len(sec_vi) else []
        
        for j in range(len(events_en)):
            ev_en = events_en[j]
            ev_vi = events_vi[j] if j < len(events_vi) else {'dateStr': ev_en['dateStr'], 'desc': ev_en['desc'], 'subItems': ev_en['subItems']}
            
            d_info = extract_date_info(ev_en['dateStr'], ev_vi['dateStr'])
            
            events.append({
                'id': event_id,
                'eraIndex': i,
                'dateEn': ev_en['dateStr'],
                'dateVi': ev_vi['dateStr'],
                'descEn': ev_en['desc'],
                'descVi': ev_vi['desc'],
                'subsEn': ev_en['subItems'],
                'subsVi': ev_vi['subItems'],
                'year': d_info['year'],
                'yearEnd': d_info['yearEnd'],
                'month': d_info['month'],
                'day': d_info['day'],
                'isBC': d_info['isBC']
            })
            event_id += 1

    print(f"Total events parsed: {len(events)}")
    
    data_js = f"window.TIMELINE_ERAS = {json.dumps(eras, ensure_ascii=False, indent=2)};\n"
    data_js += f"window.TIMELINE_EVENTS = {json.dumps(events, ensure_ascii=False, indent=None)};\n"
    
    with open('timelines_data.js', 'w', encoding='utf-8') as f:
        f.write(data_js)
    print("Saved timelines_data.js successfully!")

if __name__ == '__main__':
    main()
