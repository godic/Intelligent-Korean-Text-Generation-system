from tensorflow.keras.utils import to_categorical
import numpy as np
import util
from CustomLayers import generator

corpus = np.load("../data/corpus.npy", allow_pickle=True)
code2vec = util.loadIcode(val="vec")
char2id = util.loadChar(val="id")
id2char = util.loadChar(val="dict")

batch_size = 700
seq_length = 2
char_size = 2276
max_len = 52
corpus_size = corpus.shape[0]
print("init")

# corpus_max_len = np.array([])
# for i in range(corpus.shape[0] // batch_size):
#   top_len = 0
#   for j in range(batch_size):
#     if top_len < corpus[i * batch_size + j][0].shape[0]:
#       top_len = corpus[i * batch_size + j][0].shape[0]
#   corpus_max_len = np.append(corpus_max_len, top_len)
# print(corpus_max_len)

# generator
# from tensorflow.keras.utils import to_categorical
#
#
# def generator(corpus, batch_size, max_len):
#     size = corpus.shape[0]
#
#     while True:
#         for i in range(size // batch_size):
#             idx_end = [2275 for i in range(int(max_len[i]))]
#             x_batch = np.array([idx_end for i in range(batch_size)])
#             y_batch = np.array([idx_end for i in range(batch_size)])
#             icode_batch = np.array(
#                 [[[0 for i in range(14)] for k in range(int(max_len[i]))] for j in range(batch_size)], dtype="float")
#
#             for j in range(batch_size):
#                 now = i * batch_size + j
#                 x_batch[j][:corpus[now][0].shape[0] - 1] = corpus[now][0][:-1]
#                 y_batch[j][:corpus[now][0].shape[0] - 1] = corpus[now][0][1:]
#                 icode_batch[j] = corpus[now][1]
#
#             x_batch = to_categorical(x_batch)
#             y_batch = to_categorical(y_batch)
#
#             yield [x_batch, icode_batch], y_batch
#
#
# print("generator")
#
#
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense, LSTM, TimeDistributed, Input, concatenate
# from keras import backend as K
# K.clear_session()
#
#
# seq_input = Input(shape=(None, char_size), name="seq_input")
# lstm1 = LSTM(256, return_sequences=True)(seq_input)
#
# icode_input = Input(shape=(None, 14), name="icode_input")
#
# ann = concatenate([lstm1, icode_input])
# ann = TimeDistributed(Dense(2276, activation='softmax', name="output"))(ann)
#
# model = Model(inputs=[seq_input, icode_input], outputs=[ann])
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.summary()
# model.fit(generator(corpus, batch_size, corpus_max_len), steps_per_epoch=corpus_size//batch_size, epochs=50, verbose=1)
# model.save('20200806_v1.h5')

from keras.models import load_model
model = load_model('20200806_v1.h5')

def weightedPick(weight):
    t = np.cumsum(weight)
    s = np.sum(weight)

    return np.searchsorted(t, np.random.rand(1) * s)


def sentence_generation(model, length):
    ix = [np.random.randint(2276)]
    y_char = [id2char[ix[-1]]]
    print(ix[-1], '번 글자', y_char[-1], '로 예측을 시작!')

    # X = np.zeros((1, 2, 2276))  # (1, 2, 2276) 크기의 X 생성. 즉, LSTM의 입력 시퀀스 생성
    Y = np.zeros((1, length, 14))
    Y[0] = np.array(code2vec['Q05A08'])
    X = np.zeros((1, length, 2276))

    for i in range(0, length):
        # X[0][0] = X[0][1]
        # X[0][1][ix[-1]] = 1  # X[0][i%2][예측한 글자의 인덱스] = 1, 즉, 예측 글자를 다음 입력 시퀀스에 추가
        X[0][i][ix[-1]] = 1

        # ix = weightedPick(model.predict([X, Y])[0][-1])
        ix = weightedPick(model.predict([X[:, :i+1, :],Y[:, :i+1, :]])[0][-1])

        y_char.append(id2char[ix[-1]])

    return ('').join(y_char)


print(sentence_generation(model, 10))