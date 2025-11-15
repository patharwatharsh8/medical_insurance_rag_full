from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.node_parser import SentenceSplitter

def chunk_text(full_text: str, method="recursive"):
    if method == "fixed":
        splitter = SentenceSplitter(chunk_size=800, chunk_overlap=100)
        return splitter.split_text(full_text)

    elif method == "semantic":
        parser = SemanticSplitterNodeParser(batch_size=20)
        nodes = parser.get_nodes_from_documents([full_text])
        return [n.text for n in nodes]

    splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=150)
    return splitter.split_text(full_text)
