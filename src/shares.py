import cv2
import numpy as np
import random 

def encrypt_shares(InputImg, n):
## Img - input image
#  Img shall be binary img. 
## n - how many shares shall be created, 
#  n >= 2, shall be even number
# (non-symetrical encrypting is not allowed, to avoid image distortion)

    # coverto to boolean type
    if len(InputImg.shape) >= 3: InputImg = cv2.cvtColor(InputImg, cv2.COLOR_BGR2GRAY)
    ret, Img = cv2.threshold(InputImg,90,255,cv2.THRESH_BINARY)
    inputSize = InputImg.shape
    OutImgs = []
    outputSize = (inputSize[0]*n,inputSize[1]*n)

    for i in range(n):
        OutImgs.append(np.zeros(outputSize))

    for y in range(0, inputSize[0] ):
        for x in range(0, inputSize[1]):
            if (Img[y,x] == False): # in case of black pixel 
                positions = random.sample([(i, j) for i in range(n) for j in range(n)], n**2)
                Bout = []
                for i in range(n):
                    Bout.append(np.ones((n,n),dtype = bool))
                counter = 0
                j = 0
                for (ry, rx) in positions:
                    Bout[j][ry, rx] = False
                    counter += 1
                    if counter % n == 0:
                        j += 1
                for i in range(n):
                    OutImgs[i][y*n:y*n+n, x*n:x*n+n] = Bout[i]

            else: # in case of white pixel
                Wout = np.ones((n,n), dtype = bool)
                positions = random.sample([(i, j) for i in range(n) for j in range(n)], n)
                for (ry, rx) in positions:
                    Wout[ry, rx] = False
                for i in range(n):
                    OutImgs[i][y*n:y*n+n, x*n:x*n+n] = Wout
    for i in range(n):
        OutImgs[i] = OutImgs[i].astype(np.uint8)
        OutImgs[i] = cv2.normalize(OutImgs[i], None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return OutImgs


def decrypt_shares(Imgs, n):
    if len(Imgs) == n:
        inputSize = Imgs[0].shape
        SumImg = np.zeros(inputSize, dtype = np.uint32)
        for share in Imgs:
            SumImg = np.clip(SumImg + share, 0 ,255)
        SumImg = SumImg.astype(np.uint8)
        output_size = (int(inputSize[0]/n),int(inputSize[1]/n))
        print(f"Input shape{inputSize}, output size: {output_size}")
        OutputImg=np.zeros(output_size, dtype = 'uint8')
        threshold = 200
        for y in range(output_size[0]):
            for x in range(output_size[1]):
                result = SumImg[(n*y):(n*y+n),(n*x):(n*x+n)]
                if np.count_nonzero(result < threshold) == 0:
                    OutputImg[y,x] = 0
                else:
                    OutputImg[y,x] = 255
        # Gaussian blur
        #OutputImg = cv2.GaussianBlur(OutputImg, (3,3), 0)
        return OutputImg
    else:
        print(f'Error: too less images selected ({n} required!')
    

def encrypt_shares_description():
    txt1 =  f"This algorythm divide image into n encrypted image shares.\nAll o fthem are needed to decrypt an image.\n\n"
    txt1 += f"Encryption:\nInput: binary image.\nParameters: n - how many shares should be created.\n\n"
    txt1 += f"Decryption:\nInput: all shares are needed to decrypt image.\nParameters: n - amount of provided shares\n"
    return '1. Shares\n'+txt1