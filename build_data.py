"""
Build compact aggregated JSON from the source Excel files.
Output: data.json  (embedded into index.html so the page ALWAYS works, offline included)
"""
import pandas as pd, json, warnings, math, glob, os, sys, re
warnings.filterwarnings('ignore')


# ---------------------------------------------------------------------------
# Penyeragaman nama channel
# ---------------------------------------------------------------------------
# Sheet yang berbeda menulis channel yang sama dengan cara berbeda. Kalau tidak
# diseragamkan, satu channel muncul sebagai beberapa baris terpisah di ranking.
#
# Nama baku = penulisan di sheet 'Content Youtube Studio' (20 channel IMG).
# Perbedaan yang hanya soal huruf besar/kecil ditangani otomatis di read();
# tabel di bawah khusus untuk varian yang katanya beda (kata tambahan, jamak, dll).
#
# Cara menambah: tulis kunci dalam HURUF KECIL SEMUA, isinya nama baku.
CANON_CHANNEL = {}   # diisi otomatis dari sheet Youtube Studio

CHANNEL_ALIAS = {
    'radio rdi 97.1 fm jakarta': 'Radio RDI',
    'radio rdi 97.1 fm':         'Radio RDI',
    'rdi 97.1 fm jakarta':       'Radio RDI',
    'inews premium sports':      'iNews Premium Sport',
    'inews jatim official':      'iNews Jatim',
    'inews sumut official':      'iNews Sumut',
    'oke vibes':                 'Okezone Vibes!',
'okezone vibes':             'Okezone Vibes!',
}


def find_file(*keywords):
    """Cari file .xlsx yang namanya mengandung SEMUA kata kunci (abaikan besar/kecil huruf).
    Dibuat begini supaya nama file boleh berubah tiap bulan tanpa mengedit script."""
    for f in sorted(glob.glob('*.xlsx')):
        low = os.path.basename(f).lower()
        if all(k.lower() in low for k in keywords):
            return f
    sys.exit(f"\n[GAGAL] Tidak menemukan file Excel yang mengandung kata: {', '.join(keywords)}\n"
             f"        File .xlsx yang ada di folder ini:\n"
             + ''.join(f'          - {x}\n' for x in sorted(glob.glob('*.xlsx')) or ['(tidak ada sama sekali)']))


def find_sheet(path, *keywords):
    """Cari nama sheet yang mengandung SEMUA kata kunci."""
    names = pd.ExcelFile(path).sheet_names
    for n in names:
        low = str(n).lower()
        if all(k.lower() in low for k in keywords):
            return n
    sys.exit(f"\n[GAGAL] Di file '{path}' tidak ada sheet yang mengandung kata: {', '.join(keywords)}\n"
             f"        Sheet yang tersedia: {names}\n")


AUDIT = {'rename': [], 'unknown': []}   # rekam jejak penyeragaman nama


def read(path, *sheet_keywords, col_is_master=False):
    sheet = find_sheet(path, *sheet_keywords)
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
    # Rapikan spasi di ujung nilai teks (mis. 'tvOneNews ' -> 'tvOneNews'),
    # supaya nama yang sama tidak terhitung sebagai dua kelompok berbeda.
    # (pandas 2.x memakai dtype 'object', pandas 3.x memakai 'str' -> cek keduanya
    #  dengan cara menyingkirkan kolom angka/tanggal saja)
    for c in df.columns:
        if not pd.api.types.is_numeric_dtype(df[c]) and not pd.api.types.is_datetime64_any_dtype(df[c]):
            df[c] = df[c].map(lambda v: v.strip() if isinstance(v, str) else v)

    # ---- Penyeragaman nama channel, tiga lapis ----
    for col in ('Channel', 'Cluster', 'Portal', 'Unit', 'Platform'):
        if col not in df.columns:
            continue
        before = df[col].nunique()
        asli = df[col].tolist()

        # (1) varian kata: 'iNews Premium Sports' -> 'iNews Premium Sport'
        if col == 'Channel':
            df[col] = df[col].map(lambda v: CHANNEL_ALIAS.get(str(v).strip().lower(), v)
                                  if isinstance(v, str) else v)
            # (2) samakan ke nama baku dari sheet Youtube Studio, apa pun kapitalisasinya
            #     ('IDX CHANNEL' -> 'IDX Channel', 'RAKYAT BERSUARA' -> 'Rakyat Bersuara')
            df[col] = df[col].map(lambda v: CANON_CHANNEL.get(str(v).strip().lower(), v)
                                  if isinstance(v, str) else v)

        # (3) sisa duplikat yang hanya beda huruf besar/kecil di dalam sheet ini
        #     -> pakai ejaan yang paling sering muncul
        vc = df[col].astype(str).value_counts()
        canon = {}
        for name, n in vc.items():
            k = name.strip().lower()
            if k not in canon or n > vc[canon[k]]:
                canon[k] = name
        df[col] = df[col].map(lambda v: canon.get(str(v).strip().lower(), v) if isinstance(v, str) else v)

        # rekam apa saja yang berubah, supaya bisa ditelusuri
        for a, b in zip(asli, df[col]):
            if isinstance(a, str) and isinstance(b, str) and a.strip() != b.strip():
                AUDIT['rename'].append({'sheet': sheet, 'kolom': col,
                                        'dari': a.strip(), 'jadi': b.strip()})

        after = df[col].nunique()
        if after < before:
            print(f'      {col}: {before} -> {after} nama (varian digabung)')

    # Sheet pertama yang dibaca (Youtube Studio) menjadi acuan nama baku.
    if col_is_master and 'Channel' in df.columns and not CANON_CHANNEL:
        for v in df['Channel'].dropna().unique():
            CANON_CHANNEL[str(v).strip().lower()] = str(v).strip()
        print(f'      -> {len(CANON_CHANNEL)} nama channel baku dicatat dari sheet ini')

    print(f'   dibaca: {os.path.basename(path)} -> [{sheet}] ({len(df):,} baris)')
    return df


