from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox, LTRect, LTFigure, LTCurve, LTChar
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

import matplotlib.pyplot as plt
import numpy as np


def find_textboxes_recursively(layout_obj):
    """
    再帰的にテキストボックス（LTTextBox）を探して、テキストボックスのリストを取得する。
    """
    # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []  # その他の場合は空リストを返す。

def FindChars(layout_obj):
    if isinstance(layout_obj, LTTextBox):
        chars = []
        chars2 = []
        for child in layout_obj:
            chars.extend(child)
        for charx in chars:
            if isinstance(charx, LTChar):
                chars2.append(charx)
        return chars2

    # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(FindChars(child))

        return boxes

    return []  # その他の場合は空リストを返す。

def FindRects(layout_obj):
    if isinstance(layout_obj, LTRect):
        return [layout_obj]

    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(FindRects(child))

        return boxes

    return []  # その他の場合は空リストを返す。

def FindLTs(layout_obj):
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]
    
    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(FindLTs(child))
        return boxes
    
    else:
        return [layout_obj]
        def PDFToLayouts(path):
    # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
    laparams = LAParams(detect_vertical=True)

    # 共有のリソースを管理するリソースマネージャーを作成。
    resource_manager = PDFResourceManager()

    # ページを集めるPageAggregatorオブジェクトを作成。
    device = PDFPageAggregator(resource_manager, laparams=laparams)

    # Interpreterオブジェクトを作成。
    interpreter = PDFPageInterpreter(resource_manager, device)
    
    layouts = []
    with open(path, 'rb') as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            layouts.append(device.get_result())
    return layouts

def PDFToString(path):
    layouts = PDFToLayouts(path)
    outtext = ''
    for layout in layouts:
        boxes = find_textboxes_recursively(layout)
        # テキストボックスの左上の座標の順でテキストボックスをソートする。
        # y1（Y座標の値）は上に行くほど大きくなるので、正負を反転させている。
        boxes.sort(key=lambda b: (-b.y1, b.x0))
        for box in boxes:
            outtext += box.get_text().strip()
    return outtext

def ShowLines(lines):
    for line in lines:
        print(line)

def PDFToLines(path, sort = False, show = False):
    layouts = PDFToLayouts(path)
    lines = ['']
    for layout in layouts:
        boxes = find_textboxes_recursively(layout)
        if sort:
            boxes.sort(key=lambda b: (-b.y1, b.x0))
        y = boxes[0].y0
        for box in boxes:
            if box.y0 == y:
                lines[-1] += box.get_text().strip()
            else:
                lines.append(box.get_text().strip())
                y = box.y0
    if show:
        ShowLines(lines)
        
    return lines

def PDFToLTs(path):
    layouts = PDFToLayouts(path)
    lts = []
    for layout in layouts:
        lts.extend(FindLTs(layout))
        
    return lts
    
def Nearest(list, num):
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]

def PlotRect(x0, y0, x1, y1):
    plt.plot([x0, x1], [y0, y0], 'k-', lw=1)
    plt.plot([x0, x1], [y1, y1], 'k-', lw=1)
    plt.plot([x0, x0], [y0, y1], 'k-', lw=1)
    plt.plot([x1, x1], [y0, y1], 'k-', lw=1)

def Integrate(rects, threshold):
    #近くにある線の座標をまとめる
    xs0 = []
    ys0 = []
    for rect in rects:
        xs0.append(rect.x0)
        xs0.append(rect.x1)
        ys0.append(rect.y0)
        ys0.append(rect.y1) 
    xs0.sort()
    ys0.sort()
    xs1 = []
    ys1 = []
    if (xs0 != []) & (ys0 != []):
        xs1 = [xs0[0]]
        ys1 = [ys0[0]]
    for x in xs0:
        if x > (xs1[-1] + threshold):
            # xが既に記録した線のx座標と一定以上離れていたら、あらたにx座標を追加する
            xs1.append(x)
    for y in ys0:
        if y > (ys1[-1] + threshold):
            ys1.append(y)
            
    return [xs1, ys1]
    
def ShowBoxandRect(chars, rects, threshold):
    plt.figure(figsize=(15, 21.2))
    for charx in chars:
        plt.plot(charx.x0, charx.y0, ms=0)
        plt.annotate(charx._text, xy=(charx.x0, charx.y0))
    
    xs1, ys1 = Integrate(rects, threshold)
    
    # 長方形をプロットする
    for rect in rects:
        nx0 = Nearest(xs1, rect.x0)
        nx1 = Nearest(xs1, rect.x1)
        ny0 = Nearest(ys1, rect.y0)
        ny1 = Nearest(ys1, rect.y1) 
        PlotRect(nx0, ny0, nx1, ny1) 
    plt.show()

def ShowPDF(path, threshold=5):
    laparams = LAParams(detect_vertical=True)
    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    lines = ['']
    with open(path, 'rb') as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            layout = device.get_result()
            chars = FindChars(layout)
            rects = FindRects(layout)
            ShowBoxandRect(chars, rects, threshold)
