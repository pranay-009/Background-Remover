from PIL import Image,ImageOps
from rembg import new_session
import numpy as np
import cv2

class BackgroundRemover:

    def __init__(self,model_name="unetp"):

        self.session = new_session(model_name)
    
    def read_image(self,path):
        """
        Read the image.

        Args:
            path (str): The image path.
     
        Returns:
            PILImage: Original Image .
        """
        

        image = Image.open(path)
        return image
    
    def resize_image(self,image,width,height):
        """
        Resize the image.

        Args:
            img (PILImage): The image to be modified.
            width (int): The width of the image.
            height (int): The height of the image.

        Returns:
            PILImage: The resized image .
        """

        image = image.resize((width,height))
        return image
    
    def putalpha_cutout(self,img, mask):
        """
        Apply the specified mask to the image as an alpha cutout.

        Args:
            img (PILImage): The image to be modified.
            mask (PILImage): The mask to be applied.

        Returns:
            PILImage: The modified image with the alpha cutout applied.
        """
        img.putalpha(mask)
        return img

    def get_concat_v(self,img1, img2):
        """
        Concatenate two images vertically.

        Args:
            img1 (PILImage): The first image.
            img2 (PILImage): The second image to be concatenated below the first image.

        Returns:
            PILImage: The concatenated image.
        """
        dst = Image.new("RGBA", (img1.width, img1.height + img2.height))
        dst.paste(img1, (0, 0))
        dst.paste(img2, (0, img1.height))
        return dst

    def get_concat_v_multi(self,imgs):
        """
        Concatenate multiple images vertically.

        Args:
            imgs (List[PILImage]): The list of images to be concatenated.

        Returns:
            PILImage: The concatenated image.
        """
        pivot = imgs.pop(0)
        for im in imgs:
            pivot = self.get_concat_v(pivot, im)
        return pivot
    
    def apply_background(self,img,filepath,w,h):
        """
        Apply the specified background color to the image.

        Args:
            img (PILImage): The image to be modified.
            color (Tuple[int, int, int, int]): The RGBA color to be applied.

        Returns:
            PILImage: The modified image with the background color applied.
        """
    
        colored_image = self.read_image(filepath)
        colored_image = self.resize_image(colored_image,width=w,height=h)
        colored_image = colored_image.convert("RGBA")
        colored_image.paste(img, mask=img)

        return colored_image
    
    def process_video(self,frame,background_path):
        """
        Remove background to the image and replace with a selective background.

        Args:
            img_path: The first image path.
            background_path: The background image path.
            output_path :The directory where the file wile be saved. (optional)
            save: Whether to save the file or not. (optional)

        Returns:
            PILImage: background removed image.
        """


        lst_imgs=[]
        input = Image.fromarray(frame)
        width, height=input.size
        input=ImageOps.exif_transpose(input)
        masks = self.session.predict(input)
        for mask in masks:
            cutout = self.putalpha_cutout(input, mask)
            lst_imgs.append(cutout)
        cutout=input
        if len(lst_imgs) > 0:
            cutout = self.get_concat_v_multi(lst_imgs)
        
        result = self.apply_background(input , background_path , width , height)
        result = np.array(result)


        return result
        

    def process(self,img_path,background_path,output_path="",save=False):
        """
        Remove background to the image and replace with a selective background.

        Args:
            img_path: The first image path.
            background_path: The background image path.
            output_path :The directory where the file wile be saved. (optional)
            save: Whether to save the file or not. (optional)

        Returns:
            PILImage: background removed image.
        """


        lst_imgs=[]
        input = self.read_image(img_path)
        width, height=input.size
        input=ImageOps.exif_transpose(input)
        masks = self.session.predict(input)
        for mask in masks:
            cutout = self.putalpha_cutout(input, mask)
            lst_imgs.append(cutout)
        cutout=input
        if len(lst_imgs) > 0:
            cutout = self.get_concat_v_multi(lst_imgs)
        
        result = self.apply_background(input , background_path , width , height)

        if save:
            result.save(output_path)

        return result