F_IMG     = find_file('konten', 'img')
F_SCRAPE  = find_file('scraping')
F_SOCMED  = find_file('socmed')
F_PORTAL  = find_file('portal')

# Periode diambil otomatis dari nama file (mis. "... Juli 2026.xlsx" -> "Juli 2026")
m = re.search(r'(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)\s+(\d{4})',
              F_IMG, re.I)
# Kalau nama file tidak menyebut bulan, periode diisi belakangan dari bulan
# terakhir yang ada datanya di sheet Recap Youtube (lihat bagian KPI).
PERIODE = f'{m.group(1).capitalize()} {m.group(2)}' if m else None
TANGGAL = pd.Timestamp.today().strftime('%Y-%m-%d')

print(f'\nPeriode terdeteksi : {PERIODE or "(dari nama file tidak terbaca, akan diambil dari isi data)"}')
print(f'Tanggal update     : {TANGGAL}\n')

def num(x):
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return 0
        return round(v, 2)
    except Exception:
        return 0

def coerce(df, cols):
    """Force numeric columns to real numbers (source sheets contain '-', 'N/A', etc.)"""
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(
                df[c].astype(str).str.replace(r'[,\s%$]', '', regex=True).str.replace('(', '-', regex=False).str.replace(')', '', regex=False),
                errors='coerce'
            ).fillna(0)
    return df


_MN = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
       'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}


def month_no(sr):
    return sr.astype(str).str.strip().str.lower().map(_MN)


out = {}

# ---------- 1. YouTube Studio (IMG owned channels) ----------
df = read(F_IMG, 'youtube', 'studio', col_is_master=True)
df = coerce(df, ['Views','Engaged views','Watch time (hours)','Subscribers','Impressions','Impressions click-through rate (%)','Average percentage viewed (%)','Duration (minutes)'])
g = df.groupby(['Unit', 'Channel'], dropna=False).agg(
    videos=('Views', 'size'),
    views=('Views', 'sum'),
    engaged=('Engaged views', 'sum'),
    watch_hours=('Watch time (hours)', 'sum'),
    subs=('Subscribers', 'sum'),
    ctr=('Impressions click-through rate (%)', 'mean'),
    pct_viewed=('Average percentage viewed (%)', 'mean'),
    impressions=('Impressions', 'sum'),
).reset_index()
out['studio'] = [
    {'unit': str(r['Unit']), 'channel': str(r['Channel']), 'videos': int(r['videos']),
     'views': num(r['views']), 'engaged': num(r['engaged']), 'watch_hours': num(r['watch_hours']),
     'subs': num(r['subs']), 'ctr': num(r['ctr']), 'pct_viewed': num(r['pct_viewed']),
     'impressions': num(r['impressions'])}
    for _, r in g.iterrows()
]

# top videos IMG
tv = df.nlargest(25, 'Views')[['Channel', 'Video title', 'Views', 'Watch time (hours)', 'Video publish time']]
out['top_videos_img'] = [
    {'channel': str(r['Channel']), 'title': str(r['Video title'])[:90], 'views': num(r['Views']),
     'watch_hours': num(r['Watch time (hours)']), 'date': str(r['Video publish time'])[:10]}
    for _, r in tv.iterrows()
]

# ---------- 1b. Youtube Studio: dimensi & metrik lanjutan ----------
# Sheet ini menyimpan satu baris per video, lengkap dengan label editorial
# (Kategori, Program, Part, Sub Part, Original/Repack, Type Content) dan metrik
# monetisasi. Semuanya belum pernah dipakai -- di bawah ini diringkas.

df = coerce(df, ['Estimated revenue (IDR)', 'Likes', 'Dislikes', 'Shares', 'Comments added',
                 'RPM (IDR)', 'CPM (IDR)', 'Subscribers gained', 'Subscribers lost',
                 'New viewers', 'Returning viewers', 'Ad impressions', 'Unique viewers'])

df['_eng'] = df['Likes'] + df['Shares'] + df['Comments added']


# Tanggal publish (nomor seri Excel) -> dipakai sebagai sumbu waktu
df['_tgl'] = pd.to_datetime(pd.to_numeric(df['Video publish time'], errors='coerce'),
                            unit='D', origin='1899-12-30', errors='coerce').dt.strftime('%Y-%m-%d')

