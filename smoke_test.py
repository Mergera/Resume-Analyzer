import importlib
import os
import sys


REQUIRED_MODULES = [
    "streamlit",
    "PyPDF2",
    "google.genai",
    "langchain",
    "langchain_ollama",
]


def main() -> int:
    print("Running smoke test...")

    failed = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
            print(f"[OK] import {module_name}")
        except Exception as exc:
            print(f"[FAIL] import {module_name}: {exc}")
            failed.append(module_name)

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("[OK] GOOGLE_API_KEY is set")
    else:
        print("[WARN] GOOGLE_API_KEY is not set")

    if failed:
        print("\nSmoke test failed. Install dependencies and retry.")
        return 1

    print("[INFO] For Ollama mode, verify Ollama is running and model exists (for example: mistral).")
    print("\nSmoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


