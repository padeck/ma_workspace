#!/usr/bin bash

for dataset in 'stackoverflow'
do
    for known_cls_ratio in 0.25 0.5 0.75
    do
        for labeled_ratio in 1.0 0.2 0.4 0.6 0.8
        do
            for seed in 0 1 2 3 4 5 6 7 8 9
            do 
                python run.py \
                --dataset $dataset \
                --method 'ARPL' \
                --known_cls_ratio $known_cls_ratio \
                --labeled_ratio $labeled_ratio \
                --seed $seed \
                --backbone 'bert' \
                --config_file_name 'ARPL' \
                --pretrain \
                --train \
                --loss_fct 'ARPLoss' \
                --gpu_id '0' \
                --results_file_name 'results_ARPL.csv' \
                --save_results
            done
        done
    done
done