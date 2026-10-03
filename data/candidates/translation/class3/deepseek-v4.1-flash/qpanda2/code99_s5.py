# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    prog = QProg()
    prog << circuit
    for instruction in prog.get_instructions():
        gate = instruction.m_operation
        try:
            if gate.is_parameterized():
                param = gate.get_parameter()
                if isinstance(param, var):
                    continue
                if isinstance(param, (list, tuple)) and len(param) > 0 and isinstance(param[0], var):
                    continue
        except AttributeError:
            pass
        new_circuit << gate
    return new_circuit

machine.finalize()
