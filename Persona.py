import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class Persona:

    def __init__(self, department='dresses'):
        self.loaded = False
        self.department = department
        # self.segment_params = None
        # self.custpred = None
        return

    def department(self):
        return self.department

    def segment_affinities(self, seg_label):
        # get the characteristics/attribute preferences of the segment (seg_label)
        seg_params = {}
        if self.loaded:
            seg_params = self.segment_params[seg_label]
        return seg_params

    def load_model(self, segment_param_file, attribute_alloc_file):
        # segment_param_file will have the segment characteristics to be used by segmentAffinities method
        # attribute_alloc_file will have all the combinations of attribute values, such that this can be
        # used by predict_persona to map to the appropriate segment

        self.segment_params = pickle.load(open(segment_param_file, 'rb'))

        self.custpred = pd.read_csv(attribute_alloc_file, index_col=False, dtype={'segment_label':str})
        self.loaded = True
        return

    def predict_persona(self, param_dict):
        # For each selection of the attribute values passed in param_dict,
        # the closest segment match is returned.

        # In future, for missing attribute values, a set() of segment labels will be returned

        cols = []
        for k, v in param_dict.items():
            cols.append(k+'__'+v.lower().replace(' ', '_').replace('/', '_'))

        fill_values = np.ones((len(cols), 1)).transpose()

        df = pd.merge(pd.DataFrame(data=fill_values, columns=cols), pd.DataFrame(columns=self.custpred.columns),
                      how='outer')
        df = df.fillna(0)
        df = pd.DataFrame(df, columns=self.custpred.columns)
        index_val = cosine_similarity(df.drop('segment_label', axis=1).values,
                                      self.custpred.drop('segment_label', axis=1).values).argmax()

        return set(self.custpred.loc[self.custpred.index == index_val, 'segment_label'])
