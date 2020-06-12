LABEL = "unlabeled"
TMP = "tmp2"
YOUTUBE_FILE_PATH = "youtube_list_{}.txt".format(LABEL)
AUDIO_PATH = "/{}/b07902048/audios/{}/".format(TMP, LABEL)
SEPARATE_PATH = "/{}/b07902048/separated/{}/".format(TMP, LABEL)
PIC_PATH = "/{}/b07902048/pic/{}/".format(TMP, LABEL)

MIR500_PATH = "/{}/b07902048/MIR-ST500/".format(TMP)
DATASET_PATH = "/{}/b07902048/dataset/".format(TMP)
DATASET_SIZE = 150000


LOWEST_SEMI = 40 ## make_ground_truth.py
HIGHTEST_SEMI = 80 ## make_ground_truth.py

FRAME_SIZE = 128
OVERLAP_SIZE = (128 - 32)
PRETRAIN_MODEL_PATH = "/home/student/07/b07902048/SCB/model/pre_train_model"
MODEL_PATH = '/home/student/07/b07902048/SCB/model/ckpt.h5'
