import pickle
import random
from matplotlib import pyplot
from PIL import Image

cifar10_path = 'cifar-10-batches-py'
width_of_original_image = 32
height_of_original_image = 32
max_img_on_bg = 15
max_images = 21


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
    all_images = []
    bg = Image.new('RGB', (256, 256), (0, 0, 0))

    for x in range(0, max_images):
        print("Image Number: " + str(x))
        label_names = load_label_names()
        print(label_names[labels[x]])
        resized_image = resize_image(images[x])
        if img_on_bg < max_img_on_bg:
            img_on_bg += 1
        else:
            bg.save(str(bg_id) + '.png', 'PNG')
            img_on_bg = 0
            bg_id += 1
            bg = Image.new('RGB', (256, 256), (0, 0, 0))
            all_images = []

        bg_w, bg_h = bg.size
        img_w, img_h = resized_image.size

        while True:

            x1 = random.randint(0, bg_w - img_w)
            y1 = random.randint(0 + img_h, bg_h)
            offset = (x1, y1)

            # position and size of the image
            # top left x, top right x, width, height
            current_image = list(offset)
            current_image.extend([img_w, img_h])

            if check_for_overlaps(all_images, current_image):
                continue
            else:
                # place the image on the canvas
                bg.paste(resized_image, (x1, 256-y1))

                # store the location information of the image
                all_images.append(current_image)
                break


# check if new image overlaps with existing images
def check_for_overlaps(all_images, new_image):
    # xmin, xmax
    new_image_xaxis = (new_image[0], new_image[0] + new_image[2])
    # ymin, ymax
    new_image_yaxis = (new_image[1] - new_image[3], new_image[1])
    for old_image in all_images:
        old_image_xaxis = (old_image[0], old_image[0] + old_image[2])
        old_image_yaxis = (old_image[1] - old_image[3], new_image[1])

        if is_overlapping(new_image_xaxis, old_image_xaxis) and is_overlapping(new_image_yaxis, old_image_yaxis):
            return True

    return False


# helper function to check if the axes of the images overlap
def is_overlapping(image1, image2):
    if image1[1] >= image2[0] and image2[1] >= image1[0]:
        return True
    else:
        return False


# resize images from a scale of 0.5 to 3
def resize_image(image):
    scale = round(random.uniform(0.5, 1.5), 1)
    image = Image.fromarray(image)
    new_image = image.resize((round(width_of_original_image * scale), round(height_of_original_image * scale)),
                             Image.BILINEAR)
    return new_image


def load_label_names():
    return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


if __name__ == "__main__":
    main()
