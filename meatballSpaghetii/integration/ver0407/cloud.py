


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

class wordCloudGenerator:
    def generate_wordcloud(self, freq, mask_path, font_path, output_path="wordcloud.png"):
        mask = np.array(Image.open(mask_path))
        wc = WordCloud(width=800, height=400, mask=mask, font_path=font_path, background_color="white").generate_from_frequencies(freq)
        image_colors = ImageColorGenerator(mask)
        wc.recolor(color_func=image_colors)
        plt.figure(figsize=(5, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(output_path)
        plt.show()