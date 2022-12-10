if(isGrayscale):
            grayscale_backup = grayscale_backup.transpose(Image.TRANSPOSE.FLIP_LEFT_RIGHT)
            grayscale_preview_backup = grayscale_preview_backup.transpose(Image.TRANSPOSE.FLIP_LEFT_RIGHT)