# Semua dimensi editorial disimpan dalam SATU tabel panjang berdimensi tanggal,
# supaya bisa disaring per periode di aplikasi tanpa menggandakan data.
# ctr & pct disimpan sebagai JUMLAH (bukan rata-rata) supaya rata-ratanya bisa
# dihitung ulang dengan benar setelah baris disaring.
_DIMS = [('Kategori', 'kategori'), ('Program', 'program'), ('Part', 'part'),
         ('Sub Part', 'subpart'), ('Original', 'original'),
         ('Type Content', 'type'), ('8 Menit', 'durasi')]

_dfd = df.dropna(subset=['_tgl'])
_dim_rows = []
for _col, _nama in _DIMS:
    if _col not in df.columns:
        continue
    sub = _dfd.copy()
    sub[_col] = sub[_col].map(lambda v: '(tidak diisi)' if str(v) in ('nan', 'NaT', 'None', '') else str(v))
    if _nama == 'program':      # 107 program -> ambil 40 teratas agar file ramping
        sub = sub[sub[_col].isin(sub.groupby(_col)['Views'].sum().nlargest(40).index)]
    g = sub.groupby(['_tgl', _col], dropna=False).agg(
        videos=('Views', 'size'), views=('Views', 'sum'),
        watch=('Watch time (hours)', 'sum'), revenue=('Estimated revenue (IDR)', 'sum'),
        eng=('_eng', 'sum'), subs=('Subscribers gained', 'sum'),
        ctr_sum=('Impressions click-through rate (%)', 'sum'),
        pct_sum=('Average percentage viewed (%)', 'sum'),
    ).reset_index()
    for _, r in g.iterrows():
        _dim_rows.append([r['_tgl'], _nama, str(r[_col]), int(r['videos']), num(r['views']),
                          num(r['watch']), num(r['revenue']), num(r['eng']), num(r['subs']),
                          num(r['ctr_sum']), num(r['pct_sum'])])

out['ts_dim'] = {'cols': ['tgl', 'dim', 'key', 'videos', 'views', 'watch', 'revenue',
                          'eng', 'subs', 'ctr_sum', 'pct_sum'],
                 'rows': _dim_rows}

# Silang dimensi x channel (bulanan) -> supaya bisa menjawab
# "kategori apa yang paling bagus di Official iNews?"
_dfd['_y'] = _dfd['_tgl'].str.slice(0, 4).astype(int)
_dfd['_m'] = _dfd['_tgl'].str.slice(5, 7).astype(int)

_dc_rows = []
for _col, _nama in _DIMS:
    if _col not in df.columns:
        continue
    sub = _dfd.copy()
    sub[_col] = sub[_col].map(lambda v: '(tidak diisi)' if str(v) in ('nan', 'NaT', 'None', '') else str(v))
    if _nama == 'program':
        sub = sub[sub[_col].isin(sub.groupby(_col)['Views'].sum().nlargest(40).index)]
    g = sub.groupby(['_y', '_m', _col, 'Channel'], dropna=False).agg(
        videos=('Views', 'size'), views=('Views', 'sum'),
        watch=('Watch time (hours)', 'sum'), revenue=('Estimated revenue (IDR)', 'sum'),
        eng=('_eng', 'sum'),
        ctr_sum=('Impressions click-through rate (%)', 'sum'),
        pct_sum=('Average percentage viewed (%)', 'sum'),
    ).reset_index()
    for _, r in g.iterrows():
        _dc_rows.append([int(r['_y']), int(r['_m']), _nama, str(r[_col]), str(r['Channel']),
                         int(r['videos']), num(r['views']), num(r['watch']), num(r['revenue']),
                         num(r['eng']), num(r['ctr_sum']), num(r['pct_sum'])])

out['ts_dim_ch'] = {'cols': ['y', 'm', 'dim', 'key', 'channel', 'videos', 'views', 'watch',
                             'revenue', 'eng', 'ctr_sum', 'pct_sum'],
                    'rows': _dc_rows}

# Deret harian (kolom 'Video publish time' berisi nomor seri tanggal Excel)
if 'Video publish time' in df.columns:
    gd = _dfd.groupby('_tgl').agg(
        videos=('Views', 'size'), views=('Views', 'sum'),
        revenue=('Estimated revenue (IDR)', 'sum'), eng=('_eng', 'sum'),
        watch=('Watch time (hours)', 'sum'),
    ).reset_index().sort_values('_tgl')
    out['studio_daily'] = {'cols': ['tgl', 'videos', 'views', 'revenue', 'eng', 'watch'],
                           'rows': [[r['_tgl'], int(r['videos']), num(r['views']), num(r['revenue']),
                                     num(r['eng']), num(r['watch'])] for _, r in gd.iterrows()]}

