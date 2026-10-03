# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    prog = QProg()
    prog << circuit
    if prog.get_qgate_num() > 0:
        node_iter = prog.begin()
        while node_iter != prog.end():
            gate = node_iter.get_qgate()
            if gate.get_qubit_num() > 0:
                qidx = gate.get_qubits()[0]
                if not gate.is_parameterized():
                    if gate.get_target_qubit_num() == 1:
                        new_circuit << RX(qubits[qidx], 0.0)
                    elif gate.get_target_qubit_num() == 2:
                        new_circuit << CNOT(qubits[qidx], qubits[(qidx + 1) % 10])
            node_iter = node_iter.get_next()
    return new_circuit
machine.finalize()
