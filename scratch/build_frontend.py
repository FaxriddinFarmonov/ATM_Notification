import subprocess

res = subprocess.run("npm run build", cwd=r"C:\Users\Faxriddin\Documents\Frontend-ATM-Informations", shell=True, capture_output=True, text=True)
print("STDOUT:\n", res.stdout)
print("STDERR:\n", res.stderr)
print("EXIT CODE:", res.returncode)
