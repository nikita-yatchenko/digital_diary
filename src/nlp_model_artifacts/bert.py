import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class SentimentClassifier:
    def __init__(self) -> None:
        model_checkpoint = 'cointegrated/rubert-tiny-sentiment-balanced'
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

        self.max_len = 512

    def sentiment_predict(self, text: str) -> int:
        self.model.eval()

        _inputs, _masks = self.preprocess(text)

        with torch.no_grad():
            proba = torch.sigmoid(self.model(_inputs, _masks).logits).cpu().numpy()[0]

        return round(proba.dot([-1, 0, 1]), 2)

    def preprocess(self, text: str) -> tuple:
        encoded_sent = self.tokenizer.encode_plus(
            text=str(text),  # self._text_preprocessing(sent),  # Preprocess sentence
            add_special_tokens=True,  # Add `[CLS]` and `[SEP]`
            max_length=self.max_len,  # Max length to truncate/pad
            truncation=True,
            padding='max_length',  # Pad sentence to max length
            return_tensors="pt",
            return_attention_mask=True  # Return attention mask
        )

        input_ids = encoded_sent.get('input_ids')
        attention_masks = encoded_sent.get('attention_mask')

        # input_ids = torch.tensor(input_ids)
        # attention_masks = torch.tensor(attention_masks)

        bert_inputs = (input_ids, attention_masks)

        return bert_inputs


if __name__ == "__main__":
    model = SentimentClassifier()
    text = 'Всё хорошо!'
    print(model.sentiment_predict(text))