# Metrik monetisasi & interaksi per channel, berdimensi tanggal
gm = _dfd.groupby(['_tgl', 'Channel'], dropna=False).agg(
    videos=('Views', 'size'), views=('Views', 'sum'),
    revenue=('Estimated revenue (IDR)', 'sum'), rpm_sum=('RPM (IDR)', 'sum'),
    cpm_sum=('CPM (IDR)', 'sum'), likes=('Likes', 'sum'), shares=('Shares', 'sum'),
    comments=('Comments added', 'sum'), subs_gained=('Subscribers gained', 'sum'),
    subs_lost=('Subscribers lost', 'sum'), new_v=('New viewers', 'sum'),
    ret_v=('Returning viewers', 'sum'),
).reset_index()
out['ts_money'] = {
    'cols': ['tgl', 'channel', 'videos', 'views', 'revenue', 'rpm_sum', 'cpm_sum',
             'likes', 'shares', 'comments', 'subs_gained', 'subs_lost', 'new_v', 'ret_v'],
    'rows': [[r['_tgl'], str(r['Channel']), int(r['videos']), num(r['views']), num(r['revenue']),
              num(r['rpm_sum']), num(r['cpm_sum']), num(r['likes']), num(r['shares']),
              num(r['comments']), num(r['subs_gained']), num(r['subs_lost']),
              num(r['new_v']), num(r['ret_v'])] for _, r in gm.iterrows()]}


# ---------- 2. Scraping (IMG + competitors) ----------
sc = read(F_SCRAPE, 'scraping')
sc = coerce(sc, ['Views','Likes','Comments','ER (%)','Duration (minutes)'])
gc = sc.groupby('Cluster', dropna=False).agg(
    videos=('Views', 'size'), views=('Views', 'sum'), likes=('Likes', 'sum'),
    comments=('Comments', 'sum'), er=('ER (%)', 'mean'),
).reset_index()
out['cluster'] = [
    {'cluster': str(r['Cluster']), 'videos': int(r['videos']), 'views': num(r['views']),
     'likes': num(r['likes']), 'comments': num(r['comments']), 'er': num(r['er'])}
    for _, r in gc.iterrows()
]

gch = sc.groupby(['Cluster', 'Channel'], dropna=False).agg(
    videos=('Views', 'size'), views=('Views', 'sum'), likes=('Likes', 'sum'),
    comments=('Comments', 'sum'), er=('ER (%)', 'mean'),
).reset_index()
gch = gch.nlargest(120, 'views')
out['channels_scraping'] = [
    {'cluster': str(r['Cluster']), 'channel': str(r['Channel']), 'videos': int(r['videos']),
     'views': num(r['views']), 'likes': num(r['likes']), 'comments': num(r['comments']), 'er': num(r['er'])}
    for _, r in gch.iterrows()
]

# category performance
if 'Category' in sc.columns:
    gcat = sc.groupby('Category', dropna=False).agg(
        videos=('Views', 'size'), views=('Views', 'sum'), er=('ER (%)', 'mean')).reset_index()
    out['category'] = [
        {'category': str(r['Category']), 'videos': int(r['videos']), 'views': num(r['views']), 'er': num(r['er'])}
        for _, r in gcat.nlargest(25, 'views').iterrows()]

# top videos overall
tvs = sc.nlargest(25, 'Views')[['Cluster', 'Channel', 'Title', 'Views', 'Likes', 'Comments', 'ER (%)']]
out['top_videos_all'] = [
    {'cluster': str(r['Cluster']), 'channel': str(r['Channel']), 'title': str(r['Title'])[:90],
     'views': num(r['Views']), 'likes': num(r['Likes']), 'comments': num(r['Comments']), 'er': num(r['ER (%)'])}
    for _, r in tvs.iterrows()
]

# Jam unggah -> untuk pertanyaan "jam berapa paling bagus posting"
if 'Upload Hour' in sc.columns:
    _hh = pd.to_numeric(sc['Upload Hour'].astype(str).str.slice(0, 2), errors='coerce')
    sch = sc.assign(_jam=_hh).dropna(subset=['_jam'])
    _tgl_sc = pd.to_datetime(sch['Upload Date'], format='%d/%m/%Y', errors='coerce')
    sch = sch.assign(_tgl=_tgl_sc.dt.strftime('%Y-%m-%d')).dropna(subset=['_tgl'])
    gh = sch.groupby(['_tgl', sch['_jam'].astype(int)]).agg(
        videos=('Views', 'size'), views=('Views', 'sum'), er_sum=('ER (%)', 'sum')).reset_index()
    gh.columns = ['tgl', 'jam', 'videos', 'views', 'er_sum']
    out['ts_jam'] = {'cols': ['tgl', 'jam', 'videos', 'views', 'er_sum'],
                     'rows': [[r['tgl'], int(r['jam']), int(r['videos']), num(r['views']),
                               num(r['er_sum'])] for _, r in gh.sort_values(['tgl', 'jam']).iterrows()]}

# Jumlah channel yang dipantau per cluster (IMG vs kompetitor)
_IMG_UNITS = ['iNews', 'Sindonews', 'Okezone', 'IDX Channel']
_gcl = sc.groupby('Cluster', dropna=False).agg(channels=('Channel', 'nunique'),
                                               videos=('Views', 'size')).reset_index()
