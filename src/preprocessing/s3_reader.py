import boto3
import os
from utils.logging import setup_logging

logger = setup_logging()
s3 = boto3.client('s3')

def download_pdf_from_s3(bucket: str, key: str, save_path: str):
    """
    Descarga un PDF desde un bucket de S3 y lo guarda en save_path.

    Args:
        bucket (str): Nombre del bucket de S3 (ej: ragpdfs2025hybrid).
        key (str): Clave del archivo en S3 (ej: pdfs/file.pdf).
        save_path (str): Ruta local donde guardar el PDF.

    Returns:
        str: Ruta del archivo PDF descargado.
    """
    try:
        logger.info(f"Descargando PDF desde s3://{bucket}/{key}")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        s3.download_file(bucket, key, save_path)
        logger.info(f"PDF descargado en {save_path}")
        return save_path
    except Exception as e:
        logger.error(f"Error al descargar PDF desde s3://{bucket}/{key}: {e}")
        raise e