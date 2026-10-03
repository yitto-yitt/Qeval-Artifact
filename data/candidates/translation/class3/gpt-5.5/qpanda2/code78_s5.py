# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(32)
atexit.register(machine.finalize)

def qft_no_swaps(num_qubits):
    circuit = pq.QCircuit()
    if num_qubits > len(_qubits):
        raise ValueError("num_qubits exceeds globally allocated qubits")
    for j in range(num_qubits):
        for k in range(j):
            circuit << pq.CR(_qubits[k], _qubits[j], -math.pi / (2 ** (j - k)))
        circuit << pq.H(_qubits[j])
    return circuit
