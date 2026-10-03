# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq
import matplotlib.pyplot as plt

def create_ghz(drawing=False):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[0], qubits[2])
    
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
        
    if drawing:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, pq.draw(prog), ha='center', va='center', family='monospace')
        ax.axis('off')
        return prog, fig
        
    return prog
