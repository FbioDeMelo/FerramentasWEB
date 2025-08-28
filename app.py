from flask import Flask, render_template, request, send_file
import os
import io
from docx2pdf import convert
import uuid
import tempfile
import pythoncom
from werkzeug.utils import secure_filename 
from pdf2docx import Converter
from PIL import Image
import fitz  # PyMuPDF
import zipfile
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/compress')
def compress_page():
    return render_template('compress.html')
@app.route('/juntarpdf')
def juntarpdf():
    return render_template('juntarpdf.html')
@app.route('/decompress')
def decompress_page():
    return render_template('decompress.html')
@app.route('/pdfimg')
def pdfimg():
    return render_template('pdfimg.html')
@app.route('/atualizacoes')
def atua():
    return render_template('atualizacao.html')
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')
@app.route('/pdfword')
def pdfword():
    return render_template('pdfword.html')
@app.route('/textconverter')
def txtconvert():
    return render_template('textconverter.html')
@app.route('/wordpdf')
def wordpdf():
    return render_template('wordpdf.html')

@app.route('/imgpdf')
def imgpdf():
    return render_template('imgpdf.html')

@app.route('/convert-to-word', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400
    files = request.files.getlist('file')
    if len(files) == 0:
        return 'Nenhum arquivo selecionado.', 400

    pythoncom.CoInitialize()
    converted_files = []

    
    for file in files:
        if file and file.filename.endswith('.docx'):
            try:
                with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_docx:
                    file.save(temp_docx.name)
                
                output_dir = tempfile.mkdtemp()
                convert(temp_docx.name, output_dir)

                pdf_generated_name = os.path.splitext(os.path.basename(temp_docx.name))[0] + '.pdf'
                final_pdf_path = os.path.join(output_dir, pdf_generated_name)

                with open(final_pdf_path, 'rb') as f:
                    pdf_bytes = f.read()
                    pdf_name = secure_filename(file.filename).replace('.docx', '.pdf').replace('_', ' ')
                    converted_files.append((pdf_name, pdf_bytes))

            except Exception as e:
                return f"Erro ao converter {file.filename}: {e}", 500
            finally:
                os.unlink(temp_docx.name)

    pythoncom.CoUninitialize()

    if len(converted_files) > 1:
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, 'w') as zipf:
            for filename, filedata in converted_files:
                zipf.writestr(filename, filedata)
        zip_io.seek(0)
        return send_file(zip_io, as_attachment=True, download_name="convertidos.zip", mimetype='application/zip')

    print('teste',len(converted_files))
    filename, filedata = converted_files[0]
    return send_file(io.BytesIO(filedata), as_attachment=True, download_name=filename, mimetype='application/pdf')

# PDF → DOCX
# PDF → DOCX
@app.route('/convert-pdf', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400
    files = request.files.getlist('file')
    if len(files) == 0:
        return 'Nenhum arquivo selecionado.', 400

    converted_files = []

    for file in files:
        if file and file.filename.endswith('.pdf'):
            pdf_temp = None
            docx_temp = None
            try:
                pdf_temp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
                pdf_temp.write(file.read())
                pdf_temp.close()

                docx_temp = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
                docx_temp.close()

                cv = Converter(pdf_temp.name)
                cv.convert(docx_temp.name)
                cv.close()

                with open(docx_temp.name, 'rb') as f:
                    word_bytes = f.read()
                    word_name = secure_filename(file.filename).replace('.pdf', '.docx').replace('_', ' ')
                    converted_files.append((word_name, word_bytes))

            except Exception as e:
                return f"Erro ao converter {file.filename}: {e}", 500
            finally:
                if pdf_temp and os.path.exists(pdf_temp.name):
                    os.unlink(pdf_temp.name)
                if docx_temp and os.path.exists(docx_temp.name):
                    os.unlink(docx_temp.name)

    if len(converted_files) > 1:
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, 'w') as zipf:
            for filename, filedata in converted_files:
                zipf.writestr(filename, filedata)
        zip_io.seek(0)
        return send_file(zip_io, as_attachment=True, download_name="convertidos.zip", mimetype='application/zip')

    filename, filedata = converted_files[0]
    return send_file(io.BytesIO(filedata), as_attachment=True,
                     download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')


# PDF → Imagem
@app.route('/convert-pdf-img', methods=['POST'])
def convert_pdf_to_img():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400
    files = request.files.getlist('file')
    if len(files) == 0:
        return 'Nenhum arquivo selecionado.', 400
    converted_images = []
    for file in files:
        if file and file.filename.endswith('.pdf'):
            pdf_bytes = file.read()
            try:
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                basename = os.path.splitext(secure_filename(file.filename))[0].replace('_', ' ')
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img_io = io.BytesIO()
                    img.save(img_io, 'PNG')
                    img_io.seek(0)
                    filename = f"{basename} pagina {i+1}.png"
                    converted_images.append((filename, img_io.read()))
            except Exception as e:
                return f"Erro ao converter {file.filename}: {e}", 500
    if len(converted_images) > 1:
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, 'w') as zipf:
            for filename, filedata in converted_images:
                zipf.writestr(filename, filedata)
        zip_io.seek(0)
        return send_file(zip_io, as_attachment=True, download_name="imagens.zip", mimetype='application/zip')
    filename, img_data = converted_images[0]
    return send_file(io.BytesIO(img_data), as_attachment=True,
                     download_name=filename, mimetype='image/png')