out['cluster_channels'] = [
    {'cluster': str(r['Cluster']), 'channels': int(r['channels']), 'videos': int(r['videos']),
     'img': bool(str(r['Cluster']) in _IMG_UNITS)}
    for _, r in _gcl.sort_values(['channels', 'Cluster'], ascending=[False, True], kind='stable').iterrows()]

# ---------- 3. Social media ----------
sm = read(F_SOCMED, 'facebook')
sm = coerce(sm, ['Year','Videos Published','Lifetime Subscriber/Followers','New Subscribers/Followers','Views (Cumulative)','Revenue (USD)','Revenue (IDR)','Impressions','Reach','Engagement'])
# Followers: pakai nilai 'Lifetime Subscriber/Followers' pada BULAN TERAKHIR yang ada
# datanya, dijumlah antar channel. Bukan max lintas bulan -- kalau pakai max, penurunan
# follower akan tertutupi oleh angka puncak di bulan sebelumnya.
_BLN_EN = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
           'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
sm['_mn'] = sm['Month'].astype(str).str.strip().str.lower().map(_BLN_EN)
_smv = sm[sm['Lifetime Subscriber/Followers'] > 0]
_sm_year = int(_smv['Year'].max())
_sm_month = int(_smv[_smv['Year'] == _sm_year]['_mn'].max())
_sm_last = _smv[(_smv['Year'] == _sm_year) & (_smv['_mn'] == _sm_month)]

foll_per_ch = _sm_last.groupby(['Platform', 'Channel'], dropna=False)['Lifetime Subscriber/Followers'].max()
foll_per_plat = foll_per_ch.groupby('Platform').sum()

gp = sm.groupby('Platform', dropna=False).agg(
    channels=('Channel', 'nunique'),
    videos=('Videos Published', 'sum'),
    new_followers=('New Subscribers/Followers', 'sum'),
    views=('Views (Cumulative)', 'sum'),
    rev_usd=('Revenue (USD)', 'sum'),
    rev_idr=('Revenue (IDR)', 'sum'),
    engagement=('Engagement', 'sum'),
    reach=('Reach', 'sum'),
).reset_index()
out['platform'] = [
    {'platform': str(r['Platform']), 'channels': int(r['channels']), 'videos': num(r['videos']),
     'followers': num(foll_per_plat.get(r['Platform'], 0)), 'new_followers': num(r['new_followers']), 'views': num(r['views']),
     'rev_usd': num(r['rev_usd']), 'rev_idr': num(r['rev_idr']), 'engagement': num(r['engagement']),
     'reach': num(r['reach'])}
    for _, r in gp.iterrows()
]

gsc = sm.groupby(['Platform', 'Unit', 'Channel'], dropna=False).agg(
    followers=('Lifetime Subscriber/Followers', 'max'),
    views=('Views (Cumulative)', 'sum'),
    rev_idr=('Revenue (IDR)', 'sum'),
    engagement=('Engagement', 'sum'),
).reset_index().nlargest(80, 'views')
out['socmed_channels'] = [
    {'platform': str(r['Platform']), 'unit': str(r['Unit']), 'channel': str(r['Channel']),
     'followers': num(r['followers']), 'views': num(r['views']), 'rev_idr': num(r['rev_idr']),
     'engagement': num(r['engagement'])}
    for _, r in gsc.iterrows()
]

# Demografi penonton socmed (nilai berupa pecahan, mis. 0.707 = 70,7%)
_dem_cols = ['View Male (%)', 'View Female (%)'] + \
            [c for c in sm.columns if 'Years' in c]
sm = coerce(sm, _dem_cols)
_smd = sm.dropna(subset=['_mn'])
if len(_smd) and _dem_cols:
    _dem_label = [c.replace(' (%)', '').replace('View ', '').strip() for c in _dem_cols]
    gdm = _smd.groupby(['Year', '_mn', 'Platform'], dropna=False)[_dem_cols].mean().reset_index()
    out['ts_demografi'] = {
        'cols': ['y', 'm', 'platform'] + _dem_label,
        'rows': [[int(r['Year']), int(r['_mn']), str(r['Platform'])]
                 + [num(r[c] * 100) for c in _dem_cols] for _, r in gdm.iterrows()]}

# ---------- 4. Recap YouTube (monthly) ----------
ry = read(F_SOCMED, 'recap', 'youtube')
ry = coerce(ry, ['Year','Views Cummulative','Engaged views','Watch time (hours)','Subscribers','Videos published','Impressions','Impressions click-through rate (%)','Lifetime Subscriber/Followers','Revenue Cummulative (IDR)'])

# 'Month' berisi nama bulan (January, February, ...) -> ubah ke angka
MONTHS = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
          'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
ry['MonthNo'] = ry['Month'].astype(str).str.strip().str.lower().map(MONTHS)

# Buang baris bulan yang masih kosong (placeholder bulan yang belum berjalan)
ry = ry[ry['Views Cummulative'] > 0].copy()

