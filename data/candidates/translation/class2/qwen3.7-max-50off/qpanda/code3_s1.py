# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit

def create_ghz(drawing=False):
    try:
        qc = QuantumCircuit(3, 3)
    except TypeError:
        qc = QuantumCircuit(3)
        
    qc.h(0)
    if hasattr(qc, 'cx'):
        qc.cx(0, 1)
        qc.cx(0, 2)
    else:
        qc.cnot(0, 1)
        qc.cnot(0, 2)
        
    try:
        qc.measure_all()
    except AttributeError:
        try:
            qc.measure([0, 1, 2], [0, 1, 2])
        except Exception:
            for i in range(3):
                qc.measure(i, i)
                
    if drawing:
        try:
            return qc, qc.draw(output="mpl")
        except TypeError:
            return qc, qc.draw()
    return qc
