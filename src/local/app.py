from flask import Flask, request, jsonify
import os
import urllib.parse
from src.preprocessing.s3_reader import download_pdf_from_s3
from src.preprocessing.index_builder import build_index
from src.preprocessing.json_formatter import format_index_to_json, format_response_to_json
from src.local.rag import setup_rag_agent
from src.local.index_loader import load_index
from utils.logging import setup_logging

app = Flask(__name__)
logger = setup_logging()

index_cache = {}

@app.route('/process', methods=['POST'])
def process_json():
    try:
        input_json = request.get_json()
        request_type = input_json.get('type')

        if request_type == 'preprocess':
            pdf_url = input_json.get('pdf_url')
            pdf_key = input_json.get('key')
            if not pdf_url or not pdf_key:
                return jsonify({'error': 'Faltan pdf_url o key'}), 400

            # Extraer bucket y key desde la URL
            parsed_url = urllib.parse.urlparse(pdf_url)
            bucket = parsed_url.netloc.split('.')[0]
            key = parsed_url.path.lstrip('/')

            # Descargar PDF usando boto3
            pdf_dir = 'data/pdfs'
            save_path = os.path.join(pdf_dir, pdf_key)
            download_pdf_from_s3(bucket, key, save_path)

            # Construir índice
            persist_dir = f'data/indices/{pdf_key}'
            index_data = build_index([save_path], persist_dir)

            # Formatear respuesta
            output_json = format_index_to_json(index_data, pdf_key)
            return jsonify(output_json), 200

        elif request_type == 'query':
            query = input_json.get('query')
            index_id = input_json.get('index_id')
            if not query or not index_id:
                return jsonify({'error': 'Faltan query o index_id'}), 400

            if index_id not in index_cache:
                persist_dir = f'data/indices/{index_id}'
                index_cache[index_id] = load_index(persist_dir)
            vector_index = index_cache[index_id]

            agent = setup_rag_agent(vector_index)
            response = agent.query(query)

            output_json = format_response_to_json(query, str(response), index_id)
            return jsonify(output_json), 200

        else:
            return jsonify({'error': 'Tipo de solicitud inválido'}), 400

    except Exception as e:
        logger.error(f"Error al procesar JSON: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)