import random
import numpy as np
import trax
from trax import layers as tl
import gc
from trax.supervised import training

def ReformerLM(vocab_size=33000, n_layers=2, mode='train', attention_type=tl.SelfAttention):
    model = tl.Serial( 
                trax.models.reformer.ReformerLM(vocab_size=vocab_size,n_layers=n_layers,mode=mode,attention_type=attention_type)
            ,tl.LogSoftmax())        
    return model

def tokenize(sentence, vocab_file, vocab_dir):
    return list(trax.data.tokenize(iter([sentence]), vocab_file=vocab_file, vocab_dir=vocab_dir))[0]

def detokenize(tokens, vocab_file, vocab_dir):
    return trax.data.detokenize(tokens, vocab_file=vocab_file, vocab_dir=vocab_dir)

def ReformerLM_output_gen(ReformerLM, start_sentence, vocab_file, vocab_dir, temperature, tokenize=tokenize):
    input_tokens = tokenize(start_sentence, vocab_file=vocab_file, vocab_dir=vocab_dir)
    input_tokens_with_batch = np.array(input_tokens)[None, :]
    output_gen = trax.supervised.decoding.autoregressive_sample_stream( 
        ReformerLM,
        inputs=input_tokens_with_batch,
        temperature=temperature
    )
    return output_gen

def generate_dialogue(ReformerLM, model_state, start_sentence, vocab_file, vocab_dir, max_len, temperature):
    delimiter_1 = ' Person 1: ' 
    delimiter_2 = ' Person 2: '
    sentence = ''
    counter = 0
    result = [tokenize(': ', vocab_file=vocab_file, vocab_dir=vocab_dir)]
    ReformerLM.state = model_state

    output = ReformerLM_output_gen(ReformerLM, start_sentence, vocab_file=VOCAB_FILE, vocab_dir=VOCAB_DIR, temperature=temperature)
    print(start_sentence.replace("Person","NLP-Agent").split(delimiter_2.replace("Person","NLP-Agent"))[0].strip())
    for o in output:    
        result.append(o)
        sentence = detokenize(np.concatenate(result, axis=0), vocab_file=VOCAB_FILE, vocab_dir=VOCAB_DIR)
       
        if sentence.endswith(delimiter_1):
            sentence = sentence.split(delimiter_1)[0].split("Person")[0]
            sentence =sentence.replace("\"","");
            return sentence

        elif sentence.endswith(delimiter_2):
            sentence = sentence.split(delimiter_2)[0].split("Person")[0]
            sentence =sentence.replace("\"","");
            return sentence

        counter += 1
        if counter > max_len:
            break
    return sentence  

def attention(*args, **kwargs):
    kwargs['predict_mem_len'] = 120
    kwargs['predict_drop_len'] = 120
    return tl.SelfAttention(*args, **kwargs)

VOCAB_FILE = 'en_32k.subword'
VOCAB_DIR = 'projects/vocabs'

shape11 = trax.shapes.ShapeDtype((1, 1), dtype=np.int32)
model = ReformerLM(
    vocab_size=33000,
    n_layers=6,
    mode='predict',
    attention_type=attention,
)
results = model.init_from_file('projects/chatmodel.pkl.gz',weights_only=True, input_signature=shape11)
STARTING_STATE = model.state