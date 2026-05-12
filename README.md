Team Setup Guide
Install Git LFS: * Mac: brew install git-lfs

Windows: Download from git-lfs.com

Clone & Pull Models:

Bash
git clone https://github.com/Kathoollllll/garbage-classification.git
cd garbage-classification
git lfs install
git lfs pull
Get the Images:

Download split_dataset from our shared Google Drive.

Place the folder inside the project directory.

Note: Without Step 1, the model files will be "empty" pointers and the code will crash.
