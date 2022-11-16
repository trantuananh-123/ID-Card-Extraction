import cv2
from detecto import core, utils, visualize
from non_max_suppression_fast import non_max_suppression_fast


def get_center_point(box):
    xmin, ymin, xmax, ymax = box
    return (xmin + xmax) // 2, (ymin + ymax) // 2


def corner(path):
    # dataset = core.Dataset('D:/Nam-4/Nam-4/HTTM/sample')
    model = core.Model([
        'top_left', 'top_right', 'bottom_right', 'bottom_left'
    ])

    # losses = model.fit(dataset, epochs=100, verbose=True, learning_rate=0.001)
    model.load('./weights/corner_2.pth', ['top_left', 'top_right', 'bottom_right', 'bottom_left'])

    fname = path
    image = utils.read_image(fname)

    labels, boxes, scores = model.predict(image)

    final_boxes, final_labels = non_max_suppression_fast(
        boxes.numpy(), labels, 0.15)


    for i, bbox in enumerate(final_boxes):
        bbox = list(map(int, bbox))
        x_min, y_min, x_max, y_max = bbox
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(image, labels[i], (x_min, y_min),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        final_points = list(map(get_center_point, final_boxes))
        label_boxes = dict(zip(final_labels, final_points))

    return image
