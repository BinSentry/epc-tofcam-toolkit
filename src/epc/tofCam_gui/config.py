from pathlib import Path
from epc.tofCam_data.config import CrcCalc, NARROW_FIELD, STANDARD_FIELD, WIDE_FIELD

EPC_LOGO = Path(__file__).parent / "icons" / "epc-logo.png"
DATA = Path(__file__).parent.parent / "data"

if __name__ == "__main__":
    with open(WIDE_FIELD, "r") as f:
        x = f.read()
        print(x)

    with open(NARROW_FIELD, "r") as f:
        x = f.read()
        print(x)

    with open(STANDARD_FIELD, "r") as f:
        x = f.read()
        print(x)

    # with open(CrcCalc_linux, "rb") as f:
    #     x = f.read()

    with open(CrcCalc, "rb") as f:
        f.read()

    # with open(CrcCalc_darwin, "rb") as f:
    #     x = f.read()

    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image
    im = Image.open(EPC_LOGO)
    data = np.array(im)
    plt.imshow(data)  # shows a bluish image of the logo
    plt.show()
