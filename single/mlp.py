import numpy as np
import tensorflow.compat.v1 as tf

class MLP:
    def __init__(self, k, d, lr = 1e-4, lbd = 1e-4, hidden_layers = [2000, 1000]):
        self._k = k
        self._d = d
        self._lr = lr
        self._lbd = lbd
        self._hidden_layers = hidden_layers
        self.x = tf.placeholder(tf.float32, [None, self._d])
        self.y = tf.placeholder(tf.float32, [None, self._k])
        with tf.variable_scope("content_mlp", reuse = tf.AUTO_REUSE):
            t = self.x
            for lid, num_of_units in enumerate(self._hidden_layers):
                t = tf.layers.dense(t, num_of_units, activation = tf.sigmoid, name = 'layer_%d'%lid)
            self.F = tf.layers.dense(t, self._k, name = 'layer_output')
            self.obj = 0.5 * tf.reduce_sum((self.y - self.F) ** 2)
            self.solver = tf.train.RMSPropOptimizer(self._lr).minimize(self.obj)

    def forward(self, sess, X, batch_size = 64):
        n_row, n_col = X.shape
        F = np.zeros((n_col, self._k), dtype=np.float32)
        for i in range(0, n_row, batch_size):
            actual_batch_size = min(batch_size, n_row-i)
            F[i: i+actual_batch_size, :] = sess.run(self.F, feed_dict={self.x: X[i: i+actual_batch_size]})
        return F

    def backward(self, sess, X, Y, batch_size = 64):
        n_row, n_col = X.shape
        ridxs = np.random.permutation(n_row)
        obj = 0
        for i in range(0, n_row, batch_size):
            actual_batch_size = min(batch_size, n_row-i)
            batch_obj, _ = sess.run([self.obj, self.solver], feed_dict={self.x: X[ridxs[i: i+actual_batch_size]], self.y: Y[ridxs[i: i+actual_batch_size]]})
            obj += batch_obj
        return obj