# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    gate = pyqpanda.Y(qubits[4])
    if hasattr(gate, 'control'):
        c_gate = gate.control([qubits[0], qubits[1], qubits[2], qubits[3]])
    elif hasattr(gate, 'set_control'):
        gate.set_control([qubits[0], qubits[1], qubits[2], qubits[3]])
        c_gate = gate
    else:
        c_gate = gate
    qc << c_gate
    return qc

machine.finalize()
