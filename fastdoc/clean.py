# AUTOGENERATED! DO NOT EDIT! File to edit: 01_clean.ipynb (unless otherwise specified).

__all__ = ['count_tk', 'find_tokens', 'is_header_cell', 'is_clean_cell', 'get_stop_idx', 'clean_tags', 'clean_nb',
           'clean_all']

# Cell
from .imports import *
from .asciidoc import copy_images

# Cell
def count_tk(fname):
    nb = read_nb(Path(fname))
    c = 0
    for cell in nb['cells']: c += len(re.findall('TK', cell['source']))
    return c

# Cell
def find_tokens(path='book'):
    path = Path(path)
    tks = [(f,count_tk(f)) for f in path.iterdir() if f.suffix == '.ipynb' and not f.name.startswith('_')]
    tks.sort(key=lambda o:o[1], reverse=True)
    if tks[0]==0: print("No TK remaining!")
    else:
        for f,tk in tks:
            if tk !=0: print(f'{f} still has {tk} TK.')

# Cell
_re_header = re.compile(r'^#+\s+\S+')
_re_clean  = re.compile(r'^\s*#\s*clean\s*')

# Cell
def is_header_cell(cell): return _re_header.search(cell['source']) is not None

# Cell
def is_clean_cell(cell): return _re_clean.search(cell['source']) is not None

# Cell
_re_questionnaire = re.compile(r'^#+\s+Questionnaire')

# Cell
def get_stop_idx(cells):
    i = 0
    while i < len(cells) and _re_questionnaire.search(cells[i]['source']) is None: i+=1
    return i

# Cell
def clean_tags(cell):
    if is_header_cell(cell): return cell
    for attr in ["id", "caption", "alt", "width", "hide_input", "hide_output", "clean"]:
        cell["source"] = re.sub(r'#\s*' + attr + r'.*?($|\n)', '', cell["source"])
    return cell

# Cell
def clean_nb(fname, dest=None):
    fname = Path(fname)
    nb = read_nb(fname)
    i = get_stop_idx(nb['cells'])
    nb['cells'] = [clean_tags(c) for j,c in enumerate(nb['cells']) if
                   c['cell_type']=='code' or is_header_cell(c) or is_clean_cell(c) or j >= i]
    if dest is None: dest = fname.parent/f'{fname.stem}_clean.ipynb'
    with open(dest, 'w') as f: nbformat.write(nb, f, version=4)

# Cell
def clean_all(path='book', dest_path=None):
    path = Path(path)
    dest_path = Path('..')/'fastbook' if dest_path is None else Path(dest_path)
    dest_path1 = Path('..')/'course-v4/nbs'
    nbs = [f for f in path.iterdir() if f.suffix == '.ipynb' and not f.name.startswith('_')]
    for nb in nbs:
        shutil.copy(nb, dest_path/nb.name)
        clean_nb(nb, dest=dest_path/'clean'/nb.name)
        clean_nb(nb, dest=dest_path1/nb.name)
    shutil.copy(path/'utils.py', dest_path/'utils.py')
    shutil.copy(path/'utils.py', dest_path1/'utils.py')
    copy_images(path, dest_path)