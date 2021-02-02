FILE=$1

if [ $FILE == "2000-pretrained" ]; then
    URL=https://drive.google.com/drive/folders/1BDhtEjzXHg-DvqgEHKdM06vPSeBmuMxz?usp=sharing
    mkdir -p ./expr/checkpoints/
    OUT_FILE=./expr/checkpoints/002000_nets_ema.ckpt
    wget -N $URL -O $OUT_FILE

else
    echo "re"
    exit 1
fi
