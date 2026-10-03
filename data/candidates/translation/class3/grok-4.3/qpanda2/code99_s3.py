# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(5)
def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    if hasattr(circuit, 'data'):
        circuit_data = list(circuit.data)
        for instruction in circuit_data:
            instr = getattr(instruction, 'operation', instruction)
            params = getattr(instr, 'params', [])
            has_unassigned = False
            if params:
                for p in params:
                    if isinstance(p, Parameter):
                        has_unassigned = True
                        break
            if not has_unassigned:
                try:
                    new_circuit.insert(instr)
                except:
                    pass
    return new_circuit
machine.finalize()
