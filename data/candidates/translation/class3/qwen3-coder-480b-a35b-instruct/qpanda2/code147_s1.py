# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    # In pyQPanda, we need to decompose multi-controlled Y gate manually
    # A multi-controlled Y gate can be implemented using multi-controlled U gate
    # where U is Y rotation
    ctrl_list = [qubits[0], qubits[1], qubits[2], qubits[3]]
    target_qubit = qubits[4]
    
    # Y gate is equivalent to RY(pi) up to global phase
    # For multi-controlled Y, we use multi-controlled U gate
    # Y = -i * RY(pi) = -i * exp(-i*pi*Y/2)
    qc.mcu(ctrl_list, target_qubit, pq.QMachineType.CPU, [0, 0, 0, pq.PI])

    return qc

machine.finalize()
