#!/usr/bin bash

for dataset in  'banking' 'clinc' 'stackoverflow' 
do
    for cluster_num_factor in 1.0 2.0 3.0 4.0
    do
        for seed in 0  1 2 3 4 5 6 7 8 9
        do
            python run.py \
            --dataset $dataset \
            --method 'KM' \
            --setting 'unsupervised' \
            --seed $seed \
            --backbone 'glove' \
            --cluster_num_factor $cluster_num_factor \
            --known_cls_ratio 0 \
            --config_file_name 'KM' \
            --gpu_id '0' \
            --train \
            --save_results \
            --results_file_name 'results_KM.csv'
        done
    done
done
