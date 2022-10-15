from PIL import Image
import pytesseract 

image_path = r"C:\Python Project\capstone\0\number.jpg"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
text = pytesseract.image_to_string(Image.open(image_path), lang = "kor")
print(text)
