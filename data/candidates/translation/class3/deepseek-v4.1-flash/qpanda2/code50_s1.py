# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_gate_in_position(circuit, position):
    gates = circuit.get_gates()
    n = len(gates)
    if position < 0:
        position += n
    if position < 0 or position >= n:
        raise IndexError("list index out of range")
    new_circuit = QCircuit()
    for i, gate in enumerate(gates):
        if i != position:
            new_circuit << gate
    return new_circuit

machine.finalize()
