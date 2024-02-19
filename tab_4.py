import tab_4_regression
import tab_4_classification

def etapes_model(features,target,type_model):

    if type_model == "regression":
        model = tab_4_regression.etapes(features,target)
    else:
        model = tab_4_classification.etapes(features,target)

    return model