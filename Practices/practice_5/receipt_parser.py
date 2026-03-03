import re
import json
def clean_price(price_str):
    return float(price_str.replace(" ", "").replace(",", "."))
def extract_prices(text):
    pattern = r"\n(\d[\d\s]*,\d{2})\nСтоимость"
    matches = re.findall(pattern, text)
    return [clean_price(p) for p in matches]
def extract_products(text):
    pattern = r"\d+\.\n(.+?)\n\d+,\d{3}\s+x\s+[\d\s]+,\d{2}"
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.replace("\n", " ").strip() for m in matches]
def extract_total(text):
    pattern = r"ИТОГО:\n([\d\s]+,\d{2})"
    match = re.search(pattern, text)
    return clean_price(match.group(1)) if match else None
def extract_payment_method(text):
    pattern = r"(Банковская карта|Наличные)"
    match = re.search(pattern, text)
    return match.group(1) if match else None
def extract_datetime(text):
    pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})"
    match = re.search(pattern, text)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2)
        }
    return None
def parse_receipt(text):
    return {
        "products": extract_products(text),
        "prices": extract_prices(text),
        "total": extract_total(text),
        "payment_method": extract_payment_method(text),
        "datetime": extract_datetime(text)
    }

if __name__ == "__main__":
    with open("raw.txt", "r", encoding="utf-8") as f:
        receipt_text = f.read()
    result = parse_receipt(receipt_text)
    print(json.dumps(result, indent=4, ensure_ascii=False))