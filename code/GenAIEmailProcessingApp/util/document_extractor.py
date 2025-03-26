from pathlib import Path
from llama_index.core import SimpleDirectoryReader

from llama_index.readers.file import UnstructuredReader

def read_data_from_dir():
    dir_reader = SimpleDirectoryReader(
        "D:\\git\\gaied-gen-ai-coders\\code\\GenAIEmailProcessingApp\\samples",
        file_extractor={
            ".pdf": UnstructuredReader(),
            ".msg": UnstructuredReader(),
            ".eml": UnstructuredReader(),
        },
    )
    documents = dir_reader.load_data()

    # Print the documents data
    print(documents)

def read_data_from_file(file_path):
    loader = UnstructuredReader()
    documents = loader.load_data(
        unstructured_kwargs={"filename": file_path}
    )
    return documents

