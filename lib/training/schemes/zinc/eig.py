import tensorflow as tf
from tensorflow.keras import (optimizers, losses, metrics)
import numpy as np
import os

from lib.base.dotdict import HDict
from lib.data.datasets.zinc import EigenDataset
from lib.models.zinc.dc import DCEigTransformer
from lib.training.schemes.scheme_base import BaseEigModelScheme
from lib.training.schemes.zinc._eval import ZINCEval


class ZincDCEig(ZINCEval, BaseEigModelScheme):
    def get_default_config(self):
        config_dict = super().get_default_config()
        config_dict.update(
            dataset_name       = 'zinc',
            num_virtual_nodes  = 0,
            rlr_monitor        = 'val_mae',
            save_best_monitor  = 'val_mae',
        )
        return config_dict
    
    def get_dataset_config(self, splits=['training','validation']):
        dataset_config, _ = super().get_dataset_config()
        return dataset_config, EigenDataset
    
    def get_model_config(self):
        config = self.config
        
        model_config, _ = super().get_model_config()
        model_config.update(
            readout_edges     = False,
            num_virtual_nodes = config.num_virtual_nodes,
        )
        return model_config, DCEigTransformer
    
    def get_loss(self):
        loss = losses.MeanAbsoluteError(name='MAE')
        return loss
    
    def get_metrics(self):
        return ['mae']


SCHEME = ZincDCEig




