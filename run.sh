#!/bin/bash
# run_eval.sh

MODEL="Ling-2.5-1T"
OUTPUT="results.csv"
TMP_DIR="tmp_results"
MAX_TURNS=100
MAX_PARALLEL=64

GAMES=(100 1000 1003 1004 1005 1007 1008 1010 1011 1012 1013 1014 1015 102 103 105 106 107 11 113 117 120 122 123 126 132 133 134 136 137 140 142 144 146 147 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 172 176 177 178 180 181 182 183 184 185 186 187 189 19 190 191 193 194 196 197 2 202 206 209 21 210 211 212 213 214 215 217 218 22 220 221 222 223 224 225 226 23 230 233 234 235 24 240 25 253 256 257 258 26 262 266 267 269 271 274 275 277 279 281 282 284 286 288 290 291 293 295 298 30 302 305 306 313 314 316 318 319 32 325 326 329 331 334 335 341 343 344 345 349 35 351 353 36 362 364 367 378 379 385 386 39 394 4 40 405 408 409 415 419 42 422 423 424 428 43 435 438 441 442 444 445 446 449 452 454 456 46 461 463 472 473 475 476 477 479 481 482 483 484 486 488 489 490 491 493 494 495 496 497 498 500 501 502 503 504 505 507 509 51 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 53 530 531 532 533 534 535 536 537 538 539 540 541 543 544 545 546 547 548 549 550 551 552 554 556 557 558 559 561 562 563 564 565 566 567 568 569 571 574 575 578 579 581 582 584 586 588 592 600 606 608 609 611 613 616 62 625 628 629 631 635 637 639 64 646 65 651 652 654 655 658 659 662 667 668 671 675 68 685 686 688 689 693 694 699 700 702 704 705 709 713 715 716 717 718 719 72 720 731 733 736 737 740 742 743 744 745 747 750 751 755 756 759 762 766 77 770 776 778 781 782 783 789 794 796 797 800 804 805 806 807 810 811 812 813 815 816 818 82 820 821 822 826 833 836 837 84 840 843 844 846 848 849 850 851 852 853 856 857 858 859 860 862 865 866 867 869 872 875 881 883 890 891 893 896 898 9 907 91 92 920 922 923 924 925 926 927 928 929 930 932 933 935 937 938 939 94 940 945 948 952 953 958 96 961 962 963 964 967 969 971 972 973 977 979 98 980 981 983 984 986 987 988 989 99 990 991 992 993 994 996 997 999)

mkdir -p "$TMP_DIR"

run_job() {
    local game_idx=$1
    local diff=$2
    local lang=$3
    local ctx=$4
    local tmp_file="${TMP_DIR}/Game${game_idx}_d${diff}_${lang}_c${ctx}"
    # 如果结果文件已存在则跳过
    if [ -f "${tmp_file}" ]; then
        echo "[Skip] ${tmp_file} already exists"
        return 0
    fi
    python main.py \
        --model      "$MODEL" \
        --game       "GAME${game_idx}" \
        --difficulty "$diff" \
        --language   "$lang" \
        --context    "$ctx" \
        --max-turns  "$MAX_TURNS" \
        --eval-mode  "standard" \
        --output     "$tmp_file"
}

export -f run_job
export MODEL MAX_TURNS TMP_DIR

# 生成所有任务
jobs=()
for i in "${GAMES[@]}"; do
    for diff in 1 2 3 4 5; do
        for lang in en; do
            for ctx in 0 1 2 3 4 5; do
                jobs+=("$i $diff $lang $ctx")
            done
        done
    done
done

total=${#jobs[@]}
echo "[Info] Total jobs: $total | Parallel: $MAX_PARALLEL | Model: $MODEL"

# 分批并发
for (( start=0; start<total; start+=MAX_PARALLEL )); do
    batch=("${jobs[@]:$start:$MAX_PARALLEL}")
    echo "[Batch] $(( start/MAX_PARALLEL + 1 )) / $(( (total + MAX_PARALLEL - 1) / MAX_PARALLEL ))"
    for job in "${batch[@]}"; do
        read -r i diff lang ctx <<< "$job"
        run_job "$i" "$diff" "$lang" "$ctx" &
    done
    wait
    echo "[Batch done]"
done

# 合并所有临时 CSV
echo "[Merge] Merging results into $OUTPUT ..."
header_written=false
for f in "$TMP_DIR"/*.csv; do
    [ -f "$f" ] || continue
    if [ "$header_written" = false ]; then
        cat "$f" >> "$OUTPUT"
        header_written=true
    else
        tail -n +2 "$f" >> "$OUTPUT"  # 跳过表头
    fi
done

rm -rf "$TMP_DIR"
echo "[All done] Results saved to $OUTPUT"