# Compactar arquivos
@app.route('/compress', methods=['POST'])
def compress_files():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400
    files = request.files.getlist('file')
    if not files:
        return 'Nenhum arquivo selecionado.', 400

    # Pega o nome do formulário (campo zipname do HTML)
    user_filename = request.form.get("zipname", "").strip()

    # Se não informar nada, usa padrão
    if not user_filename:
        user_filename = "arquivos_comprimidos"

    # Garante que o nome é seguro e termina em .zip
    user_filename = secure_filename(user_filename)
    if not user_filename.lower().endswith(".zip"):
        user_filename += ".zip"

    # Monta o zip em memória
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                zipf.writestr(filename, file.read())
    zip_io.seek(0)

    return send_file(zip_io, as_attachment=True,
                     download_name=user_filename,
                     mimetype='application/zip')

# Descompactar arquivos
@app.route('/decompress', methods=['POST'])
def decompress_files():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400

    file = request.files['file']
    if not file.filename.endswith('.zip'):
        return 'Envie um arquivo ZIP válido.', 400

    zip_bytes = io.BytesIO(file.read())
    extracted_files = []

    try:
        with zipfile.ZipFile(zip_bytes, 'r') as zipf:
            for name in zipf.namelist():
                extracted_files.append((name, zipf.read(name)))
    except Exception as e:
        return f"Erro ao descompactar: {e}", 500

    if len(extracted_files) > 1:
        # Criar nome da pasta baseado no nome do ZIP enviado
        import os
        folder_name = os.path.splitext(file.filename)[0] + "/"

        # Reempacotar arquivos extraídos em um novo zip para download
        new_zip = io.BytesIO()
        with zipfile.ZipFile(new_zip, 'w', zipfile.ZIP_DEFLATED) as newzip:
            for filename, data in extracted_files:
                # Coloca todos dentro da pasta
                newzip.writestr(folder_name + filename, data)
        new_zip.seek(0)
        return send_file(new_zip, as_attachment=True,
                         download_name="arquivos_extraidos.zip",
                         mimetype='application/zip')

    # Se só tiver 1 arquivo dentro, baixar direto
    filename, data = extracted_files[0]
    return send_file(io.BytesIO(data), as_attachment=True,
                     download_name=filename)
# Unir PDFs
@app.route('/merge-pdf', methods=['POST'])
def merge_pdfs():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400
    files = request.files.getlist('file')
    if not files:
        return 'Nenhum arquivo selecionado.', 400

    writer = PdfWriter()
    for file in files:
        if file and file.filename.endswith('.pdf'):
            try:
                reader = PdfReader(io.BytesIO(file.read()))
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                return f"Erro ao mesclar {file.filename}: {e}", 500

    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    writer.close()
    output_pdf.seek(0)
    return send_file(output_pdf, as_attachment=True, download_name='pdf unificado.pdf', mimetype='application/pdf')

# Imagem → PDF
@app.route('/convert-img-pdf', methods=['POST'])
def convert_img_to_pdf():
    if 'file' not in request.files:
        return 'Nenhuma imagem enviada.', 400
    files = request.files.getlist('file')
    if len(files) == 0:
        return 'Nenhuma imagem selecionada.', 400
    images = []
    for file in files:
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            try:
                img = Image.open(file)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                return f"Erro ao processar {file.filename}: {e}", 500
    if not images:
        return 'Nenhuma imagem válida.', 400
    pdf_io = io.BytesIO()
    images[0].save(pdf_io, format='PDF', save_all=True, append_images=images[1:])
    pdf_io.seek(0)

    return send_file(pdf_io, as_attachment=True,
                     download_name='imagens convertidas.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
