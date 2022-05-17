#NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.GPU0)

from deoldify.visualize import *
plt.style.use('dark_background')
torch.backends.cudnn.benchmark=True
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

import glob
import os
import argparse
from tqdm import tqdm




def main(args):

    colorizer = get_image_colorizer(artistic=False)

    for vid in tqdm(sorted(os.listdir(args.source_path))):
        for fn in tqdm(sorted(glob.glob(f'{args.source_path}/{vid}/left/*')), leave=False):
            fn_out = Path(f'{args.source_path}/{vid}/left_{args.result_folder}')
            os.makedirs(fn_out, exist_ok=True)

            result = colorizer.get_transformed_image(path=fn, render_factor=args.render_factor, watermarked=False)
            _ = colorizer._save_result_image(Path(fn), result, results_dir=fn_out)
            result.close()
        
        for fn in tqdm(sorted(glob.glob(f'{args.source_path}/{vid}/right/*')), leave=False):
            fn_out = Path(f'{args.source_path}/{vid}/right_{args.result_folder}')
            os.makedirs(fn_out, exist_ok=True)
            result = colorizer.get_transformed_image(path=fn, render_factor=args.render_factor, watermarked=False)
            _ = colorizer._save_result_image(Path(fn), result, results_dir=fn_out)
            result.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--source_path", help="folder for source images",)
    parser.add_argument("--result_folder", default='colorized', help="folder name for colorized outputs")

    parser.add_argument( "--render_factor", default=45, help="render factor")

    args = parser.parse_args()

    
    main(args)