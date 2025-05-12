from src.preprocessing.s3_reader import read_pdfs
from src.preprocessing.index_builder import build_index
from src.preprocessing.s3_writer import write_index
from utils.logging import setup_logging
from config.settings import S3_INPUT_PREFIX

logger = setup_logging()

def main():
    logger.info("Starting preprocessing")
    persist_dir = "data/jsonfiles"
    pdf_files = read_pdfs(S3_INPUT_PREFIX)
    build_index(pdf_files, persist_dir)
    write_index(persist_dir)
    logger.info("Preprocessing complete")

if __name__ == "__main__":
    main()