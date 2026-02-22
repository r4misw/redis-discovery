import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    "main.py",
    "exercise_4_2_basic.py",
    "exercise_4_3_1_sorted_set.py",
    "exercise_4_3_2_json.py",
]


def run_script(script_name: str) -> None:
    script_path = Path(__file__).parent / script_name
    print(f"\n=== Running {script_name} ===")
    subprocess.run([sys.executable, str(script_path)], check=True)


if __name__ == "__main__":
    for script in SCRIPTS:
        run_script(script)
    print("\nAll section 4 scripts completed successfully.")
