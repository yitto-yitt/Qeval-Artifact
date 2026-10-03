# EVAL_META: task_id=81, framework=qpanda2, class=3
import atexit
import os
import tempfile
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];"""
    converter = getattr(pq, "convert_qasm_string_to_qprog", None)
    if converter is not None:
        converted = converter(qasm_string, machine)
    else:
        fd, path = tempfile.mkstemp(suffix=".qasm")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(qasm_string)
            converted = pq.convert_qasm_to_qprog(path, machine)
        finally:
            if os.path.exists(path):
                os.remove(path)
    if isinstance(converted, (tuple, list)):
        return converted[0]
    return converted

atexit.register(lambda: machine.finalize())
