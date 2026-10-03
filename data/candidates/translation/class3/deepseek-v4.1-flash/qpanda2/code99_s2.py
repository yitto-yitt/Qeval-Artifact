# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
cbits = machine.cAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for instruction in circuit.get_instructions():
        if isinstance(instruction, QGate):
            param = instruction.get_parameter()
            if param.get_name() != "":
                continue
        new_circuit << instruction
    return new_circuit

machine.finalize()
