from utils.logging import setup_logging

logger = setup_logging()

def format_index_to_json(index_data: dict, pdf_key: str) -> dict:
    try:
        output_json = {
            'index_id': index_data.get('index_id', pdf_key),
            'pdf_key': pdf_key,
            'metadata': index_data.get('metadata', {}),
            'status': 'processed'
        }
        logger.info(f"Índice JSON formateado para {pdf_key}")
        return output_json
    except Exception as e:
        logger.error(f"Error al formatear JSON del índice: {e}")
        raise e

def format_response_to_json(query: str, response: str, index_id: str) -> dict:
    try:
        output_json = {
            'query': query,
            'response': response,
            'index_id': index_id,
            'status': 'answered'
        }
        logger.info(f"Respuesta JSON formateada para consulta: {query}")
        return output_json
    except Exception as e:
        logger.error(f"Error al formatear JSON de respuesta: {e}")
        raise e