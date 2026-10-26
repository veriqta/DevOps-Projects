# Contributing

Keep every project independently usable. Explain the business purpose, exact working directory, configuration, verification, failure recovery and cleanup. Do not replace the required walkthrough with a link to external documentation.

Run `python3 .github/checks.py` from the repository root. Container and cloud checks require the documented target environment; state exactly what you executed. Do not commit credentials, generated private keys, Terraform state or fabricated deployment evidence.

On a disposable Docker host, run `bash .github/container-smoke.sh`. It creates and removes named lab containers/volumes, including a physical PostgreSQL recovery drill. Do not run it against existing lab data you intend to keep.
