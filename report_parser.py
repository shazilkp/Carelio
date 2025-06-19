from PIL import Image
import pytesseract
import re
from name_map import name_map
from rapidfuzz import process

translation_table = str.maketrans({'§': '5', ',': ''})

def parseRange(string):
    num = re.search(r"([\d.,]+)\s*[-–]\s*([\d.,]+)", string)
    if num:
        range_ = [float(num.group(1).translate(translation_table)), float(num.group(2).translate(translation_table))]
        unit = string[num.end():].strip()
        return range_,unit

    symbolic = re.search(r"([<>]=?)\s*(\d+(?:\.\d+)?)", string)
    if symbolic:
        range_ [symbolic.group(1), float(symbolic.group(2))]
        unit = string[symbolic.end():].strip()
        return range_,unit

    verbal = re.search(r"(?:less than|under|below|up to|upto)\s+(\d+(?:\.\d+)?)", string)
    if verbal:
        range_ = ["<", float(verbal.group(1))]
        unit = string[verbal.end():].strip()
        return range_,unit

    verbal = re.search(r"(?:more than|above)\s+(\d+(?:\.\d+)?)", string)
    if verbal:
        range_ = [">", float(verbal.group(1))]
        unit = string[verbal.end():].strip()
        return range_,unit
    return None
        
        
def report_parser(url):
    text_out = pytesseract.image_to_string(Image.open(url))


    text_out = text_out.split('\n')
    # removing every dot not inbetween 2 numbers
    text_out = [re.sub(r"(?<!\d)\.(?!\d)", '', line) for line in text_out]

    for y in text_out:
        print(y)

    report = []
    for x in text_out:
        match = re.search(r"([a-zA-Z/_%#()\}{\- ]+)\s+([§\d.,]+)[.+_+\s+](.*)",x)
        if match:
            data = {}
            data['name'] = match.group(1)
            data['value'] = float(match.group(2).translate(translation_table))
            range_unit = parseRange(match.group(3).lower())
            if range_unit != None:
                data['ref_range'] = range_unit[0]
                data['unit'] = re.sub(r"(\d+)\s*[%*°]\s*(\d+)/(\w+)", r"10^\2/\3", range_unit[1])
            report.append(data)

    for y in report:
        result = process.extractOne(y['name'].lower(), name_map.keys())
        if result and result[1] > 90:
            y['name'] = name_map[result[0]]

    return report