# Ringkasan per TAHUN (+ jumlah bulan yang tersedia, supaya perbandingan adil)
gy = ry.groupby('Year', dropna=False).agg(
    views=('Views Cummulative', 'sum'), watch=('Watch time (hours)', 'sum'),
    subs=('Subscribers', 'sum'), videos=('Videos published', 'sum'),
    months=('MonthNo', 'nunique'),
).reset_index()
out['yearly'] = [
    {'year': int(num(r['Year'])), 'views': num(r['views']), 'watch': num(r['watch']),
     'subs': num(r['subs']), 'videos': num(r['videos']), 'months': int(r['months'])}
    for _, r in gy.iterrows()
]

# Deret per BULAN untuk grafik tren
gmm = ry.dropna(subset=['MonthNo']).groupby(['Year', 'MonthNo'], dropna=False).agg(
    views=('Views Cummulative', 'sum'), watch=('Watch time (hours)', 'sum'),
    subs=('Subscribers', 'sum'), videos=('Videos published', 'sum'),
).reset_index().sort_values(['Year', 'MonthNo'])
out['monthly'] = [
    {'year': int(num(r['Year'])), 'month': int(num(r['MonthNo'])), 'views': num(r['views']),
     'watch': num(r['watch']), 'subs': num(r['subs']), 'videos': num(r['videos'])}
    for _, r in gmm.iterrows()
]

gyc = ry.groupby(['Unit', 'Channel'], dropna=False).agg(
    views=('Views Cummulative', 'sum'), watch=('Watch time (hours)', 'sum'),
    subs=('Subscribers', 'sum'), videos=('Videos published', 'sum'),
    ctr=('Impressions click-through rate (%)', 'mean'),
).reset_index().nlargest(60, 'views')
out['yt_channels'] = [
    {'unit': str(r['Unit']), 'channel': str(r['Channel']), 'views': num(r['views']),
     'watch': num(r['watch']), 'subs': num(r['subs']), 'videos': num(r['videos']), 'ctr': num(r['ctr'])}
    for _, r in gyc.iterrows()
]

# ---------- 5. YouTube revenue ----------
try:
    rev = read(F_SOCMED, 'revenue', 'youtube')
    rev = coerce(rev, ['Estimated revenue (IDR)','Transaction revenue (IDR)','Total sales (IDR)'])
    gr = rev.groupby(['Unit', 'Channel'], dropna=False).agg(
        revenue=('Estimated revenue (IDR)', 'sum')).reset_index().nlargest(40, 'revenue')
    out['yt_revenue'] = [
        {'unit': str(r['Unit']), 'channel': str(r['Channel']), 'revenue': num(r['revenue'])}
        for _, r in gr.iterrows()]
    grs = rev.groupby('Revenue source', dropna=False).agg(
        revenue=('Estimated revenue (IDR)', 'sum')).reset_index().nlargest(15, 'revenue')
    out['yt_revenue_source'] = [
        {'source': str(r['Revenue source']), 'revenue': num(r['revenue'])} for _, r in grs.iterrows()]
except Exception as e:
    print('rev skip', e)

# ---------- 6. Portal ----------
pc = read(F_PORTAL, 'similar')
pc = coerce(pc, ['Year','Total Visits','Page Views','Unique Visitors','Bounce Rate','Page per Visit'])
gpo = pc.groupby(['Group', 'Portal'], dropna=False).agg(
    visits=('Total Visits', 'sum'), pageviews=('Page Views', 'sum'),
    uv=('Unique Visitors', 'sum'), bounce=('Bounce Rate', 'mean'),
    ppv=('Page per Visit', 'mean'),
).reset_index().nlargest(60, 'visits')
out['portal'] = [
    {'group': str(r['Group']), 'portal': str(r['Portal']), 'visits': num(r['visits']),
     'pageviews': num(r['pageviews']), 'uv': num(r['uv']), 'bounce': num(r['bounce']), 'ppv': num(r['ppv'])}
    for _, r in gpo.iterrows()
]

try:
    prv = read(F_PORTAL, 'revenue', 'portal')
    prv = coerce(prv, ['VALUE'])
    gprv = prv.groupby('CHANNEL', dropna=False).agg(revenue=('VALUE', 'sum')).reset_index().nlargest(30, 'revenue')
    out['portal_revenue'] = [
        {'channel': str(r['CHANNEL']), 'revenue': num(r['revenue'])} for _, r in gprv.iterrows()]
except Exception as e:
    print('portal rev skip', e)

# Revenue portal per jenis penjualan
try:
    if 'TYPE' in prv.columns:
        prv['_mn'] = month_no(prv['MONTH'])
        prv['_y'] = pd.to_numeric(prv['YEAR'], errors='coerce').fillna(0).astype(int)
        pt = prv.dropna(subset=['_mn'])
        gt = pt.groupby(['_y', '_mn', 'TYPE'], dropna=False).agg(revenue=('VALUE', 'sum')).reset_index()
        out['ts_portal_tipe'] = {
            'cols': ['y', 'm', 'tipe', 'revenue'],
            'rows': [[int(r['_y']), int(r['_mn']), str(r['TYPE']), num(r['revenue'])]
                     for _, r in gt.iterrows()]}
