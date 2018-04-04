import tensorflow as tf
import numpy as np
class NN_Regression:
    def seq_length(self, sequence):
        used = tf.sign(tf.reduce_max(tf.abs(sequence), reduction_indices=2))
        length = tf.reduce_sum(used, reduction_indices=1)
        length = tf.cast(length, tf.int32)
        return length

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.1, dtype=tf.float64)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    def __init__(self, data, label, seq_length, dim, batch_size):
        self.data = data
        self.label = label

        self.Expectation_Time = 24
        self.batch_size = batch_size

        self.rnn_Cell = tf.nn.rnn_cell.BasicLSTMCell(100)
        self.rnn_Cell2 = tf.nn.rnn_cell.BasicLSTMCell(1)

        self.Weight_Output = self.weight_variable(shape=[1, 100, 1])

        self.sequence_Length = seq_length

        self.Batch_Size = batch_size - self.sequence_Length - self.Expectation_Time + 1

        DataLength = 432

        self.x = tf.placeholder(dtype=tf.float64, shape=[None, self.sequence_Length, dim])
        self.y = tf.placeholder(dtype=tf.float64, shape=[None, self.sequence_Length, 1])

        self.Data = np.zeros(dtype=np.float32, shape=[DataLength - self.sequence_Length - self.Expectation_Time + 1,
                                                      self.sequence_Length, dim])
        self.forecast_Data = np.zeros(dtype=np.float32,
                                      shape=[DataLength - self.sequence_Length - self.Expectation_Time + 1,
                                             self.sequence_Length, 1])
        self.Batch_Size = DataLength - self.sequence_Length - self.Expectation_Time + 1

        for i in range(DataLength - self.sequence_Length - self.Expectation_Time + 1):
            for j in range(self.sequence_Length):
                for k in range(dim):
                    self.Data[i, j, k] = data[j + i, k]
                    self.forecast_Data[i, j, 0] = label[j + i + self.Expectation_Time]

        print('Batch', self.Batch_Size)
        self.TrainX = np.zeros(dtype=np.float32, shape=[300, self.sequence_Length, dim])
        self.TrainY = np.zeros(dtype=np.float32, shape=[300, self.sequence_Length, 1])

        self.TestX = np.zeros(dtype=np.float32, shape=[self.Batch_Size - 300, self.sequence_Length, dim])
        self.TestY = np.zeros(dtype=np.float32, shape=[self.Batch_Size - 300, self.sequence_Length, 1])

        for i in range(300):
            self.TrainX[i] = self.Data[i]
            self.TrainY[i] = self.forecast_Data[i]

            for j in range(self.sequence_Length):
                for k in range(dim):
                    0

        for i in range(300, self.Batch_Size):
            self.TestX[i - 300] = self.Data[i]
            self.TestY[i - 300] = self.forecast_Data[i]

            for j in range(self.sequence_Length):
                for k in range(dim):
                    0

    def Model(self, data_):
        with tf.variable_scope("Rnn_Layer") as scope:
            weight = tf.tile(self.Weight_Output, [self.batch_size, 1, 1])

            output, encoding = tf.nn.dynamic_rnn(cell=self.rnn_Cell,
                                                 inputs=self.x,
                                                 sequence_length=self.seq_length(data_),
                                                 dtype=tf.float64)

        with tf.variable_scope("Rnn_Layer2") as scope:
            result, encoding2 = tf.nn.dynamic_rnn(cell=self.rnn_Cell2,
                                                 inputs=output,
                                                 sequence_length=self.seq_length(data_),
                                                 dtype=tf.float64)
        return result * 300

    def Training(self, epoch=1000, isCon=False):
        print(self.data.shape, self.label.shape)
        print(self.x, self.y)
        #input()

        with tf.Session() as sess:

            model = self.Model(self.TrainX)

            if isCon:
                saver = tf.train.Saver()
                save_path = saver.restore(sess,
                                          'D:/freeze_and_burst/regression.ckpf')

            loss = tf.reduce_mean(tf.square(tf.subtract(model, self.y)))
            train_step = tf.train.AdamOptimizer(learning_rate=0.0002).minimize(loss)

            feed_dict = {self.x: self.TrainX, self.y: self.TrainY}
            sess.run(tf.initialize_all_variables())

            for i in range(epoch):
                sess.run(train_step, feed_dict)



                if i % 100 == 0 and i > 0:
                    print(i)
                    print('loss', sess.run(loss, feed_dict))
                if i % 105 == 0:
                    saver = tf.train.Saver()
                    save_path = saver.save(sess,
                                           'D:/freeze_and_burst/regression.ckpf')


    def propagate(self):
        with tf.Session() as sess:
            sess.run(tf.initialize_all_variables())
            model = self.Model(self.TestX)
            saver = tf.train.Saver()
            save_path = saver.restore(sess,
                                      'D:/freeze_and_burst/regression.ckpf')
            feed_dict = {self.x: self.TestX, self.y: self.TestY}
            loss = tf.reduce_mean(tf.square(tf.subtract(model, self.y)))
            score = sess.run(loss, feed_dict=feed_dict)
            preidction_result = sess.run(model, feed_dict=feed_dict)

            print(score)
            for i in range(10):
                print(i)
                for l in range(20):
                    print('{{' + str(preidction_result[i, l]) + str(self.TestY[i, l]) + ' }}', end=' ,, ')

                print()
                print()
