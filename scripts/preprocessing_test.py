import pickle
import random
from matplotlib import pyplot
from PIL import Image
from PIL import ImageDraw
from pascal_voc_writer import Writer

cifar10_path = 'cifar-10-batches-py'
width_of_original_image = 32
height_of_original_image = 32
max_img_on_bg = 20
max_images = 10000


def main():
    create_training_data()


def create_training_data():
    images, labels = load_cfar10_batch(cifar10_path, 1)
    img_on_bg = 1
    bg_id = 0

    # list of all images that have been placed on the background
    all_images = []

    # list of coordinates that should not be chosen from
    excluded_coordinates = set()

    # create a new background
    bg = Image.new('RGB', (256, 256), (0, 0, 0))

    # store all possible coordinates
    all_coordinates = set()
    for x_coordinates in range(0, 216):
        for y_coordinates in range(40, 256):
            coordinates = (x_coordinates, y_coordinates)
            all_coordinates.add(coordinates)

    ####### initialise a writer to create pascal voc file #######
    writer = Writer(
        '/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test/' + str(
            bg_id) + '.jpg', 256, 256)

    file = open(
        "/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test_ground/" + str(
            bg_id) + ".txt", "w")

    for x in range(0, max_images):
        print("Image Number: " + str(x))
        label_names = load_label_names()
        name_of_object = label_names[labels[x]]
        print(name_of_object)
        resized_image = resize_image(images[x])

        # once the desired number of images have been placed on the background, create a new background
        if img_on_bg > max_img_on_bg or x == max_images - 1:
            bg.save(
                '/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test/' + str(
                    bg_id) + '.jpg', 'JPEG')
            img_on_bg = 1

            ####### save pascal voc file #######
            writer.save(
                '/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test/' + str(
                    bg_id) + '.xml')

            file.close()

            if not x == max_images - 1:
                bg_id += 1
                bg = Image.new('RGB', (256, 256), (0, 0, 0))
                all_images = []
                excluded_coordinates = set()

                ####### initialise a writer to create pascal voc file #######
                writer = Writer(
                    '/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test/' + str(
                        bg_id) + '.jpg', 256, 256)

                ####### initialise a writer to create TXT file #######
                file = open(
                    "/Users/chadd/Documents/Chadd/Work/DSO/Model_Re-training/TensorFlow/workspace/training/images/test_ground/" + str(
                        bg_id) + ".txt", "w")

        img_w, img_h = resized_image.size

        while True:

            # choose coordinates from the remaining set of coordinates
            remaining_coordinates = all_coordinates - excluded_coordinates
            offset = random.choice(tuple(remaining_coordinates))
            x1, y1 = offset

            # position and size of the current image
            # top left x, top right x, width, height
            current_image = list(offset)
            current_image.extend([img_w, img_h])

            if check_for_overlaps(all_images, current_image) and len(excluded_coordinates) != 0 and len(
                    all_images) != 0:
                continue
            else:

                img_on_bg += 1

                # place the image on the background
                bg.paste(resized_image, (x1, 256 - y1))

                # store the location information of the image
                all_images.append(current_image)

                ####### add object to pascal voc file #######
                if name_of_object != 'horse':
                    writer.addObject(name_of_object, x1, 256 - y1, x1 + img_w, 256 - y1 + img_h)
                    line_of_text = "%s %s %s %s %s\n" % (name_of_object, x1, 256 - y1, x1 + img_w, 256 - y1 + img_h)
                    file.write(line_of_text)

                # draw rectangles
                # img1 = ImageDraw.Draw(bg)
                # img1.rectangle([(x1, 256 - y1), (x1 + img_w, 256 - y1 + img_h)], outline=(255, 0, 0), fill=None)

                # add to the excluded coordinates list
                for x_coordinates in range(x1, x1 + img_w):
                    for y_coordinates in range(y1 - img_h, y1):
                        coordinates = (x_coordinates, y_coordinates)
                        excluded_coordinates.add(coordinates)

                break


# load the cifar dataset
def load_cfar10_batch(cifar10_path, batch_id):
    with open(cifar10_path + '/test_batch', mode='rb') as file:
        batch = pickle.load(file, encoding='latin1')

    images = batch['data'].reshape((len(batch['data']), 3, 32, 32)).transpose(0, 2, 3, 1)
    labels = batch['labels']
    return images, labels


# check if new image overlaps with existing images
def check_for_overlaps(all_images, new_image):
    # x-min, x-max for new image
    new_image_xaxis = (new_image[0], new_image[0] + new_image[2])

    # y-min, y-max for new image
    new_image_yaxis = (new_image[1] - new_image[3], new_image[1])

    for old_image in all_images:

        # x-min, x-max for old image
        old_image_xaxis = (old_image[0], old_image[0] + old_image[2])

        # y-min, y-max for old image
        old_image_yaxis = (old_image[1] - old_image[3], old_image[1])

        if is_overlapping(new_image_xaxis, old_image_xaxis) and is_overlapping(new_image_yaxis, old_image_yaxis):
            return True

    return False


# helper function to check if the axes of the images overlap
def is_overlapping(image1, image2):
    if image1[1] >= image2[0] and image2[1] >= image1[0]:
        return True
    else:
        return False


# resize images from a scale of 0.5 to 1.25
def resize_image(image):
    scale = round(random.uniform(0.5, 1.25), 1)
    image = Image.fromarray(image)
    new_image = image.resize((round(width_of_original_image * scale), round(height_of_original_image * scale)),
                             Image.BILINEAR)
    return new_image


def load_label_names():
    return ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


if __name__ == "__main__":
    main()
