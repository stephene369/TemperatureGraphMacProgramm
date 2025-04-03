from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class WorkerSignals(QObject):
    """
    Définit les signaux disponibles pour un Worker (QRunnable).
    """
    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    """
    Worker thread pour exécuter des tâches en arrière-plan.
    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        
        # Stocker la fonction et ses arguments
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        
        # Ajouter le callback de progression aux kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        
    @pyqtSlot()
    def run(self):
        """
        Exécute la fonction avec les arguments fournis.
        """
        try:
            # Exécuter la fonction
            result = self.fn(*self.args, **self.kwargs)
            
            # Émettre le signal de résultat
            self.signals.result.emit(result)
            
        except Exception as e:
            # Émettre le signal d'erreur
            self.signals.error.emit(e)
            
        finally:
            # Émettre le signal de fin
            self.signals.finished.emit()
