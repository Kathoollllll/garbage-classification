import splitfolders

splitfolders.ratio(
    "Garbage_Classification", 
    output="split_dataset",
    seed=42,
    ratio=(0.7, 0.15, 0.15)
)