from PIL import Image
import pytesseract
import re

def parseRange(string):
    num = re.search(r"([\d.]+)\s*[-–]\s*([\d.]+)", string)
    if num:
        range_ = [float(num.group(1)), float(num.group(2))]
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
        
        

text_out = pytesseract.image_to_string(Image.open('rep2.jpg'))
text_out = re.sub(r"(\d+\.\d+)(\d+\.\d+)", r"\1 - \2", text_out)
tr = "MCHC% 33 32.0-36.0 g/dL"
match = re.search(r"([\w/\-%#]+)\s+([\d.]+)\s+([\d.]+)\s*[-–]\s*([\d.]+)\s+(.*)", tr)

text_out = text_out.split('\n')
report = []
for x in text_out:
    match = re.search(r"([\w/\-%#\(\) ]+)\s+([\d.]+)\s+(.*)",x)
    if match:
        data = {}
        data['name'] = match.group(1)
        data['value'] = float(match.group(2))
        range_unit = parseRange(match.group(3).lower())
        if range_unit != None:
            data['ref_range'] = range_unit[0]
            data['unit'] = re.sub(r"(\d+)\s*[%*°]\s*(\d+)/(\w+)", r"10^\2/\3", range_unit[1])
        report.append(data)

for y in report:
    print(y)