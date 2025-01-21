from keybert import KeyBERT
from transformers import AutoTokenizer, AutoModelForTokenClassification


TRANSFORMER_MODEL = "jjzha/jobbert_knowledge_extraction"
TRANSFORMER_TOKENIZER = AutoTokenizer.from_pretrained(TRANSFORMER_MODEL)
TRANSFORMER_LLM = AutoModelForTokenClassification.from_pretrained(TRANSFORMER_MODEL)


class KeywordExtractor:
    def __get_relevant_tokens(self, tokens, logits):
        zipped = [(x, y) for x, y in zip(logits, tokens)]

        results = []
        adding = False
        current = []

        for (label, token) in zipped:
            if label == 2:
                if not adding:
                    continue
                else:
                    results.append(current)
                    current = []
                    adding = False
            else:
                if label == 1:
                    current.append(token)
                elif label == 0:
                    if not adding:
                        adding = True
                        current.append(token)
                    else:
                        if token != 1116:
                            results.append(current)
                            current = []
                        current.append(token)
        
        return results

    def __token_matcher():
        pass
    
    def __reconstruct_keywords(self, tokens):
        decoded = [TRANSFORMER_TOKENIZER.decode(result) for result in tokens]

        print(decoded)

        true_results = []
        in_list = False
        slash_found = False
        last_token_was_added_slash = False
        last_token_was_added_minus = False

        for token in decoded:
            if in_list:
                if token.startswith("##") and len(token) >= 3 and len(true_results):
                    true_results[-1] += token[2:]
                else:
                    true_results[-1] += token
                if token.endswith(")"):
                    in_list = False
                continue
            if token.startswith("##") and len(token) >= 3 and len(true_results):
                true_results[-1] += token[2:]
                if last_token_was_added_slash and len(true_results) >= 2:
                    true_results[-2] += token[2:]
            elif token.startswith("+"):
                true_results[-1] += token
                if last_token_was_added_slash and len(true_results) >= 2:
                    true_results[-2] += token
            elif token.endswith("-"):
                true_results[-1] += token
                if last_token_was_added_slash and len(true_results) >= 2:
                    true_results[-2] += token
                last_token_was_added_minus = True
            elif token == "/":
                slash_found = True
            elif len(true_results) and true_results[-1].endswith("("):
                in_list = True
                true_results[-1] += token
            else:
                if last_token_was_added_minus:
                    last_token_was_added_minus = False
                    true_results[-1] += token
                    continue
                if last_token_was_added_slash:
                    last_token_was_added_slash = False
                if slash_found:
                    slash_found = False
                    last_token_was_added_slash = True
                    true_results.append(true_results[-1] + "/" + token)
                true_results.append(token)
        
        return true_results
    
    def get_keywords(self, text):
        inputs = TRANSFORMER_TOKENIZER.encode(text, return_tensors="pt")
        outputs = TRANSFORMER_LLM(inputs)

        relevant_tokens = self.__get_relevant_tokens(inputs[0], outputs.logits.argmax(-1)[0])

        reconstructed_tokens = self.__reconstruct_keywords(relevant_tokens)
        
        keywords = set(list(filter(lambda x: len(x) > 1 or x.lower() == "c", reconstructed_tokens)))
        keywords = set(list(map(lambda x: x.lower(), keywords)))
        
        if not keywords:
            used_fallback = True
            kw_model = KeyBERT()
            keywords = list(map(lambda x: x[0].lower(), kw_model.extract_keywords(text, top_n=20, keyphrase_ngram_range=(1, 2))))
        else:
            used_fallback = False

        with open("artifacts/topics.txt", "w+") as f:
            f.write("\n".join(keywords | {"*** Fallback used ***" if used_fallback else "*** Fallback not used ***"}))

        return keywords


if __name__ == "__main__":
    def read_posting():
        with open("input/posting.txt", "r+") as f:
            return f.read()

    print(KeywordExtractor().get_keywords(read_posting()))
