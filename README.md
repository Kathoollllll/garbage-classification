## Quick Start Guide for Teammates


### Step 1: Install Git LFS (Required for Models)
Before doing anything, install Git LFS so the .keras files download correctly:

**Mac:** brew install git-lfs

**Windows:** Download from git-lfs.com


### Step 2: Pull the Repo

``` git clone https://github.com/Kathoollllll/garbage-classification.git ```

``` cd garbage-classification ```

``` git lfs install ```

``` git lfs pull ```


### Step 3: Setup the Data (Choose One)

**Option A (Fastest):** Download the split_dataset.zip from our Google Drive and extract it into this folder.

**Option B (Manual):** Run the split script using the raw images already in the repo:

``` python split_data.py ```


### Step 4: Run the Classifier
Test the model with a sample image:

``` python classify.py ```


**⚠️ Important Note**
If you don't do Step 1, the model files will only be 1KB (empty pointers) and the code will fail with an OSError.
