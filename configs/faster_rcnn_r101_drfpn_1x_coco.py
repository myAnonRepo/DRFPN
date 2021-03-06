_base_ = './faster_rcnn_r50_fpn_1x_coco.py'
model = dict(
    pretrained='torchvision://resnet101',
    backbone=dict(depth=101),
    neck=dict(
        type='DRFPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        num_outs=5))
data = dict(samples_per_gpu=6)
optimizer = dict(type='SGD', lr=0.03, momentum=0.9, weight_decay=0.0001)
work_dir = './work_dirs/faster_rcnn_r101_drfpn_1x'
