# OCR/image recognition using basic machine learning with k-NN (no imports), as seen on clumsy computer 2020/07/06

VOD: Coming soon!

This is a simple program that performs image recognition on the
[mnist](http://yann.lecun.com/exdb/mnist/)
and
[fashion-mnist](https://github.com/zalandoresearch/fashion-mnist)
datasets using the k-nearest neighbors algorithm. It's around 170 lines of Python and
represents a very basic example of image recognition. It's not particularly fast, but I hope you
find it easy to follow and interesting!

The program also includes the `read_images()` and `read_labels()` functions which read the
MNIST data format, used in both datasets.

As a disclaimer, I did end up importing _PIL_ and _numpy_ in the final code, but
this was stricly so that we can see the images we're working with, and load in our own images.
These imports are not required for the code to work, hence me keeping the description of
“no imports”.

If you'd like to run this, you can change the following variables:

* `DEBUG` at the top determines whether or not you want to write out and/or read in your own
  images, which happens in `main()`.
* `n_train` and `n_test` in `main()` determine how many samples you want to load from the dataset
  for training and testing respectively, which is useful so running the program doesn't take ages.
* `k` in `main()` determines the `k` used in the k-nearest neighbors algorithm.

Keep in mind that running this program can take some time as k-NN is not the fastest
algorithm!
