#!/usr/bin bash

for dataset in  'stackoverflow' 
do
    for cluster_num_factor in 1.0 
    do
        for seed in 0 
        do 
            python run.py \
            --dataset $dataset \
            --method 'UnsupUSNID' \
            --setting 'unsupervised' \
            --known_cls_ratio 0 \
            --seed $seed \
            --train \
            --config_file_name 'UnsupUSNID' \
            --cluster_num_factor $cluster_num_factor \
            --backbone 'bert_USNID_Unsup' \
            --gpu_id '1' \
            --results_file_name 'results_unsupervised.csv' \
            --save_results \
            --output_dir '../' 
        done
    done
done

 