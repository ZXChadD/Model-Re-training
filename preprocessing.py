import pickle
import random
from matplotlib import pyplot
from PIL import Image

cifar10_path = 'cifar-10-batches-py'
width = 32
height = 32


def main():
    create_training_data()


def load_cfar10_batch(cifar10_path, batch_id):
    with open(cifar10_path + '/data_batch_' + str(batch_id), mode='rb') as file:
        batch = pickle.load(file, encoding='latin1')

    images = batch['data'].reshape((len(batch['data']), 3, 32, 32)).transpose(0, 2, 3, 1)
    labels = batch['labels']
    return images, labels


def create_training_data():
    images, labels = load_cfar10_batch(cifar10_path, 1)

    img_on_bg = 0
    bg_id = 0
    bg = Image.new('RGB', (256, 256), (0, 0, 0))

    for x in range(0, 10000):
        resized_image = resize_image(images[x])
        if img_on_bg <= 49:
            img_on_bg += 1
        else:
            img_on_bg = 0
            bg.save('bg_' + str(bg_id) + '.png')
            bg_id += 1
            bg = Image.new('RGB', (256, 256), (0, 0, 0))

        bg_w, bg_h = bg.size
        img_w, img_h = resized_image.size

        y_axis = random.randint(0, bg_w - img_w)
        x_axis = random.randint(0, bg_h - img_h)
        offset = (x_axis,y_axis)

        # place the image on the canvas
        bg.paste(resized_image, offset)

    bg.show()

    # new_image = resize_image(images[3])
    # pyplot.imshow(new_image)
    # pyplot.show()


# resize images from a scale of 0.5 to 3
def resize_image(image):
    scale = round(random.uniform(0.5, 3.0), 1)
    image = Image.fromarray(image)
    new_image = image.resize((round(width * scale), round(height * scale)))
    return new_image


def load_label_names():
    return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


if __name__ == "__main__":
    main()
