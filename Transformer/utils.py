from prettytable import PrettyTable
import matplotlib.pyplot as plt
from IPython.display import clear_output

def count_parameters(model):
    table = PrettyTable(["Modules", "Parameters"])
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad: continue
        params = parameter.numel()
        table.add_row([name, params])
        total_params+=params
    print(table)
    print(f"Total Trainable Params: {total_params}")
    return total_params


def plot_metrics (x, train_loss, val_loss, train_accuracy, val_accuracy, train_auc, val_auc, train_f1, val_f1):
        
        
        f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharex=True, figsize=(20,5))
        clear_output(wait=True)
        
        #ax1.set_yscale('log')
        ax1.plot(x, train_loss, label="loss")
        ax1.plot(x, val_loss, label="val_loss")
        ax1.set_xlabel('epoch')
        ax1.legend()
        ax1.grid()
        
        ax2.plot(x, train_accuracy, label="accuracy({:.3f}%)".format(100*train_accuracy[-1]))
        max_acc = max(train_accuracy)
        ax2.plot(x, len(x)*[max_acc], 'b--', label="max acc. ({:.3f}%)".format(100*max_acc))
        ax2.plot(x, val_accuracy, label="val acc. ({:.3f}%)".format(100*val_accuracy[-1]))
        max_val_acc = max(val_accuracy)
        ax2.plot(x, len(x)*[max_val_acc], 'g--', label="max val. acc. ({:.3f}%)".format(100*max_val_acc))
        ax2.legend(loc="lower right")
        ax2.set_xlabel('epoch')
        ax2.set_ylim(0.5, 1.0)
        ax2.grid()
         
        ax3.plot(x, train_auc, label="AUC({:.3f})".format(train_auc[-1]))   #changed
        max_auc = max(train_auc)
        ax3.plot(x, len(x)*[max_auc], 'b--', label="max auc. ({:.3f})".format(max_auc))
        ax3.plot(x, val_auc, label="val AUC({:.3f})".format(val_auc[-1]))
        max_val_auc = max(val_auc)
        ax3.plot(x, len(x)*[max_val_auc], 'g--', label="max val. auc. ({:.3f})".format(max_val_auc))
        ax3.legend(loc="lower right")
        ax3.set_xlabel('epoch')
        ax3.set_ylim(0.5, 1.0)
        #ax3.set_yscale('log')
        ax3.grid()


        ax4.plot(x, train_f1, label="F1({:.3f})".format(train_f1[-1]))   #changed
        max_f1 = max(train_f1)
        ax4.plot(x, len(x)*[max_f1], 'b--', label="max F1 ({:.3f})".format(max_f1))
        ax4.plot(x, val_f1, label="val F1({:.3f})".format(val_f1[-1]))
        max_val_f1 = max(val_f1)
        ax4.plot(x, len(x)*[max_val_f1], 'g--', label="max val. F1 ({:.3f})".format(max_val_f1))
        ax4.legend(loc="lower right")
        ax4.set_xlabel('epoch')
       # ax4.set_ylim(0.0, 1.0)
        #ax3.set_yscale('log')
        ax4.grid()




        
        plt.show()