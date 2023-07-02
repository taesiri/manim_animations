from manim import *
from PIL import Image
import torchvision.transforms.functional as fv
import torchvision.transforms as transforms
from functools import partial
import numpy as np


class ImageToGrid(Scene):
    def construct(self):
        # Set the background color to white
        self.camera.background_color = WHITE

        # Load the image
        img_path = "photo.jpeg"
        img_obj = ImageMobject(img_path)
        img_obj.scale_to_fit_height(5)

        # Show the image in the white background
        self.play(FadeIn(img_obj))
        self.wait()

        # Slice the image into 9 patches using PIL
        img = Image.open(img_path)
        width, height = img.size
        patch_width = width // 3
        patch_height = height // 3
        patches = []
        for i in range(3):
            for j in range(3):
                left = j * patch_width
                upper = i * patch_height
                right = left + patch_width
                lower = upper + patch_height
                patch = img.crop((left, upper, right, lower))
                patches.append(patch)

        # Replace the original one with the 9 patches
        patch_mobs = []
        for patch in patches:
            patch_np = np.array(patch)
            patch_mob = ImageMobject(patch_np)
            patch_mob.scale_to_fit_height(5 / 3)
            patch_mobs.append(patch_mob)
        self.remove(img_obj)

        # Initial positions of each patch
        initial_positions = [
            [-5 / 3, 5 / 3, 0],
            [0, 5 / 3, 0],
            [5 / 3, 5 / 3, 0],
            [-5 / 3, 0, 0],
            [0, 0, 0],
            [5 / 3, 0, 0],
            [-5 / 3, -5 / 3, 0],
            [0, -5 / 3, 0],
            [5 / 3, -5 / 3, 0],
        ]

        # Set each patch to its initial position
        for patch_mob, initial_position in zip(patch_mobs, initial_positions):
            patch_mob.move_to(initial_position)

        # Add all patches to the scene
        self.add(*patch_mobs)

        # Final positions of each patch
        target_positions = [
            [-2, 2, 0],
            [0, 2, 0],
            [2, 2, 0],
            [-2, 0, 0],
            [0, 0, 0],
            [2, 0, 0],
            [-2, -2, 0],
            [0, -2, 0],
            [2, -2, 0],
        ]

        # Create dots for the target positions
        dots = [
            Dot(point=position, radius=0.1, color=BLACK)
            for position in target_positions
        ]

        # Slowly animate patches away from their original location all at once
        animations = [
            patch_mob.animate.move_to(target_position)
            for patch_mob, target_position in zip(patch_mobs, target_positions)
        ]

        # Add animations for the dots to appear
        animations += [FadeIn(dot) for dot in dots]

        # Play all animations
        self.play(*animations, run_time=2)

        self.wait()
