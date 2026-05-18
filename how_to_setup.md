# WaveNet Setup Guide

## Install training data

Download the VCTK corpus from Kaggle:
https://www.kaggle.com/datasets/pratt3000/vctk-corpus?resource=download

Extract and place it so the directory structure looks like:

```
archive/
└── VCTK-Corpus/
    └── ...
```

## Set up Conda

```bash
conda create -n wavenet python=3.10 -y
conda activate wavenet
pip install -r requirements_locks.txt
```

**requirements_locks.txt:**
```
tensorflow==2.21.0
librosa==0.11.0
numpy==1.26.4
scipy==1.11.4
soundfile==0.13.1
tqdm==4.67.1
matplotlib==3.8.4
```

## Set up CUDA in TensorFlow (optional)

```bash
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
nvidia-smi
pip install tensorflow[and-cuda]==2.21.0
conda install -c conda-forge cudatoolkit=11.8 cudnn=8.9
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## Reset — delete Conda environment

```bash
conda deactivate
conda remove -n wavenet --all
```

## Run without GPU

```bash
CUDA_VISIBLE_DEVICES="" python train.py --data_dir=archive
```