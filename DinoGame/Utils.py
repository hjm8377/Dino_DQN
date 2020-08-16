from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import base64
import torch


class Util:

    def screenshot(self, browser):
        image_b64 = browser.execute_script
        screen = np.array(Image.open(BytesIO(base64.b64decode(image_b64))))
        image = self.process_img(screen)
        return image

    def show_img(self, graphs=False):
        while True:
            screen = (yield)
            window_title = "Dino Agent"
            cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
            imS = cv2.resize(screen, (800, 400))
            cv2.imshow(window_title, screen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def process_img(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = image[:500, :600]
        image = cv2.resize(image, (84, 84))
        image[image > 0] = 255
        image = np.reshape(image, (84, 84, 1))
        return image

    def image_to_tensor(self, image):
        image = np.transpose(image, (2, 0, 1))
        image_tensor = image.astype(np.float32)
        image_tensor = torch.from_numpy(image)
        if torch.cuda.is_available():
            image_tensor = image_tensor.cuda()
        return image_tensor