except Exception as e:
    print('   portal_revenue_tipe dilewati:', e)

# ---------- Pemeriksaan nama channel ----------
# Sheet Recap Youtube dan Source Revenue seharusnya berisi channel IMG yang sama
# persis dengan sheet Youtube Studio. Kalau ada nama yang tidak dikenal, berarti
# muncul varian penulisan baru -> perlu ditambahkan ke CHANNEL_ALIAS.
import difflib

_canon_names = sorted(set(CANON_CHANNEL.values()))
for _lbl, _dfx in [('Recap Youtube', ry), ('Source Revenue Youtube', rev if 'rev' in dir() else None)]:
    if _dfx is None or 'Channel' not in getattr(_dfx, 'columns', []):
        continue
    for _n in sorted(set(str(x).strip() for x in _dfx['Channel'].dropna())):
        if _n.lower() in CANON_CHANNEL:
            continue
        _dekat = difflib.get_close_matches(_n, _canon_names, n=1, cutoff=0.6)
        AUDIT['unknown'].append({'sheet': _lbl, 'nama': _n,
                                 'mirip': _dekat[0] if _dekat else None})

if AUDIT['unknown']:
    print('\n[PERHATIAN] Nama channel berikut tidak ada di sheet Youtube Studio:')
    for u in AUDIT['unknown']:
        saran = f" -> mungkin maksudnya '{u['mirip']}'" if u['mirip'] else ''
        print(f"   [{u['sheet']}] '{u['nama']}'{saran}")
    print("   Tambahkan ke CHANNEL_ALIAS di build_data.py bila memang channel yang sama.\n")

# ringkasan penggantian nama (dikelompokkan)
_rk = {}
for r in AUDIT['rename']:
    _rk.setdefault((r['dari'], r['jadi']), 0)
    _rk[(r['dari'], r['jadi'])] += 1
out['audit'] = {
    'rename': [{'dari': a, 'jadi': b, 'baris': n} for (a, b), n in
               sorted(_rk.items(), key=lambda x: -x[1])],
    'unknown': AUDIT['unknown'],
    'canon': _canon_names,
}

# ---------- DERET WAKTU (supaya pertanyaan berperiode bisa dijawab) ----------
# Disimpan ringkas: {'cols': [...], 'rows': [[...], ...]} -- jauh lebih kecil daripada
# array of object, karena nama kolom tidak diulang di tiap baris.

def as_table(df, cols):
    return {'cols': cols,
            'rows': [[int(r[c]) if c in ('y', 'm') else
                      (str(r[c]) if isinstance(r[c], str) else num(r[c]))
                      for c in cols] for _, r in df.iterrows()]}


# 1) YouTube IMG per bulan per channel (sumber: Recap Youtube)
_ts = ry.copy()
_ts['y'] = _ts['Year'].astype(int)
_ts['m'] = _ts['MonthNo'].astype(int)
_g = _ts.groupby(['y', 'm', 'Unit', 'Channel'], dropna=False).agg(
    views=('Views Cummulative', 'sum'),
    watch=('Watch time (hours)', 'sum'),
    subs_gained=('Subscribers', 'sum'),
    videos=('Videos published', 'sum'),
    revenue=('Revenue Cummulative (IDR)', 'sum'),
    lifetime=('Lifetime Subscriber/Followers', 'max'),
).reset_index().rename(columns={'Unit': 'unit', 'Channel': 'channel'})
out['ts_youtube'] = as_table(_g, ['y', 'm', 'unit', 'channel', 'views', 'watch',
                                  'subs_gained', 'videos', 'revenue', 'lifetime'])

# 2) Sumber revenue YouTube per bulan
try:
    _r = rev.copy()
    _r['m'] = month_no(_r['Month'])
    _r = _r.dropna(subset=['m'])
    _r['y'] = pd.to_numeric(_r['Year'], errors='coerce').fillna(0).astype(int)
    _r['m'] = _r['m'].astype(int)
    _gr = _r.groupby(['y', 'm', 'Revenue source'], dropna=False).agg(
        revenue=('Estimated revenue (IDR)', 'sum')).reset_index().rename(columns={'Revenue source': 'source'})
    _gr = _gr[_gr['revenue'] != 0]
    out['ts_revenue_source'] = as_table(_gr, ['y', 'm', 'source', 'revenue'])
except Exception as e:
    print('   ts_revenue_source dilewati:', e)

# 3) Social media per bulan per platform+channel
_s = sm.copy()
_s['m'] = _s['_mn']
_s = _s.dropna(subset=['m'])
_s['y'] = pd.to_numeric(_s['Year'], errors='coerce').fillna(0).astype(int)
_s['m'] = _s['m'].astype(int)
_gs = _s.groupby(['y', 'm', 'Platform', 'Channel'], dropna=False).agg(
    views=('Views (Cumulative)', 'sum'),
    followers=('Lifetime Subscriber/Followers', 'max'),
    new_followers=('New Subscribers/Followers', 'sum'),
    engagement=('Engagement', 'sum'),
    revenue=('Revenue (IDR)', 'sum'),
).reset_index().rename(columns={'Platform': 'platform', 'Channel': 'channel'})
_gs = _gs[(_gs['views'] != 0) | (_gs['followers'] != 0)]
out['ts_socmed'] = as_table(_gs, ['y', 'm', 'platform', 'channel', 'views',
                                  'followers', 'new_followers', 'engagement', 'revenue'])

