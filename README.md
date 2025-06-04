🖼️ Images_Cryptography
A basic project developed for study purposes. This application allows you to encrypt and decrypt images using simple custom algorithms. It's a great way to explore image processing and cryptography concepts hands-on.

🚀 Features
Load and display images

Encrypt or decrypt images using basic custom algorithms:

• `Visual Secret Sharing`
• `One-Time Pad`

Simple and user-friendly interface 

🚀 How to run

   • To start the application, run the `open.py` file (`src/open.py`):

      python open.py

   •  Compiled files (in Release v1.0) are .exe files. To run application execute:
   
      .\open.exe

🔐 Algorithms Used
• `Visual Secret Sharing`
  Visual Secret Sharing divides the input binary image into n shares.
  Each share alone reveals no information about the original image.
  All n shares are required to decrypt the image.
  
  Each pixel from the input image is mapped to an n×n block across the output shares.
  As a result, each share is n times larger in size.
  This algorithm is designed for binary (black & white) images.
  If grayscale or color images are used, information loss will occur during encryption.
  
  Input:
  
  Binary image
  
  Parameter n – number of shares to create
  
  Output:
  
  n share images

• `One-Time Pad`
  This algorithm performs a pixel-wise bitwise XOR between the input image and a key image.
  The key image must be the same size as the input image.
  Decryption is done by applying XOR again with the same key.
  
  This method is also designed for binary images.
  Using grayscale or color images will result in information loss.
  
  Input:
  
  Binary image
  
  Key image (same size as input)
  
  Output:
  
  Encrypted or decrypted image

🛠️ Technologies Used
Programming Language:

Python 3.11.9

Libraries / Frameworks:

NumPy 2.0.2

OpenCV 4.11.0.86

Tkinter 8.6

📌 Notes
This is the first version of the project.

Created for educational purposes by two students.

