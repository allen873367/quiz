"""
Update all CSV files in 資料結構題目/:
1. Convert from tab-delimited to comma-delimited
2. Add columns: 連貫題組別, 自編題目, 題目來源
3. Mark all sequential question groups
"""
import os, csv, io

CSV_DIR = '資料結構題目'

# Sequential question group definitions
SEQUENCE_GROUPS = {
    'ch02_time_complexity.csv': {
        'time_analysis':     [12, 13, 14, 15],
        'big_o_definition':  [17, 18, 19],
    },
    'ch04_array.csv': {
        'matrix_storage_1':  [7, 8],
        'matrix_storage_2':  [9, 10],
    },
    'ch11_graph.csv': {
        'graph_search':      [6, 7],
        'euler_hamiltonian': [19, 20],
    },
}

def build_q2group_map(filename):
    groups = SEQUENCE_GROUPS.get(filename, {})
    q2g = {}
    for gname, qnums in groups.items():
        for qn in qnums:
            q2g[qn] = gname
    return q2g

def fix_csv(filepath, q2g):
    with open(filepath, 'rb') as f:
        raw_bytes = f.read()
    # Strip initial BOM(s) - handle double BOM from previous bad runs
    while raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]
    # Also strip embedded BOM character if present
    raw = raw_bytes.decode('utf-8')
    if raw and raw[0] == '﻿':
        raw = raw[1:]

    first_line = raw.split('\n')[0].rstrip('\r')
    delimiter = '\t' if '\t' in first_line else ','

    reader = csv.DictReader(io.StringIO(raw), delimiter=delimiter)
    fieldnames = list(reader.fieldnames)

    # These are the Chinese column names to add (traditional Chinese)
    new_cols = ['連貫題組別', '自編題目', '題目來源']
    for col in new_cols:
        if col not in fieldnames:
            fieldnames.append(col)

    rows = []
    for row in reader:
        qnum_str = str(row.get('題號', '')).strip()
        qnum = int(qnum_str) if qnum_str.isdigit() else 0

        if qnum in q2g:
            row['連貫題組別'] = q2g[qnum]
        else:
            row.setdefault('連貫題組別', '')

        row.setdefault('自編題目', '')
        row.setdefault('題目來源', '')

        rows.append(row)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

    with open(filepath, 'wb') as f:
        f.write(output.getvalue().encode('utf-8-sig'))

    print(f'  OK {os.path.basename(filepath)} ({len(rows)} qs, {len(q2g)} in groups)')

def main():
    csv_files = sorted(
        f for f in os.listdir(CSV_DIR)
        if f.endswith('.csv') and 'export' not in f.lower()
    )
    for fname in csv_files:
        path = os.path.join(CSV_DIR, fname)
        q2g = build_q2group_map(fname)
        fix_csv(path, q2g)

    print('\nSequential groups:')
    for fname, groups in sorted(SEQUENCE_GROUPS.items()):
        print(f'  {fname}:')
        for gname, qnums in groups.items():
            print(f'    [{gname}] Q{qnums[0]}-Q{qnums[-1]}')

if __name__ == '__main__':
    main()
