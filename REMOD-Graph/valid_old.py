import numpy as np
import pickle
import torch
from sklearn.preprocessing import label_binarize
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score



if __name__ == "__main__":
    relation_num = 26
    path = "result/proposal-bce/"
    for e in range(0,300,10):
        if e != 280:
            continue
        res = torch.load(path+str(e)+"/test/result.pth")
        score = np.vstack(res[0])
        true = np.array(res[2])
        y_true = label_binarize(true, classes=list(range(relation_num)))

        precision = dict()
        recall = dict()
        threshold = dict()
        average_precision = dict()
        best_threshold = dict()
        for i in range(score.shape[1]):
            precision[i], recall[i], threshold[i] = precision_recall_curve(y_true[:, i], score[:, i])
            average_precision[i] = average_precision_score(y_true[:, i], score[:, i])
            f1 = 2*precision[i]*recall[i]/(precision[i] + recall[i] + 1e-10)
            best_threshold[i] = threshold[i][np.argmax(f1)]

        precision["micro"], recall["micro"], _ = precision_recall_curve(y_true.ravel(), score.ravel())
        average_precision["micro"] = average_precision_score(y_true, score, average="micro")
        #with open("HAN-TuckER-precision-recall.pkl", "wb") as f:
        #    pickle.dump({'precision':precision["micro"], 'recall':recall["micro"]}, f)
        print("average precision:",average_precision)
        print("best threshold:", best_threshold)

        print("validation set:")
        y_pred = np.array(score >= np.array(list(best_threshold.values())), dtype=np.int8)
        for i in range(y_true.shape[1]):
            print(i, accuracy_score(y_true[:,i], y_pred[:,i]))
        print(accuracy_score(y_true.ravel(), y_pred.ravel()))
        print(classification_report(y_true, y_pred))

        print("annotated set:")
        pres = torch.load(path+str(e)+"/pred/result.pth")
        pscore = np.vstack(pres[0])
        ptrue = np.array(pres[2])
        y_true = label_binarize(ptrue, classes=list(range(relation_num)))
        y_pred = np.array(pscore >= np.array(list(best_threshold.values())), dtype=np.int8)
        for i in range(y_true.shape[1]):
            print(i, accuracy_score(y_true[:,i], y_pred[:,i]))
        print(accuracy_score(y_true.ravel(), y_pred.ravel()))
        print(classification_report(y_true, y_pred, digits=3))
