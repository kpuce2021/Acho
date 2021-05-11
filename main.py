import torch

import argparse
import shutil
import os
import os.path

from Face_parsing.test import parsing
from stargan_v2.test import stargan
from SEAN.test import reconstruct

def main(args):
    print(args)
    torch.manual_seed(args.seed)

    if os.path.exists("./results") == True:
      shutil.rmtree("./results") 

    sourcefemale = './data/src/female'
    sourcemale = './data/src/male'

    destination = './data/srcc'
    reffemale = './data/ref/female'
    refmale = './data/ref/male'

    filesfemale = os.listdir(sourcefemale)
    filesmale = os.listdir(sourcemale)

    count = 0
    exist = 0
    
    if args.mode == 'styling':
        # StarGAN > Parsing > SEAN

        stargan(args)
    
        for f in filesfemale:
            exist += 1

        if exist != 0:
          for f in filesfemale:
            sourceFile = os.path.join(sourcefemale, f)
            print( "copying " + sourceFile + " to " + destination  )
            shutil.copy(sourceFile, destination)
            count = count + 1
        else:
          for f in filesmale:
            sourceFile = os.path.join(sourcemale, f)
            print( "copying " + sourceFile + " to " + destination  )
            shutil.copy(sourceFile, destination)    
            
         
        parsing(respth='./results/label/src', dspth='./data/srcc') # parsing src_image
        parsing(respth='./results/label/others', dspth='./results/img') # parsing fake_image

        reconstruct(args.mode)

        sourceresult = './results/results/synthesized_image' 
        filesresult = os.listdir(sourceresult)

        if count == 1:
          for f in filesresult:
            
            sourceFile = os.path.join(sourceresult, f)
            print( "Moving " + sourceFile + " to " + reffemale  )
            shutil.rmtree("./data/ref/female/")
            os.mkdir("./data/ref/female")
            shutil.move(sourceFile, reffemale)
            count = 0
        else:
          for f in filesresult:
            sourceFile = os.path.join(sourceresult, f)
            print( "Moving " + sourceFile + " to " + refmale  )
            shutil.rmtree("./data/ref/male/")
            os.mkdir("./data/ref/male")
            shutil.move(sourceFile, refmale)

        stargan(args)

      
        shutil.rmtree("./data/ref/female/")
        shutil.rmtree("./data/ref/male/")
        shutil.rmtree("./data/src/female/")
        shutil.rmtree("./data/src/male/")
        shutil.rmtree("./data/srcc/")

        os.mkdir("./data/ref/female")
        os.mkdir("./data/ref/male")
        os.mkdir("./data/src/female")
        os.mkdir("./data/src/male")
        os.mkdir("./data/srcc")
    
    else:
        raise NotImplementedError


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # implement
    parser.add_argument('--mode', type=str, required=True,
                        choices=['styling'], help='set mode')
    parser.add_argument('--seed', type=int, default=777,
                        help='Seed for random number generator')

    # StarGAN_v2
    parser.add_argument('--img_size', type=int, default=256, help='Image resolution')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers used in DataLoader')

    parser.add_argument('--num_domains', type=int, default=2, help='Number of domains')
    parser.add_argument('--latent_dim', type=int, default=16, help='Latent vector dimension')
    parser.add_argument('--hidden_dim', type=int, default=512, help='Hidden dimension of mapping network')
    parser.add_argument('--style_dim', type=int, default=64,help='Style code dimension')
    parser.add_argument('--w_hpf', type=float, default=1, help='weight for high-pass filtering')

    parser.add_argument('--resume_iter', type=int, default=184000,help='Iterations to resume training/testing')
    parser.add_argument('--checkpoint_dir', type=str, default='pretrained_network/StarGAN')
    parser.add_argument('--wing_path', type=str, default='pretrained_network/StarGAN/wing.ckpt')

    parser.add_argument('--src_dir', type=str, default='./data/src')
    parser.add_argument('--result_dir', type=str, default='./results/img')
    
    # for styling_ref
    parser.add_argument('--ref_dir', type=str, default='./data/ref')

    # for styling_rand
    parser.add_argument('--target_domain', type=int, default=0)
    parser.add_argument('--num_outs_per_domain', type=int, default=3)
    
    args = parser.parse_args()
    main(args)
