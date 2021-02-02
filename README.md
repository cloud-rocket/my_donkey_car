# my_donkey_car


## Running

```
LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1 python3 manage.py drive --model=./models/linear2.tflite --type=tflite_linear
```



## Image classification

```
cd ~/projects
git clone https://github.com/dusty-nv/jetson-inference/
cd jetson-inference

git submodule update --init
```

## Model analysis

```
donkey tubplot --tub ./data/tub_175_20-11-15/ --model ./models/linear4.h5 --limit -1
```