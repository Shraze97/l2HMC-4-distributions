
"""
Collection of useful layers
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf
TF_FLOAT = tf.float32
NP_FLOAT = np.float32

class Linear(object):
    def __init__(self, in_, out_, scope='linear', factor=1.0):
        with tf.compat.v1.variable_scope(scope):
            initializer = tf.compat.v1.keras.initializers.VarianceScaling(scale=factor * 2.0, mode=('FAN_IN').lower(), distribution=("uniform" if False else "truncated_normal"), dtype=TF_FLOAT)
            self.W = tf.compat.v1.get_variable('W', shape=(in_, out_), initializer=initializer)
            self.b = tf.compat.v1.get_variable('b', shape=(out_,), initializer=tf.compat.v1.constant_initializer(0., dtype=TF_FLOAT))

    def __call__(self, x):
        return tf.add(tf.matmul(x, self.W), self.b)


class ConcatLinear(object):
    def __init__(self, ins_, out_, factors=None, scope='concat_linear'):
        self.layers = []

        with tf.compat.v1.variable_scope(scope):
            for i, in_ in enumerate(ins_):
                if factors is None:
                    factor = 1.0
                else:
                    factor = factors[i]

        self.layers.append(Linear(in_, out_, scope='linear_%d' % i, factor=factor))

    def __call__(self, inputs):
        output = 0.
        for i, x in enumerate(inputs):
            output += self.layers[i](x)
    
        return output

class Parallel(object):
    def __init__(self, layers=[]):
        self.layers = layers
    def add(self, layer):
        self.layers.append(layer)
    def __call__(self, x):
        return [layer(x) for layer in self.layers]

class Sequential(object):
    def __init__(self, layers = []):
        self.layers = layers
        
    def add(self, layer):
        self.layers.append(layer)
        
    def __call__(self, x):
        y = x
        for layer in self.layers:
            y = layer(y)
        return y

class ScaleTanh(object):
    def __init__(self, in_, scope='scale_tanh'):
        with tf.compat.v1.variable_scope(scope):
            self.scale = tf.exp(tf.compat.v1.get_variable('scale', shape=(1, in_), initializer=tf.compat.v1.constant_initializer(0., dtype=TF_FLOAT)))
    def __call__(self, x):
        return self.scale * tf.nn.tanh(x)
    
class Zip(object):
    def __init__(self, layers=[]):
        self.layers = layers
    
    def __call__(self, x):
        assert len(x) == len(self.layers)
        n = len(self.layers)
        return [self.layers[i](x[i]) for i in range(n)]

