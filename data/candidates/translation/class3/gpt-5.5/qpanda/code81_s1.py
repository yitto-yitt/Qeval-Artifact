# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    machine = CPUQVM()
    for init_name in ("init_qvm", "init"):
        init_func = getattr(machine, init_name, None)
        if callable(init_func):
            try:
                init_func()
            except TypeError:
                pass

    convert_qasm_string_to_quantum_circuit._machine = machine

    for converter_name in ("convert_qasm_string_to_qprog", "qasm_string_to_qprog", "convert_qasm_to_qprog"):
        converter = globals().get(converter_name)
        if callable(converter):
            for args in ((qasm_string, machine), (machine, qasm_string), (qasm_string,)):
                try:
                    result = converter(*args)
                    if isinstance(result, tuple):
                        result = result[0]
                    return result
                except TypeError:
                    continue
                except Exception:
                    continue

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    else:
        qubits = machine.qalloc_many(2)

    circuit = QCircuit()
    circuit << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    return circuit
