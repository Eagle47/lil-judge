import subprocess
import sys


def check(solution, tests):
    for (test_input, test_output) in tests:
        with open(test_input) as inf:
            result = subprocess.run([sys.executable, solution], stdout=subprocess.PIPE, stdin=inf)

            if result.returncode != 0:
                return False

            with open(test_output) as outf:
                expected_output = outf.read().strip()

                if result.stdout.decode().strip() != expected_output:
                    return False

    return True