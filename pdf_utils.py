import fitz  # PyMuPDF
from classifier import classify_page  # Assumes this function is defined to return 'blank' or other labels

def auto_clean_pdf(input_path, output_path, rotate_pages=None, bookmarks=None, request_files=None):
    doc = fitz.open(input_path)
    new_doc = fitz.open()

    rotate_pages = rotate_pages or {}
    bookmarks = bookmarks or {}
    request_files = request_files or {}

    for page_num, page in enumerate(doc):
        text = page.get_text().strip()
        label = classify_page(text)
        print(f"Page {page_num + 1}: Text length = {len(text)}, Label = {label}")

        if label.lower() == "blank":
            continue  # Skip blank pages

        # Copy page into new_doc
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        new_page = new_doc[-1]

        # Apply rotation
        if str(page_num + 1) in rotate_pages:
            angle = int(rotate_pages[str(page_num + 1)])
            new_page.set_rotation(angle)

        # Apply bookmarks (image or text)
        page_bookmarks = bookmarks.get(str(page_num + 1), [])
        for mark in page_bookmarks:
            x = float(mark.get("x", 50))
            y = float(mark.get("y", 50))
            w = float(mark.get("width", 100))
            h = float(mark.get("height", 100))

            if mark["type"] == "text":
                txt = mark.get("text", "")
                new_page.insert_text((x, y), txt, fontsize=12, color=(1, 0, 0))  # Red text

            elif mark["type"] == "image":
                image_id = mark.get("image_id", "")
                if image_id in request_files:
                    try:
                        image_file = request_files[image_id]
                        image_bytes = image_file.read()
                        rect = fitz.Rect(x, y, x + w, y + h)
                        new_page.insert_image(rect, stream=image_bytes)
                    except Exception as e:
                        print(f"⚠️ Error inserting image on page {page_num + 1}: {e}")
                else:
                    print(f"⚠️ Missing image file for ID: {image_id}")

    # Optional: Add table of contents from first text bookmark per page
    toc = []
    for p_num_str, marks in bookmarks.items():
        for mark in marks:
            if mark["type"] == "text":
                toc.append([1, mark["text"], int(p_num_str)])
                break

    if toc:
        new_doc.set_toc(toc)

    if len(new_doc) == 0:
        raise ValueError("❌ All pages were removed. Cannot create a PDF with zero pages.")

    new_doc.save(output_path)
    return output_path


