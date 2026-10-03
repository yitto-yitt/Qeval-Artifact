# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
import re
import copy
import atexit

machine = CPUQVM()
machine.init_qvm()
_GLOBAL_QUBITS = machine.qAlloc_many(256)
_GLOBAL_CBITS = machine.cAlloc_many(256)

def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned_param(param):
        if param is None:
            return False
        if hasattr(param, "parameters"):
            try:
                return bool(param.parameters)
            except Exception:
                pass
        try:
            complex(param)
            return False
        except Exception:
            pass
        cls_name = param.__class__.__name__.lower()
        mod_name = getattr(param.__class__, "__module__", "").lower()
        if "parameter" in cls_name or "parameter" in mod_name:
            return True
        if cls_name in {"var", "expression", "variable"} or "variational" in mod_name:
            return True
        if isinstance(param, str):
            try:
                complex(param)
                return False
            except Exception:
                return True
        return False

    def _has_unassigned_params_from_params(params):
        if params is None:
            return False
        if isinstance(params, (list, tuple)):
            return any(_is_unassigned_param(p) for p in params)
        return _is_unassigned_param(params)

    if hasattr(circuit, "data") and hasattr(circuit, "num_qubits"):
        new_circuit = circuit.__class__(circuit.num_qubits, getattr(circuit, "num_clbits", 0))
        for instruction in circuit.data.copy():
            instr = getattr(instruction, "operation", instruction[0])
            qargs = getattr(instruction, "qubits", instruction[1])
            cargs = getattr(instruction, "clbits", instruction[2])
            if not _has_unassigned_params_from_params(getattr(instr, "params", [])):
                try:
                    qidx = [circuit.find_bit(q).index for q in qargs]
                    cidx = [circuit.find_bit(c).index for c in cargs]
                    new_circuit.append(instr, qidx, cidx)
                except Exception:
                    new_circuit.append(instr, qargs, cargs)
        return new_circuit

    def _to_originir(obj):
        try:
            return convert_qprog_to_originir(obj, machine)
        except Exception:
            prog = QProg()
            prog.insert(obj)
            return convert_qprog_to_originir(prog, machine)

    def _line_has_unassigned_parameter(line):
        text = line.split("//", 1)[0].strip()
        if not text:
            return False
        first = text.split(None, 1)[0].upper()
        if first in {
            "QINIT", "CREG", "DAGGER", "ENDDAGGER", "CONTROL", "ENDCONTROL",
            "QIF", "ELSE", "ENDIF", "QWHILE", "ENDQWHILE"
        }:
            return False
        tail = text[len(text.split(None, 1)[0]):]
        tail = re.sub(r"[qc]\[\d+\]", "", tail)
        tokens = re.findall(r"[A-Za-z_]\w*", tail)
        allowed = {"pi", "e", "sin", "cos", "tan", "asin", "acos", "atan", "sqrt", "exp", "ln", "log"}
        return any(tok.lower() not in allowed for tok in tokens)

    try:
        originir = _to_originir(circuit)
        filtered_lines = []
        for line in originir.splitlines():
            if not _line_has_unassigned_parameter(line):
                filtered_lines.append(line)
        filtered_originir = "\n".join(filtered_lines)

        converter = globals().get("convert_originir_to_qprog", None)
        if converter is None:
            converter = globals().get("convert_originir_string_to_qprog", None)

        if converter is not None:
            try:
                result_prog = converter(filtered_originir, machine)
            except Exception:
                result_prog = converter(machine, filtered_originir)
            if circuit.__class__.__name__ == "QCircuit":
                try:
                    result_circuit = QCircuit()
                    result_circuit.insert(result_prog)
                    return result_circuit
                except Exception:
                    return result_prog
            return result_prog
    except Exception:
        pass

    try:
        return copy.deepcopy(circuit)
    except Exception:
        return circuit

atexit.register(lambda: machine.finalize())
