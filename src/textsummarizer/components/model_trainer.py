from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk
import torch
from textsummarizer.entity.config_entity import ModelTrainerConfig



from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq, Trainer, TrainingArguments
from datasets import load_from_disk
import torch
import os

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def preprocess_data(self, dataset, tokenizer):
        def tokenize_function(examples):
            model_inputs = tokenizer(examples['dialogue'], padding="max_length", truncation=True)
            with tokenizer.as_target_tokenizer():
                labels = tokenizer(examples['summary'], padding="max_length", truncation=True)
            model_inputs['labels'] = labels['input_ids']
            return model_inputs
        
        return dataset.map(tokenize_function, batched=True)

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        dataset_samsum_pt = self.preprocess_data(dataset_samsum_pt, tokenizer)

        # Trainer arguments
        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=1, warmup_steps=500,
            per_device_train_batch_size=1, per_device_eval_batch_size=1,
            weight_decay=0.01, logging_steps=10,
            evaluation_strategy='steps', eval_steps=500, save_steps=1e6,
            gradient_accumulation_steps=16
        )

        # Trainer setup
        trainer = Trainer(model=model_pegasus, args=trainer_args,
                          tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                          train_dataset=dataset_samsum_pt["test"], 
                          eval_dataset=dataset_samsum_pt["validation"])
        

        # Save the model and tokenizer
        model_pegasus.save_pretrained(os.path.join(self.config.root_dir, "pegasus-samsum-model"))
        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))
