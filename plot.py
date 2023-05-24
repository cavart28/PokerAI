from PokerAI.deck import suits, faces_values

import os
from itertools import product
import matplotlib.image as mpimg
import matplotlib.pyplot as plt



pic_folder = os.path.dirname(os.path.realpath(__file__)) + '/card_pics/'


def make_image_dict(pic_folder=pic_folder):
    image_dict = dict()
    for card in product(suits, faces_values):
        card_filename = f'({card[0]}, {card[1]})'
        img_loc = os.path.join(pic_folder, card_filename)
        image_dict[card] = mpimg.imread(img_loc)
    return image_dict

image_dict = make_image_dict()

def plot_hand(hand):
    n_cards = len(hand)
    _, axs = plt.subplots(1, n_cards)
    for ax, card in zip(axs, hand):
        ax.imshow(image_dict[card])
        ax.axis('off')
    
