from pdfplumber import open as op
from pandas import DataFrame
from json import dump
from langdetect import detect
from langcodes import Language
from tqdm import tqdm
from os import path, makedirs, walk

not_extracted = []  # recording non-English PDFs or error PDFs

# Sort elements from top to bottom then left to right
def sort_elements(elements):
    return sorted(elements, key=lambda element: (element['top'], element['x0']))

def group_elements_by_line(elements, tolerance=5):
    lines = []; current_line = []; current_top = elements[0]['top']
    for element in elements:
        if abs(element['top'] - current_top) > tolerance:
            lines.append(current_line)
            current_line = [element]
            current_top = element['top']
        else:
            current_line.append(element)
    lines.append(current_line)
    return lines

def reconstruct_text_with_spaces(lines, margin_unit=2):
    result = []
    for line in lines:
        sorted_line = sorted(line, key=lambda e: e['x0'])
        if sorted_line:
            first_element = sorted_line[0]
            line_text = ' ' * int(first_element['x0'] / margin_unit)  # Add leading spaces based on margin
            last_x = first_element['x0']

            for element in sorted_line:
                if element != first_element:
                    space_count = int((element['x0'] - last_x) / margin_unit)
                    line_text += ' ' * space_count
                line_text += element['content']
                last_x = element['x0'] + len(element['content']) * margin_unit
            result.append(line_text)
    return "\n".join(result).strip()

def extract_text_and_images_per_page(pdf_path: str, image_save_dir: str) -> list:
    page_data = []
    with op(pdf_path) as pdf:
        pdf_name = pdf_path.replace("/", '_').split('.')[-2][1:]
        for page_num, page in enumerate(pdf.pages):
            elements = []

            # Extract words
            elements.extend([{'x0': word['x0'], 'top': word['top'], 'content': word['text']} for word in page.extract_words()])

            # Extract images and add as textual elements
            if page.images:
                for img_num, img in enumerate(page.images):
                    img_bbox = img['x0'], img['top'], img['x1'], img['bottom']
                    save_path = path.join(image_save_dir, f"{pdf_name}_page_{page_num + 1}_img_{img_num + 1}.png")
                    page.within_bbox(img_bbox).to_image(resolution=512).save(save_path, format="PNG")
                    # Add the image path as a string element
                    elements.append({'x0': img['x0'], 'top': img['top'], 'content': f"<img>{save_path}</img>"})

            # Extract tables and add as textual elements
            tables_loc = page.find_tables()
            tables = page.extract_tables()
            if tables:
                elements.extend([{'x0': loc.bbox[0], 'top': loc.bbox[1], 'content': f"<table>{str(table)}</table>"} for table, loc in zip(tables, tables_loc)])

            # Sort and group elements into lines
            text = reconstruct_text_with_spaces(group_elements_by_line(sort_elements(elements)))

            # Language detection
            lang_code = detect(text) if text else "unknown"
            if lang_code != "unknown":
                detected_language = Language.get(lang_code).display_name()

            # Append page data
            page_data.append({'pdf_path': pdf_path, 'page_number': page_num + 1, 'text': text, 'language': detected_language})
    return page_data

def process_pdf(pdf_path: str, output_dir: str) -> None:
    try:
        page_data = extract_text_and_images_per_page(pdf_path, path.join(output_dir, "images")) # extract data from a pdf
        df = DataFrame(page_data)
        pdf_name = pdf_path.replace("/", "_").split('.')[-2][1:]
        if (df['language'] != 'English').any():
            not_extracted.append({'pdf_path': pdf_path, "language": ', '.join(df['language'].unique())})
        else:
            csv_file_path = path.join(output_dir, f"csv/{pdf_name}.csv")
            print(csv_file_path)
            printsaving("saving..")
            df.to_csv(csv_file_path, mode='a', index=False, header=not os.path.exists(csv_file_path), encoding='utf-8') # save as csv
            json_file_path = path.join(output_dir, f"json/{pdf_name}.json")
            with open(json_file_path, mode='w', encoding='utf-8') as json_file:
                dump(page_data, json_file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Failed to process {pdf_path}: {e}")
        not_extracted.append({"pdf_path": pdf_path, "language": "unknown"})

def process_all_pdfs(directory, output_dir):
    if not path.exists(output_dir):
        makedirs(output_dir)
    images_dir = path.join(output_dir, 'images')
    if not path.exists(images_dir):
        makedirs(images_dir); del images_dir
    pdf_paths = []
    for root, dirs, files in walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_paths.append(path.join(root, file))
    print("Number of pdfs files found in ", directory, ": ", len(pdf_paths))
    try:
        list(process_pdf(pdf_path, output_dir) for pdf_path in tqdm(pdf_paths[:1], total=len(pdf_paths[:1]), desc=f"Processing {directory} PDFs"))
    except Exception as e:
        print(e)
    DataFrame(not_extracted).to_csv(path.join(output_dir, f"notExtracted-eng_pdfs.csv"), encoding = 'utf-8', index=False, mode = "w", header=True)

if __name__ == "__main__":
    pdf_directory = "../../../pdfs/"
    output_directory = "../../../extracted_data/eng/"
    process_all_pdfs(pdf_directory, output_directory)
