import tensorflow as tf
from tf.keras.datasets import mnist

def create_input_from_mnist(index=0, normalize=True):
    """
    Loads an image from the MNIST dataset and prepares it as an input tensor.

    Parameters:
    - index: The index of the image in the MNIST test set (default: 0).
    - normalize: Whether to normalize pixel values to [0,1].

    Returns:
    - input_tensor: The processed MNIST image as a TensorFlow tensor.
    - label: The corresponding label of the image.
    """
    # Load the MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Select an image from the test set
    image = x_test[index]
    label = y_test[index]  # Get the corresponding label

    # Reshape to (32,32,1) to match LeNet input size (original MNIST is 28x28)
    image = tf.image.resize(image[..., tf.newaxis], [32, 32])  # Add channel dimension & resize

    # Normalize if required
    if normalize:
        image = tf.cast(image, tf.float32) / 255.0  # Normalize to range [0,1]

    # Expand batch dimension to simulate input batch
    input_tensor = tf.expand_dims(image, axis=0)  # Shape becomes (1, 32, 32, 1)

    return input_tensor, label

# Example usage
input_tensor, label = create_input_from_mnist(index=10)
print("Input Tensor Shape:", input_tensor.shape)
print("Label:", label)
