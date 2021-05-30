import torch
import time


import argparse
import shutil
import os
import os.path

from Face_parsing.test import parsing
from stargan_v2.test import stargan
from SEAN.test import reconstruct

def main(args):
    torch.manual_seed(args.seed)
    
    if os.path.exists("./results") == True:
        shutil.rmtree("./results") 

    sourceYes = './Acho/data/src/yes'
    sourceNo = './Acho/data/src/no'
    sourceMiddle = './Acho/data/src/middle'


    destination = './Acho/data/srcc'
    refYes = './Acho/data/ref/yes'
    refNo = './Acho/data/ref/no'
    refMiddle = './data/ref/middle'
    
    filesYes = os.listdir(sourceYes)
    filesNo = os.listdir(sourceNo)
    filesMiddle = os.listdir(sourceMiddle)



    count = 0
    exist = 0

    if args.mode == 'styling':
        # StarGAN > Parsing > SEAN
        
        
        stargan(args)
        

    
        for f in filesYes:
            exist = 1
        for f in filesMiddle:
            exist = 2


        if exist == 1:
            for f in filesYes:   
                sourceFile = os.path.join(sourceYes, f)
                print( "copying " + sourceFile + " to " + destination  )
                shutil.copy(sourceFile, destination)
                count = count + 1
        elif exist == 2:
            for f in filesMiddle:
                sourceFile = os.path.join(sourceMiddle, f)
                print( "copying " + sourceFile + " to " + destination  )
                shutil.copy(sourceFile, destination)
                count = count + 2
        else:
            for f in filesNo:
                sourceFile = os.path.join(sourceNo, f)
                print( "copying " + sourceFile + " to " + destination  )
                shutil.copy(sourceFile, destination)    
            
         
        parsing(respth='./Acho/results/label/src', dspth='./Acho/data/srcc') # parsing src_image
        parsing(respth='./Acho/results/label/others', dspth='./Acho/results/img') # parsing fake_image

        reconstruct(args.mode)

        sourceresult = './Acho/results/results/synthesized_image' 
        filesresult = os.listdir(sourceresult)

        if count == 1:
            for f in filesresult:
            
                sourceFile = os.path.join(sourceresult, f)
                print( "Moving " + sourceFile + " to " + refYes  )
                shutil.rmtree("./Acho/data/ref/yes/")
                os.mkdir("./Acho/data/ref/yes")
                shutil.move(sourceFile, refYes)
                count = 0
        elif count == 2:
            for f in filesresult:
            
                sourceFile = os.path.join(sourceresult, f)
                print( "Moving " + sourceFile + " to " + refMiddle  )
                shutil.rmtree("./Acho/data/ref/middle/")
                os.mkdir("./Acho/data/ref/middle")
                shutil.move(sourceFile, refMiddle)
                count = 0
        else:
            for f in filesresult:
                sourceFile = os.path.join(sourceresult, f)
                print( "Moving " + sourceFile + " to " + refNo  )
                shutil.rmtree("./Acho/data/ref/no/")
                os.mkdir("./Acho/data/ref/no")
                shutil.move(sourceFile, refNo)

        stargan(args)

      
        shutil.rmtree("./Acho/data/ref/yes/")
        shutil.rmtree("./Acho/data/ref/middle/")
        shutil.rmtree("./Acho/data/ref/no/")
        shutil.rmtree("./Acho/data/src/yes/")
        shutil.rmtree("./Acho/data/src/middle/")
        shutil.rmtree("./Acho/data/src/no/")
        shutil.rmtree("./Acho/data/srcc/")

        os.mkdir("./Acho/data/ref/yes")
        os.mkdir("./Acho/data/ref/middle")
        os.mkdir("./Acho/data/ref/no")
        os.mkdir("./Acho/data/src/yes")
        os.mkdir("./Acho/data/src/middle")
        os.mkdir("./Acho/data/src/no")
        os.mkdir("./Acho/data/srcc")
    
    else:
        raise NotImplementedError


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # implement
    parser.add_argument('--mode', type=str,choices=['styling'],default = 'styling',help='set mode')
    parser.add_argument('--seed', type=int, default=777,
                        help='Seed for random number generator')

    # StarGAN_v2
    parser.add_argument('--img_size', type=int, default=256, help='Image resolution')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--num_workers', type=int, default=4, help='Number of workers used in DataLoader')

    parser.add_argument('--num_domains', type=int, default=3, help='Number of domains')
    parser.add_argument('--latent_dim', type=int, default=16, help='Latent vector dimension')
    parser.add_argument('--hidden_dim', type=int, default=512, help='Hidden dimension of mapping network')
    parser.add_argument('--style_dim', type=int, default=64,help='Style code dimension')
    parser.add_argument('--w_hpf', type=float, default=1, help='weight for high-pass filtering')

    parser.add_argument('--resume_iter', type=int, default=110400,help='Iterations to resume training/testing')
    parser.add_argument('--checkpoint_dir', type=str, default='Acho/pretrained_network/StarGAN')
    parser.add_argument('--wing_path', type=str, default='Acho/pretrained_network/StarGAN/wing.ckpt')

    parser.add_argument('--src_dir', type=str, default='./Acho/data/src')
    parser.add_argument('--result_dir', type=str, default='./Acho/results/img')
    
    # for styling_ref
    parser.add_argument('--ref_dir', type=str, default='./Acho/data/ref')

    # for styling_rand
    parser.add_argument('--target_domain', type=int, default=0)
    parser.add_argument('--num_outs_per_domain', type=int, default=3)
    
    args = parser.parse_args()
    main(args)
