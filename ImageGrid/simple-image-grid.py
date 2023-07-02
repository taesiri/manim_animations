from manim import *
from PIL import Image
import numpy as np
from functools import partial
import torchvision.transforms.functional as fv
import torchvision.transforms as transforms


def crop_at(size, slice_x, slice_y):
    def slice_crop(image, size, slice_x, slice_y):
        width, height = image.size
        tile_size_x = width // 3
        tile_size_y = height // 3
        anchor_x = (slice_y * tile_size_x) + (tile_size_x // 2)
        anchor_y = (slice_x * tile_size_y) + (tile_size_y // 2)
        return fv.crop(
            image,
            anchor_y - (size // 2),
            anchor_x - (size // 2),
            size,
            size,
        )

    return partial(slice_crop, size=size, slice_x=slice_x, slice_y=slice_y)


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

        # Slice the image into 9 patches using torchvision.transforms and the crop_at function
        img = Image.open(img_path)

        zoom_scales = [256, 512, 768, 1024]

        patch_mobs = []
        for i in range(3):
            for j in range(3):
                zoom_transform = transforms.Compose(
                    [
                        transforms.Resize(
                            zoom_scales[0],
                            interpolation=transforms.InterpolationMode.BICUBIC,
                        ),
                        crop_at(224, i, j),
                    ]
                )
                patch = zoom_transform(img)
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

        # Animate zoom scale transitions
        for scale in zoom_scales[1:]:
            new_patch_mobs = []
            for i in range(3):
                for j in range(3):
                    zoom_transform = transforms.Compose(
                        [
                            transforms.Resize(
                                scale,
                                interpolation=transforms.InterpolationMode.BICUBIC,
                            ),
                            crop_at(224, i, j),
                        ]
                    )
                    patch = zoom_transform(img)
                    patch_np = np.array(patch)
                    patch_mob = ImageMobject(patch_np)
                    patch_mob.scale_to_fit_height(5 / 3)
                    patch_mob.move_to(patch_mobs[i * 3 + j].get_center())
                    new_patch_mobs.append(patch_mob)

            # Animate transition to new patches
            self.play(*[FadeOut(old) for old in patch_mobs], run_time=0.5)
            self.play(*[FadeIn(new) for new in new_patch_mobs], run_time=0.5)
            patch_mobs = new_patch_mobs

        self.wait()
