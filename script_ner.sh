# train CoNLL03
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=conll_ner
export TEXT_RESULT=test_result.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 train_ner.py --data_dir data/labeled/conll_2003/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict \
--overwrite_output_dir



# train WikiANN Nepali
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=wikiann_ner
export TEXT_RESULT=test_result.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0 python3 train_ner.py --data_dir data/labeled/wikiann_ne/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict \
--overwrite_output_dir


# train WikiANN Hindi
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=wikiann_hiner
export TEXT_RESULT=test_result.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 train_ner.py --data_dir data/labeled/wikiann_hi/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict \
--overwrite_output_dir


# train Singh NER
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=singh_ner
export TEXT_RESULT=test_result.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 train_ner.py --data_dir data/labeled/singh_ner/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_train \
--do_eval \
--do_predict \
--overwrite_output_dir


# Transfer from CoNLL03
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=conll_ner
export TEXT_RESULT=conll_nep.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0 python3 train_ner.py --data_dir data/labeled/singh_ner/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_predict \
--overwrite_output_dir


# Transfer from WikiANN Nepal
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=wikiann_ner
export TEXT_RESULT=wiki_nep.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0 python3 train_ner.py --data_dir data/labeled/singh_ner/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_predict \
--overwrite_output_dir

# Transfer from WikiANN Hindi
export MAX_LENGTH=164
export BERT_MODEL=bert-base-multilingual-cased
export OUTPUT_DIR=wikiann_hiner
export TEXT_RESULT=wiki_hi.txt
export TEXT_PREDICTION=test_predictions.txt
export BATCH_SIZE=32
export NUM_EPOCHS=20
export SAVE_STEPS=10000
export SEED=1

CUDA_VISIBLE_DEVICES=0 python3 train_ner.py --data_dir data/labeled/singh_ner/ \
--model_type bert \
--model_name_or_path $BERT_MODEL \
--output_dir $OUTPUT_DIR \
--test_result_file $TEXT_RESULT \
--test_prediction_file $TEXT_PREDICTION \
--max_seq_length  $MAX_LENGTH \
--num_train_epochs $NUM_EPOCHS \
--per_gpu_train_batch_size $BATCH_SIZE \
--save_steps $SAVE_STEPS \
--seed $SEED \
--do_predict \
--overwrite_output_dir

wikiann: 32.77	73.09
conll03: 59.98
nepali_ner: 86.10

2301 329 658
