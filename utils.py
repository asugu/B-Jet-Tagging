from prettytable import PrettyTable


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


def plot_metrics (x, train_loss, val_loss, train_accuracy, val_accuracy, train_auc, val_auc):
        import matplotlib.pyplot as plt
        from IPython.display import clear_output
        
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, figsize=(15,5))
        clear_output(wait=True)
        
        #ax1.set_yscale('log')
        ax1.plot(x, train_loss, label="loss")
        ax1.plot(x, val_loss, label="val_loss")
        ax1.set_xlabel('epoch')
        ax1.legend()
        ax1.grid()
        
        ax2.plot(x, train_accuracy, label="accuracy({:.3f}%)".format(100*train_accuracy[-1]))
        max_acc = max(train_accuracy)
        ax2.plot(x, len(x)*[max_acc], 'b--', label="max acc. attained ({:.1f}%)".format(100*max_acc))
        ax2.plot(x, val_accuracy, label="validation accuracy({:.3f}%)".format(100*val_accuracy[-1]))
        max_val_acc = max(val_accuracy)
        ax2.plot(x, len(x)*[max_val_acc], 'g--', label="max val. acc. attained ({:.3f}%)".format(100*max_val_acc))
        ax2.legend(loc="lower right")
        ax2.set_xlabel('epoch')
        ax2.set_ylim(0.0, 1.0)
        #ax2.set_yscale('log')
        ax2.grid()
         
        ax3.plot(x, train_auc, label="AUC({:.3f})".format(train_auc[-1]))   #changed
        max_auc = max(train_auc)
        ax3.plot(x, len(x)*[max_auc], 'b--', label="max auc. attained ({:.3f})".format(max_auc))
        ax3.plot(x, val_auc, label="validation AUC({:.3f})".format(val_auc[-1]))
        max_val_acc = max(val_auc)
        ax3.plot(x, len(x)*[max_val_acc], 'g--', label="max val. auc. attained ({:.3f})".format(max_val_acc))
        ax3.legend(loc="lower right")
        ax3.set_xlabel('epoch')
        ax3.set_ylim(0.0, 1.0)
        #ax3.set_yscale('log')
        ax3.grid()
        
        plt.show()