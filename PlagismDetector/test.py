import logging

from vncorenlp import VnCoreNLP


annotator = VnCoreNLP(address="http://127.0.0.1", port=9000)

# Input


def simple_usage():
    # Uncomment this line for debugging
    # logging.basicConfig(level=logging.DEBUG)

    vncorenlp_file = (
        "D:\study\PlagismDetector\PlagismDetector/VnCoreNLP/VnCoreNLP-1.1.1.jar"
    )

    sentences = (
        "VTV đồng ý chia sẻ bản quyền World Cup 2018 cho HTV để khai thác. "
        "Nhưng cả hai nhà đài đều phải chờ sự đồng ý của FIFA mới thực hiện được điều này."
    )

    # Use "with ... as" to close the server automatically
    with VnCoreNLP(vncorenlp_file) as vncorenlp:
        print("Tokenizing:", vncorenlp.tokenize(sentences))
        print("POS Tagging:", vncorenlp.pos_tag(sentences))
        print("Named-Entity Recognizing:", vncorenlp.ner(sentences))
        print("Dependency Parsing:", vncorenlp.dep_parse(sentences))
        print("Annotating:", vncorenlp.annotate(sentences))
        print("Language:", vncorenlp.detect_language(sentences))

    # In this way, you have to close the server manually by calling close function
    vncorenlp = VnCoreNLP(vncorenlp_file)

    print("Tokenizing:", vncorenlp.tokenize(sentences))
    print("POS Tagging:", vncorenlp.pos_tag(sentences))
    print("Named-Entity Recognizing:", vncorenlp.ner(sentences))
    print("Dependency Parsing:", vncorenlp.dep_parse(sentences))
    print("Annotating:", vncorenlp.annotate(sentences))
    print("Language:", vncorenlp.detect_language(sentences))

    # Do not forget to close the server
    vncorenlp.close()


if __name__ == "__main__":
    text = "Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."

    # To perform word segmentation, POS tagging, NER and then dependency parsing
    annotated_text = annotator.annotate(text)

    # To perform word segmentation only
    word_segmented_text = annotator.tokenize(text)