# 4) Portal per bulan
_p = pc.copy()
_p['m'] = month_no(_p['Month'])
_p = _p.dropna(subset=['m'])
_p['y'] = pd.to_numeric(_p['Year'], errors='coerce').fillna(0).astype(int)
_p['m'] = _p['m'].astype(int)
def _sec2(v):
    try:
        h2, mi2, s2 = str(v).split(':')
        return int(h2) * 3600 + int(mi2) * 60 + int(s2)
    except Exception:
        return 0
_p['_dur'] = _p['Avg Visit Duration'].map(_sec2) if 'Avg Visit Duration' in _p.columns else 0
_gpp = _p.groupby(['y', 'm', 'Group', 'Portal'], dropna=False).agg(
    visits=('Total Visits', 'sum'), pageviews=('Page Views', 'sum'),
    uv=('Unique Visitors', 'sum'), dur_sum=('_dur', 'sum'),
    bounce_sum=('Bounce Rate', 'sum'), n=('Total Visits', 'size'),
).reset_index().rename(columns={'Group': 'group', 'Portal': 'portal'})
_gpp = _gpp[_gpp['visits'] != 0]
out['ts_portal'] = as_table(_gpp, ['y', 'm', 'group', 'portal', 'visits', 'pageviews', 'uv',
                                   'dur_sum', 'bounce_sum', 'n'])

# Rentang bulan yang tersedia -> dipakai untuk memvalidasi periode yang diminta user
def _span(tbl):
    rs = out[tbl]['rows']
    if not rs:
        return None
    ym = sorted((r[0] * 12 + r[1]) for r in rs)
    return {'from': [ym[0] // 12, ym[0] % 12 or 12], 'to': [ym[-1] // 12, ym[-1] % 12 or 12]}


def _span_tgl(tbl):
    rs = out.get(tbl, {}).get('rows', [])
    if not rs:
        return None
    ts = sorted(r[0] for r in rs)
    a, b = ts[0], ts[-1]
    return {'from': [int(a[:4]), int(a[5:7])], 'to': [int(b[:4]), int(b[5:7])],
            'tgl_from': a, 'tgl_to': b, 'hari': len({r[0] for r in rs})}


out['coverage'] = {
    'youtube': _span('ts_youtube'),
    'socmed': _span('ts_socmed'),
    'portal': _span('ts_portal'),
    'portal_sales': _span('ts_portal_tipe'),
    'studio': _span_tgl('ts_dim'),
    'scraping': _span_tgl('ts_jam'),
    # Scraping & YouTube Studio hanya berisi satu bulan -> tidak bisa difilter periode
    'snapshot_only': PERIODE,
}

# ---------- KPI bulan terakhir (untuk kartu di bagian atas aplikasi) ----------
BULAN_ID = ['Januari','Februari','Maret','April','Mei','Juni',
            'Juli','Agustus','September','Oktober','November','Desember']

# 'ry' sudah difilter: hanya baris bulan yang benar-benar ada datanya
_last_year = int(ry['Year'].max())
_ly = ry[ry['Year'] == _last_year]
_last_month = int(_ly['MonthNo'].max())
_lm = _ly[_ly['MonthNo'] == _last_month]

# Total subscriber YouTube IMG = nilai lifetime tiap channel di bulan terakhir, dijumlah
_yt_subs = num(_lm.groupby('Channel')['Lifetime Subscriber/Followers'].max().sum())
_socmed_foll = num(foll_per_plat.sum())

_LAST_LABEL = f'{BULAN_ID[_last_month - 1]} {_last_year}'
if not PERIODE:
    PERIODE = _LAST_LABEL
    print(f'   periode diambil dari isi data: {PERIODE}')

out['kpi'] = {
    'last_label': _LAST_LABEL,
    'yt_views_last': num(_lm['Views Cummulative'].sum()),
    'yt_revenue_last': num(_lm['Revenue Cummulative (IDR)'].sum()),
    'yt_subs': _yt_subs,
    'yt_channels': int(_lm['Channel'].nunique()),
    'socmed_followers': num(_yt_subs + _socmed_foll),
    'socmed_platforms': int(sm['Platform'].nunique()) + 1,   # +1 untuk YouTube
}

# ---------- meta ----------
out['meta'] = {
    'generated': TANGGAL,
    'period': PERIODE,
    'rows_studio': int(len(df)),
    'rows_scraping': int(len(sc)),
    'rows_socmed': int(len(sm)),
    'rows_portal': int(len(pc)),
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, separators=(',', ':'))

import os
print(f"✅ data.json written: {os.path.getsize('data.json')/1024:.0f} KB")
for k, v in out.items():
    if isinstance(v, list):
        print(f"   {k}: {len(v)} entries")
