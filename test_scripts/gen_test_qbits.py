import json
from pathlib import Path
import sys
# To connect to Lagrange
from iqm.qiskit_iqm import IQMProvider
# To build the test circuit from qiskit import QuantumCircuit from qiskit import transpile
from qiskit import QuantumCircuit, transpile
import subprocess
import os
from bitarray import bitarray
# This points to the folder containing this file
BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_PATH = BASE_DIR / 'tokens.json'
DATA_DIR = BASE_DIR / "quantum_random_number_generation" / "data"
TEST_SCRIPT_DIR = BASE_DIR / "sp800_22_tests" / "sp800_22_tests.py"


# Check if the script is called properly

if len(sys.argv) != 2 or sys.argv[1].isdigit() == 0:
    printf("Remember to pass the number of shots as a command line argument!\n Usage: gen_test_qbits.py <n_shots>")
    exit()

# Extract the api token
with open(TOKEN_PATH) as f:
    d = json.load(f)
api_token = d['access_token']

# Try and access Lagrange
iqm_url = "https://spark.quantum.linksfoundation.com/"
quantum_computer = "default"
provider = IQMProvider(iqm_url, quantum_computer=quantum_computer, token = api_token)
backend = provider.get_backend()


# Build a test circuit and transpile it
circuit = QuantumCircuit(1,1)
circuit.h(0)
circuit.measure_all()
transpiled_circuit = transpile(circuit, backend=backend)

# Send the circuit to Lagrange

job = backend.run([transpiled_circuit], shots = int(sys.argv[1]))

# Elaborate the results
result = job.result()
bitstr = ""
for bit in result.get_memory():
    bitstr += bit


# Generate appropriate filename for storing results
filename = "Quantum_Bits-"+ sys.argv[1] 
if os.path.exists(DATA_DIR / (filename + ".bin")):
    i = 1
    filename_new = filename + "-" + str(i) + ".bin"
    while(os.path.exists(DATA_DIR / filename_new)):
        i+=1
        filename_new = filename + "-" + str(i) + ".bin"
    filename = filename_new
else:
    filename += ".bin"



with open(DATA_DIR / filename,"wb") as out:
     bitarr = bitarray(bitstr)
     bitarr.tofile(out)


cmd = "uv run " + str(TEST_SCRIPT_DIR) + " " + str(DATA_DIR / filename)
subprocess.run(cmd.split(" "))
