'''
if you use two-stage detector, such as faster rcnn,please change the codes :
1. mmdet/models/detectors/two_stage.py

    def extract_feat(self, img):
    """Directly extract features from the backbone+neck
    """
    x_backbone = self.backbone(img)
    if self.with_neck:
        x_fpn = self.neck(x_backbone)
    return x_backbone,x_fpn

and:

    def simple_test(self, img, img_metas, proposals=None, rescale=False):
        """Test without augmentation."""
        assert self.with_bbox, 'Bbox head must be implemented.'

        x_backbone,x_fpn = self.extract_feat(img)

        if proposals is None:
            proposal_list = self.simple_test_rpn(x_fpn, img_metas)
        else:
            proposal_list = proposals

        return self.roi_head.simple_test(
            x_fpn, proposal_list, img_metas, rescale=rescale),x_backbone,x_fpn

2.mmdet/apis/inference.py

    def inference_detector(model, img):
    .......
            # forward the model
        with torch.no_grad():
            result,x_backbone,x_fpn= model(return_loss=False, rescale=True, **data)
        return result,x_backbone,x_fpn

if you use other detectors, it is easy to achieve it like this

'''



from mmdet.apis import inference_detector, init_detector
import cv2
import numpy as np
import time
import torch
import os

def main():
    config = '/home/maer/Workspace/mmdetection/configs/coco/faster_rcnn_r50_fpn_1x_coco_fpnDCN_4gpu.py'
    checkpoint = '/home/maer/Workspace/mmdetection/work_dirs/faster_rcnn_r50_fpn_1x_coco_fpn_DCN_4gpu/epoch_12.pth'
    #config = './configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py'
    #checkpoint = './work_dirs/faster_rcnn_r50_fpn_1x_coco.pth'
    device = 'cuda:0'
    # build the model from a config file and a checkpoint file
    model = init_detector(config, checkpoint, device=device)
    images_dir = 'test_images'
    # test a single image
    for i in os.listdir(images_dir):
        img_path = os.path.join(images_dir, i)
        img_name = i.split('.')[0]
        image = cv2.imread(img_path)
        height, width, channels = image.shape
        result, laterals, x_laterls_sum, laterals_align_sum, x_fpn = inference_detector(model, img_path)

        fm_save_path = os.path.join('feature_map', img_name)
        if not os.path.exists(fm_save_path):
            os.makedirs(fm_save_path)

        feature_index = 1
        for feature in laterals:
            feature_index += 1
            L_save_path = os.path.join(fm_save_path, 'L_'+str(feature_index))
            if not os.path.exists(L_save_path):
                os.makedirs(L_save_path)
            P = torch.sigmoid(feature)
            #P = feature
            P = P.cpu().detach().numpy()
            P = np.maximum(P, 0)
            P = (P - np.min(P)) / (np.max(P) - np.min(P))
            P = P.squeeze(0)
            #print(P.shape)

            C = P.shape[0]
            for c in range(C):
                P_ = P[c, ...] 
            

                cam = cv2.resize(P_, (width, height))
                heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
                heatmap = np.float32(heatmap) / 255
                heatmap = heatmap / np.max(heatmap)
                heatmap_image = np.uint8(255 * heatmap)

                cv2.imwrite(L_save_path + '/'+ str(c)+'_heatmap.jpg', heatmap_image)
                result = cv2.addWeighted(image, 0.8, heatmap_image, 0.3, 0)
                cv2.imwrite(L_save_path + '/'+ str(c) + '_result.jpg', result)

        feature_index = 1
        for feature in x_laterls_sum:
            feature_index += 1
            LS_save_path = os.path.join(fm_save_path, 'LS_'+str(feature_index))
            if not os.path.exists(LS_save_path):
                os.makedirs(LS_save_path)
            P = torch.sigmoid(feature)
            #P = feature
            P = P.cpu().detach().numpy()
            P = np.maximum(P, 0)
            P = (P - np.min(P)) / (np.max(P) - np.min(P))
            P = P.squeeze(0)
            #print(P.shape)

            C = P.shape[0]
            for c in range(C):
                P_ = P[c, ...] 
            

                cam = cv2.resize(P_, (width, height))
                heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
                heatmap = np.float32(heatmap) / 255
                heatmap = heatmap / np.max(heatmap)
                heatmap_image = np.uint8(255 * heatmap)

                cv2.imwrite(LS_save_path + '/'+ str(c)+'_heatmap.jpg', heatmap_image)
                result = cv2.addWeighted(image, 0.8, heatmap_image, 0.3, 0)
                cv2.imwrite(LS_save_path + '/'+ str(c) + '_result.jpg', result)

        feature_index = 1
        for feature in laterals_align_sum:
            feature_index += 1
            LAS_save_path = os.path.join(fm_save_path, 'LAS_'+str(feature_index))
            if not os.path.exists(LAS_save_path):
                os.makedirs(LAS_save_path)
            P = torch.sigmoid(feature)
            #P = feature
            P = P.cpu().detach().numpy()
            P = np.maximum(P, 0)
            P = (P - np.min(P)) / (np.max(P) - np.min(P))
            P = P.squeeze(0)
            #print(P.shape)

            C = P.shape[0]
            for c in range(C):
                P_ = P[c, ...] 
            

                cam = cv2.resize(P_, (width, height))
                heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
                heatmap = np.float32(heatmap) / 255
                heatmap = heatmap / np.max(heatmap)
                heatmap_image = np.uint8(255 * heatmap)

                cv2.imwrite(LAS_save_path + '/'+ str(c)+'_heatmap.jpg', heatmap_image)
                result = cv2.addWeighted(image, 0.8, heatmap_image, 0.3, 0)
                cv2.imwrite(LAS_save_path + '/'+ str(c) + '_result.jpg', result)

        feature_index = 1
        for feature in x_fpn:
            feature_index += 1
            Final_save_path = os.path.join(fm_save_path, 'Final_'+str(feature_index))
            if not os.path.exists(Final_save_path):
                os.makedirs(Final_save_path)
            P = torch.sigmoid(feature)
            #P = feature
            P = P.cpu().detach().numpy()
            P = np.maximum(P, 0)
            P = (P - np.min(P)) / (np.max(P) - np.min(P))
            P = P.squeeze(0)
            #P = P[2, ...]
            #print(P.shape)
            C = P.shape[0]
            for c in range(C):
                P_ = P[c, ...] 
                cam = cv2.resize(P_, (width, height))
                heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
                heatmap = np.float32(heatmap) / 255
                heatmap = heatmap / np.max(heatmap)
                heatmap_image = np.uint8(255 * heatmap)

                cv2.imwrite(Final_save_path + '/'+ str(c)+ '_heatmap.jpg', heatmap_image)  # 生成图像
                result = cv2.addWeighted(image, 0.8, heatmap_image, 0.3, 0)
                cv2.imwrite(Final_save_path + '/'+ str(c)+ '_result.jpg', result)


if __name__ == '__main__':
    main()
