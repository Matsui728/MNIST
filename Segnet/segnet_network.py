# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:13:41 2017

@author: kawalab
"""


import chainer
import chainer.functions as F
import chainer.links as L


class SegNet(chainer.Chain):
    def __init__(self, in_channel=3, out_channel=10,  c1=64, c2=64, c3=64,
                 c4=64, c5=64, filter_size1=7):
        super(SegNet, self).__init__(
            # Convolution Parts
            conv1_1=L.Convolution2D(in_channel, c1, ksize=filter_size1, pad=3),
            conv1_2=L.Convolution2D(c1, c1, ksize=filter_size1, pad=3),
            bnorm1_1=L.BatchNormalization(c1, initial_beta=0.001),
            bnorm1_2=L.BatchNormalization(c1, initial_beta=0.001),

            conv2_1=L.Convolution2D(c1, c2, ksize=filter_size1, pad=3),
            conv2_2=L.Convolution2D(c2, c2, ksize=filter_size1, pad=3),
            bnorm2_1=L.BatchNormalization(c2, initial_beta=0.001),
            bnorm2_2=L.BatchNormalization(c2, initial_beta=0.001),

            conv3_1=L.Convolution2D(c2, c3, ksize=filter_size1, pad=3),
            conv3_2=L.Convolution2D(c3, c3, ksize=filter_size1, pad=3),
            conv3_3=L.Convolution2D(c3, c3, ksize=filter_size1, pad=3),
            bnorm3_1=L.BatchNormalization(c3, initial_beta=0.001),
            bnorm3_2=L.BatchNormalization(c3, initial_beta=0.001),
            bnorm3_3=L.BatchNormalization(c3, initial_beta=0.001),

            conv4_1=L.Convolution2D(c3, c4, ksize=filter_size1, pad=3),
            conv4_2=L.Convolution2D(c4, c4, ksize=filter_size1, pad=3),
            conv4_3=L.Convolution2D(c4, c4, ksize=filter_size1, pad=3),
            bnorm4_1=L.BatchNormalization(c4, initial_beta=0.001),
            bnorm4_2=L.BatchNormalization(c4, initial_beta=0.001),
            bnorm4_3=L.BatchNormalization(c4, initial_beta=0.001),

            conv5_1=L.Convolution2D(c4, c5, ksize=filter_size1, pad=3),
            conv5_2=L.Convolution2D(c5, c5, ksize=filter_size1, pad=3),
            conv5_3=L.Convolution2D(c5, c5, ksize=filter_size1, pad=3),
            bnorm5_1=L.BatchNormalization(c5, initial_beta=0.001),
            bnorm5_2=L.BatchNormalization(c5, initial_beta=0.001),
            bnorm5_3=L.BatchNormalization(c5, initial_beta=0.001),


            # Deconvolution Parts
            dconv5_1=L.Deconvolution2D(c5, c5, ksize=filter_size1, pad=3),
            dconv5_2=L.Deconvolution2D(c5, c5, ksize=filter_size1, pad=3),
            dconv5_3=L.Deconvolution2D(c5, c5, ksize=filter_size1, pad=3),
            bnorm6_1=L.BatchNormalization(c5, initial_beta=0.001),
            bnorm6_2=L.BatchNormalization(c5, initial_beta=0.001),
            bnorm6_3=L.BatchNormalization(c5, initial_beta=0.001),

            dconv4_1=L.Deconvolution2D(c5, c4, ksize=filter_size1, pad=3),
            dconv4_2=L.Deconvolution2D(c4, c4, ksize=filter_size1, pad=3),
            dconv4_3=L.Deconvolution2D(c4, c4, ksize=filter_size1, pad=3),
            bnorm7_1=L.BatchNormalization(c4, initial_beta=0.001),
            bnorm7_2=L.BatchNormalization(c4, initial_beta=0.001),
            bnorm7_3=L.BatchNormalization(c4, initial_beta=0.001),

            dconv3_1=L.Deconvolution2D(c4, c3, ksize=filter_size1, pad=3),
            dconv3_2=L.Deconvolution2D(c3, c3, ksize=filter_size1, pad=3),
            dconv3_3=L.Deconvolution2D(c3, c3, ksize=filter_size1, pad=3),
            bnorm8_1=L.BatchNormalization(c3, initial_beta=0.001),
            bnorm8_2=L.BatchNormalization(c3, initial_beta=0.001),
            bnorm8_3=L.BatchNormalization(c3, initial_beta=0.001),

            dconv2_1=L.Deconvolution2D(c3, c2, ksize=filter_size1, pad=3),
            dconv2_2=L.Deconvolution2D(c2, c2, ksize=filter_size1, pad=3),
            bnorm9_1=L.BatchNormalization(c2, initial_beta=0.001),
            bnorm9_2=L.BatchNormalization(c2, initial_beta=0.001),

            dconv1_1=L.Deconvolution2D(c2, out_channel,
                                       ksize=filter_size1, pad=3),
            dconv1_2=L.Deconvolution2D(out_channel, out_channel,
                                       ksize=filter_size1, pad=3),
            bnorm10_1=L.BatchNormalization(out_channel, initial_beta=0.001),
            bnorm10_2=L.BatchNormalization(out_channel, initial_beta=0.001),
            )

    def __call__(self, x):
        # x.data = x.data.reshape((len(x.data), 1, 28, 28))
        # Convolution Parts
        outsize1 = x.shape[-2:]
        h = F.relu(self.bnorm1_1(self.conv1_1(x)))
        h = F.relu(self.bnorm1_2(self.conv1_2(x)))
        h = F.max_pooling_2d(h, 2)

        outsize2 = h.shape[-2:]
        h = F.relu(self.bnorm2_1(self.conv12_1(x)))
        h = F.relu(self.bnorm2_2(self.conv2_2(x)))
        h = F.max_pooling_2d(h, 2)

        outsize3 = h.shape[-2:]
        h = F.relu(self.bnorm3_1(self.conv3_1(x)))
        h = F.relu(self.bnorm3_2(self.conv3_2(x)))
        h = F.relu(self.bnorm3_3(self.conv3_3(x)))
        h = F.max_pooling_2d(h, 2)

        outsize4 = h.shape[-2:]
        h = F.relu(self.bnorm4_1(self.conv4_1(x)))
        h = F.relu(self.bnorm4_2(self.conv4_2(x)))
        h = F.relu(self.bnorm4_3(self.conv4_3(x)))
        h = F.max_pooling_2d(h, 2)

        outsize5 = h.shape[-2:]
        h = F.relu(self.bnorm5_1(self.conv5_1(x)))
        h = F.relu(self.bnorm5_2(self.conv5_2(x)))
        h = F.relu(self.bnorm5_3(self.conv5_3(x)))
        h = F.max_pooling_2d(h, 2)

        # Deconvolution Parts
        h = F.unpooling_2d(h, 2, outsize=outsize5)
        h = F.relu(self.bnorm6_1(self.dconv5_1(x)))
        h = F.relu(self.bnorm6_2(self.dconv5_2(x)))
        h = F.relu(self.bnorm6_3(self.dconv5_3(x)))

        h = F.unpooling_2d(h, 2, outsize=outsize4)
        h = F.relu(self.bnorm7_1(self.dconv4_1(x)))
        h = F.relu(self.bnorm7_2(self.dconv4_2(x)))
        h = F.relu(self.bnorm7_3(self.dconv4_3(x)))

        h = F.unpooling_2d(h, 2, outsize=outsize3)
        h = F.relu(self.bnorm8_1(self.dconv3_1(x)))
        h = F.relu(self.bnorm8_2(self.dconv3_2(x)))
        h = F.relu(self.bnorm8_3(self.dconv3_3(x)))

        h = F.unpooling_2d(h, 2, outsize=outsize2)
        h = F.relu(self.bnorm9_1(self.dconv2_1(x)))
        h = F.relu(self.bnorm9_2(self.dconv2_2(x)))

        h = F.unpooling_2d(h, 2, outsize=outsize1)
        h = F.relu(self.bnorm10_1(self.dconv1_1(x)))
        y = F.relu(self.bnorm10_2(self.dconv2_2(x)))
        return y


if __name__ == '__main__':
    SegNet()