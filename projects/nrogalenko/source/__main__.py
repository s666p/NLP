import nltk
from text_annotation.text_processor import process_file
from typos_correction.corrupted_text_processor import process_corrupted_file
from text_vectorization.vectorize import build_frequency_dict_and_term_doc_matrix
from text_vectorization.w2v import w2v_train, create_doc_embeddings_file
from text_vectorization.vector_demo import test_w2v_and_tfidf_models, test_different_w2v_models
from topic_modelling.data_preprocessing import build_csr_term_doc_matrix
from topic_modelling.lda_model import train_lda_model, use_lda_model
from topic_modelling.lda_visualize import create_plot


def main():
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('punkt')
    nltk.download('stopwords')

    # lab 1 - text annotation
    process_file('../assets/train.csv', 'train')
    process_file('../assets/test.csv', 'test')

    # lab 2 - typos correction
    process_corrupted_file("../assets/test-corrupted.csv", "../assets/test")

    # lab 3 - vectorization
    build_frequency_dict_and_term_doc_matrix("../assets/train", 10, "../assets/train-dict-improved.json",
                                             "../assets/train-td-matrix")
    w2v_train("../assets/little-test.csv", 5, 100, 5, "../assets/w2v-train-model_100_5.bin")
    w2v_train("../assets/train.csv", 10, 100, 5, "../assets/w2v-train-model_100_10.bin")
    w2v_train("../assets/train.csv", 10, 300, 5, "../assets/w2v-train-model_300_10.bin")
    test_different_w2v_models(["../assets/w2v-train-model_100_5.bin",
                               "../assets/w2v-train-model_100_10.bin",
                               "../assets/w2v-train-model_300_10.bin"])
    test_w2v_and_tfidf_models("../assets/w2v-train-model_100_5.bin", "../assets/train-td-matrix.csv")
    create_doc_embeddings_file("../assets/w2v-train-model_100_5.bin",
                               "../assets/test.csv",
                               "../assets/train-dict.json",
                               "../assets/train-td-matrix.csv",
                               "../assets/annotated-corpus/test-embeddings.tsv")

    # lab 4 - lda topic modelling
    build_csr_term_doc_matrix("../assets/train", 5, "../assets/train-dict-improved.json", "../assets/train-td-matrix.npz")
    iterations_num_list = [5, 10, 20]
    topics_num_list = [2, 4, 5, 10, 20, 30, 40]
    top_words_to_display_num = 10
    for iterations_num in iterations_num_list:
        print(str(iterations_num))
        for topics_num in topics_num_list:
            print(str(topics_num))
            train_lda_model(topics_num, iterations_num, "../assets/train-td-matrix.npz")
            use_lda_model("../assets/lda-models/lda_model_" + str(iterations_num) + "_" + str(topics_num) + ".jl",
                          "../assets/train-dict-improved.json", "../assets/train-td-matrix.npz", "../assets/train.csv",
                          "../assets/test-td-matrix.npz", top_words_to_display_num)
    create_plot("../assets/topic-modelling-results/perplexity")


if __name__ == "__main__":
    main()
