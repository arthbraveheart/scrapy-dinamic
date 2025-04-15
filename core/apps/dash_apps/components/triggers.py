import subprocess
from .constants import MAKE_MAP

def run_crawler(seller):

    spider = MAKE_MAP.get(seller)

    try:
        subprocess.run(
            ["make", spider],
            check=True
        )
        return "Spider completed successfully!"
    except subprocess.CalledProcessError as e:
        return f"Crawler failed with return code:\n\t {e}"